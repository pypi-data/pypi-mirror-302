import atexit
import contextlib
import functools
import mimetypes
import os
import pathlib
import tempfile
import time
import concurrent.futures
import zlib
from email.utils import formatdate, parsedate_tz, mktime_tz
from importlib import resources

import portalocker

from fresco import context
from fresco import Request
from fresco import Response
from fresco.response import STATUS_NOT_MODIFIED
from fresco_static.cistr import cistr

HeaderDict = dict[cistr, str]

# 860 bytes - fits in one packet anyway and compression overheads outweigh gains
# https://webmasters.stackexchange.com/questions/31750/
MIN_COMPRESSION_SIZE = 860

compressor_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1).__enter__()
compression_suffix = {"brotli": ".br", "gzip": ".gz"}
compression_levels = {"brotli": 11, "gzip": 9}
compression_header_keys = {"brotli": "br", "gzip": "gz"}


def serve_file(
    path: pathlib.Path | str,
    headers: dict[str | cistr, str] = {},
    compression: str | None = "brotli,gzip",
    cachedir: str | None = None,
):
    path = os.path.abspath(path)
    if compression and not cachedir:
        cachedir = tempdir()
    headers = headerdict(headers)
    content_type = headers.get(cistr("content-type"))
    if compression:
        compression_keys = {
            compression_header_keys[s.strip()]: s.strip()
            for s in compression.split(",")
        }
    else:
        compression_keys = None

    def serve_file(request=None):
        request = request or context.request
        return _serve_file(
            request, path, cachedir, headers, compression_keys, content_type
        )

    return serve_file


def serve_directory(
    dirpath: pathlib.Path | str,
    headers: dict[str | cistr, str] = {},
    compression: str | None = "brotli,gzip",
    cachedir: str | None = None,
):
    mountpoint = None
    dirpath = os.path.abspath(dirpath)
    if compression and not cachedir:
        cachedir = tempdir()
    headers = headerdict(headers)
    content_type = headers.get(cistr("content-type"))
    if compression:
        compression_keys = {
            compression_header_keys[s.strip()]: s.strip()
            for s in compression.split(",")
        }
    else:
        compression_keys = None

    def serve_directory(request=None):
        nonlocal mountpoint
        request = request or context.request
        path_info = request.path_info
        if mountpoint is None:
            mountpoint = context.route_traversal.build_path()
        path = os.path.normpath(
            os.path.join(dirpath, path_info[len(mountpoint) :].lstrip("/"))
        )
        if path[: len(dirpath)] != dirpath:
            return Response.forbidden()
        return _serve_file(
            request, path, cachedir, headers, compression_keys, content_type
        )

    return serve_directory


def serve_package_directory(
    package_name: str,
    dirpath: pathlib.Path | str,
    headers: dict[str | cistr, str] = {},
    compression: str | None = "brotli,gzip",
    cachedir: str | None = None,
):
    _context = contextlib.ExitStack()
    files = resources.files(package_name)
    mapped_dir = _context.enter_context(
        resources.as_file(files.joinpath(str(dirpath)))
    )
    atexit.register(_context.close)
    assert mapped_dir.is_dir()
    return serve_directory(mapped_dir, headers, compression, cachedir)


def _serve_file(
    request: Request,
    path: str,
    cachedir: str,
    headers: HeaderDict,
    compression_keys={},
    content_type=None,
    bufsize=8192,
    BAD_REQUEST=Response.bad_request(),
    NOT_MODIFIED=Response(status=STATUS_NOT_MODIFIED),
    FORBIDDEN=Response.forbidden(),
) -> Response:
    method = request.method
    if method not in {"GET", "HEAD"}:
        return Response.method_not_allowed()

    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return Response.not_found()

    mod_since = request.get_header("if-modified-since")
    if mod_since is not None:
        try:
            mod_since = mktime_tz(parsedate_tz(mod_since))
        except (TypeError, OverflowError, ValueError):
            return BAD_REQUEST
        if int(mtime) <= int(mod_since):
            return NOT_MODIFIED

    content_length = os.path.getsize(path)

    if content_type is None:
        content_type = mimetypes.guess_type(path)[0]
        if content_type is None:
            content_type = "application/octet-stream"

    if method == "HEAD":
        def content_iterator(f):
            return []

    else:
        file_wrapper = request.environ.get("wsgi.file_wrapper")
        if file_wrapper is not None:

            def content_iterator(f):
                return file_wrapper(f, bufsize)

        else:

            def content_iterator(f):
                while True:
                    chunk = f.read(bufsize)
                    if chunk == b"":
                        break
                    yield chunk
                f.close()

    content_encoding = None
    compressed_path = None
    if compression_keys and content_length >= MIN_COMPRESSION_SIZE:
        accept = request.get_header("accept-encoding")
        if accept:
            for scheme in parse_accept(accept):
                if scheme in compression_keys:
                    compressed_path = get_compressed_path(
                        path, mtime, cachedir, compression_keys[scheme], create=True
                    )
                    if compressed_path:
                        content_encoding = scheme
                        break

    try:
        _file = open(compressed_path or path, "rb")
    except IOError:
        return FORBIDDEN

    return Response(
        content=content_iterator(_file),
        content_length=str(
            os.path.getsize(compressed_path) if compressed_path else content_length
        ),
        last_modified=formatdate(mtime, localtime=False, usegmt=True),
        content_encoding=content_encoding,
        content_type=content_type,
        passthrough=True,
        **headers
    )


def tempdir(*args, **kwargs):
    cachedir_cm = tempfile.TemporaryDirectory(*args, **kwargs)
    cachedir = cachedir_cm.__enter__()
    atexit.register(functools.partial(cachedir_cm.__exit__, None, None, None))
    return cachedir


def get_compressed_path(
    path: str,
    mtime: float,
    cachedir: str,
    compression: str,
    create=False,
    delete_stale=True,
) -> str | None:
    """
    Return the path to a compressed copy of ``path`` from ``cachedir``.
    If it is currently being created, return None
    """
    p = os.path.join(
        cachedir, path.lstrip(os.path.sep) + compression_suffix[compression]
    )
    if os.path.exists(p):
        compressed_mtime = os.path.getmtime(p)
        if compressed_mtime == mtime:
            return p
        if delete_stale:
            os.unlink(p)
        return None
    if create:
        compressor_pool.submit(create_compressed, path, p, compression)
    return None


def create_compressed(src: str, dest: str, compression: str) -> None:
    """
    Write a compressed copy of the file in ``src`` to ``dest``.
    The mtime is copied from the original file to later help determine freshness

    The dest file is locked during the operation to prevent parallel threads
    trying to compress the same file.
    """
    bufsize = 8192
    if compression == "brotli":
        import brotli

        compressor = brotli.Compressor(quality=compression_levels[compression])
        compress = compressor.compress
        flush = compressor.finish
    elif compression == "gzip":
        compressor = zlib.compressobj(wbits=31, level=compression_levels[compression])
        compress = compressor.compress
        flush = compressor.flush
    else:
        return

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with portalocker.Lock(dest + ".lock"):
        if os.path.exists(dest):
            return
        with open(src, "rb") as src_f, open(dest, "wb") as dest_f:
            while True:
                chunk = src_f.read(bufsize)
                if chunk == b"":
                    dest_f.write(flush())
                    break
                else:
                    dest_f.write(compress(chunk))
        os.utime(dest, (time.time(), os.path.getmtime(src)))


def headerdict(headers: dict[str | cistr, str]):
    return {cistr(h): v for h, v in headers.items()}


def parse_accept(s: str) -> list[str]:
    """
    Parse an Accept-Encoding request header and return the acceptable encodings.

    The encodings are returned as an ordered list of sets
    """
    encodings = s.split(",")
    result: list[tuple[float, str]] = []
    for item in encodings:
        if ";" in item:
            enc, qual = item.split(";", 1)
            enc = enc.strip()
            q = -float(qual.split("=", 1)[1].strip())
            if q == 0:
                continue
        else:
            enc = item.strip()
            q = -1.0
        result.append((q, enc))
    result.sort()
    return [e for q, e in result]
