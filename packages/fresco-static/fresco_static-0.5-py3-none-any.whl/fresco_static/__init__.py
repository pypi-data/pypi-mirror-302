# Copyright 2015 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from posixpath import isfile
from posixpath import isdir
from posixpath import join
import atexit
import contextlib
import logging

from importlib import resources

from fresco import GET
from fresco import HEAD
from fresco import context
from fresco.static import serve_static_file
from fresco.util.urls import normpath

__version__ = "0.5"

logger = logging.getLogger(__name__)


def gather_headers(*sources):
    headers = {}
    header_names = {}
    for source in sources:
        for key, value in source.items():
            header_names[key.lower()] = key
            key = key.lower()
            if value is None:
                headers.pop(key, None)
            else:
                headers[key] = value
    return {header_names[key]: value for key, value in headers.items()}


class StaticFiles(object):
    #: Registry of instances
    __registry__ = {}

    def __init__(
        self, app=None, prefix="/static", cache_max_age=60, route_name="static",
        headers=None
    ):
        self.__class__.__registry__[app] = self
        self.app = app
        self.prefix = prefix
        self.route_name = route_name
        self.sources = {}
        self.file_context = contextlib.ExitStack()
        self.headers = {}

        if cache_max_age:
            self.headers["Cache-Control"] = f"max-age: {cache_max_age}"

        if headers:
            self.headers.update(headers)

        if app is not None:
            self.init_app(app)

        atexit.register(self.close)

    @classmethod
    def of(cls, app):
        return cls.__registry__[app]

    @classmethod
    def active(cls, context=context):
        return cls.of(context.app)

    def init_app(self, app):
        app.route(
            self.prefix + "/<path:path>", [GET, HEAD], self.serve, name=self.route_name
        )

    def add_package(self, package_name, directory, cache_max_age=None):
        """
        Add static files served from within a python package.

        Only one directory per python package may be configured using this
        method. For more flexibility use
        :meth:`fresco_static.StaticFiles.add_source`.

        :param package_name: The python package name
        :param directory: The directory within the package containing the
                          static files
        :param cache_max_age: Optional duration in seconds for the
                              Cache-Control max-age header. If omitted the
                              default value is used
        """
        self.add_source(package_name, package_name, directory, cache_max_age)

    def add_directory(self, name, directory, cache_max_age=None):
        """
        Add a directory for static files not associated with any python
        package.

        :param name: The (unique) name used to identify this source
        :param directory: Absolute path to the directory containing the
                          static files
        :param cache_max_age: Optional duration in seconds for the
                              Cache-Control max-age header. If omitted the
                              default value is used
        """
        self.add_source(name, None, directory, cache_max_age)

    def add_source(self, name, package_name, directory, cache_max_age=None):
        """
        Add a static files source directory, optionally associated with a
        python package.

        :param name: The (unique) name used to identify this source.
        :param package_name: The name of the python package containing the
                             files
        :param directory: Path to the directory containing the
                          static files. Should be relative if package_name is
                          specified, otherwise absolute.
        :param cache_max_age: Optional duration in seconds for the
                              Cache-Control max-age header. If omitted the
                              default value is used
        """
        if name in self.sources:
            raise ValueError("StaticFiles source %r is already used" % (name,))

        if package_name:
            files = resources.files(package_name)
            _mapped = {}

            def map_path(path):
                try:
                    return _mapped[path]
                except KeyError:
                    mapped = str(
                        self.file_context.enter_context(
                            resources.as_file(files.joinpath(path))
                        )
                    )
                    _mapped[path] = mapped
                    return mapped

        else:

            def map_path(path):
                return path

        static_root = map_path(directory)
        if not isdir(static_root):
            raise ValueError("%r is not a directory" % (static_root,))

        if cache_max_age:
            headers = {"Cache-Control": f"max-age: {cache_max_age}"}
        else:
            headers = {}

        self.sources[name] = (map_path, directory, gather_headers(self.headers, headers))

    def resolve_path(self, path, normpath=normpath):
        """
        Resolve ``path`` to a source and physical path if possible.

        :param path: a path of the form `<source>/<fspath>` or `<fspath>`
        :returns: a tuple of `(source, mapped_path, headers)`.
                  `source` may be `None` if no source was identified.
        """
        path = normpath(path.lstrip("/"))
        try:
            source, remaining = path.split("/", 1)
        except ValueError:
            source = None
            remaining = path

        if source and source in self.sources:
            map_path, d, headers = self.sources[source]
            path = map_path(join(d, remaining))
            return source, path, headers

        for s, p, headers in self.map_path_all_sources(path):
            if isfile(p):
                return s, p, headers

        return None, path, self.headers

    def map_path_all_sources(self, path):
        """
        Try to map ``path`` to a file in the list of configured sources.
        :return: a generator yielding mapped filesystem paths.
        """
        for s in reversed(self.sources):
            map_path, d, headers = self.sources[s]
            yield s, map_path(join(d, path)), headers

    def serve(self, path, serve_static_file=serve_static_file):
        source, fspath, headers = self.resolve_path(path)
        logger.info("Serving %r from %r", path, fspath)
        response = serve_static_file(fspath)
        if headers:
            response = response.replace(headers=response.headers + list(headers.items()))
        return response

    def pathfor(self, path):
        return self.prefix + "/" + path

    def close(self):
        """
        Clean up any filesystem resources created via importlib.resources
        """
        self.file_context.close()
