import functools


@functools.total_ordering
class cistr(str):
    """
    String that is case insensitive for comparison / hashing
    """

    def __eq__(self, other):
        try:
            return self.casefold() == other.casefold()
        except Exception:
            return super(self).__eq__(self, other)

    def __le__(self, other):
        try:
            return self.casefold() < other.casefold()
        except Exception:
            return super(self).__eq__(self, other)

    def __hash__(self):
        return hash(self.casefold())
