"""
A iterator reader that keeps a cache and can backstep.

>>> s = Stream([1, 2, 3, 4, 5])
>>> s.next()
1
>>> s.next()
2
>>> s.backstep(2)
>>> s.next()
1
>>> s.next()
2
>>> s.backstep()
>>> s.next()
2
>>> s.next()
3
"""
class Stream(object):
    def __init__(self, lines):
        self.pointer = 0
        self.cache = []
        self.lines = iter(lines)

    def next(self):
        if self.pointer:
            self.pointer -= 1
            return self.cache[-(self.pointer+1)]
        self.cache.append(self.lines.next())
        return self.cache[-1]

    def backstep(self, steps=1):
        self.pointer += steps
