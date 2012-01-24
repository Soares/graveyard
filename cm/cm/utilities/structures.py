"""
The code in this module contains modified code from the django codebase.
As such, the license for the following code uses the django license.
Please see LICENSE.txt in the root of the project for details.
"""

class StackDictPopException(Exception):
    pass

class StackDictNoPrevious(Exception):
    pass


class StackDict(object):
    def __init__(self, **kwargs):
        self.dicts = [kwargs]

    def __repr__(self):
        return repr(self.dicts)

    def __iter__(self):
        for d in self.dicts:
            yield d

    def push(self):
        self.dicts = [{}] + self.dicts
        return self.dicts[0]

    def pop(self):
        if len(self.dicts) == 1:
            raise StackDictPopException
        return self.dicts.pop(0)

    def __setitem__(self, key, value):
        self.dicts[0][key] = value

    def __getitem__(self, key):
        for d in self.dicts:
            if key in d:
                return d[key]
        raise KeyError(key)

    def __delitem__(self, key):
        del self.dicts[0][key]

    def has_key(self, key):
        for d in self.dicts:
            if key in d:
                return True
        return False

    __contains__ = has_key

    def get(self, key, otherwise=None):
        for d in self.dicts:
            if key in d:
                return d[key]
        return otherwise

    def setdefault(self, key, default):
        for d in self.dicts:
            if key in d:
                return d[key]
        self[key] = default
        return default

    def update(self, other_dict):
        """Pushes an entire dictionary's keys and values onto the context."""
        if not hasattr(other_dict, '__getitem__'):
            raise TypeError('other_dict must be a mapping (dictionary-like) object.')
        self.dicts.insert(0, other_dict)
        return other_dict

    def previous(self):
        if len(self.dicts) > 1:
            return self.dicts[1]
        raise StackDictNoPrevious


class ListDict(object):
    def __init__(self, *tuples):
        self._dict = {}
        for (name, value) in tuples:
            self.add(name, value)

    def add(self, name, value):
        self._dict.setdefault(name, []).append(value)

    def lists(self):
        return self._dict.values()

    def items(self):
        for (k, vs) in self._dict.items():
            for v in vs:
                yield (k, v)

    def dict(self):
        return dict(self._dict)

    def __iter__(self):
        return iter(self._dict)
