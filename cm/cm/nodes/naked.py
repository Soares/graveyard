from node import Node, is_node


class Naked(Node):
    def __init__(self, *parts):
        self.parts = parts
        self.compress()

    def sections(self):
        for part in filter(is_node, self.parts):
            for s in part.sections():
                yield s

    def subparse(self, parse):
        from string import String
        def subparse(all, bit):
            if isinstance(bit, String):
                return all + bit.subparse(parse).parts
            all.append(bit)
            return all
        self.parts = list(reduce(subparse, self.parts, []))
        self.compress()

    def push(self, bit):
        self.parts.append(bit)
        self.compress()

    def insert(self, bit):
        self.parts.insert(0, bit)
        self.compress()

    def compress(self):
        def join(all, next):
            if not all:
                return [next]
            if isinstance(next, str) and isinstance(all[-1], str):
                all[-1] += next
            else:
                all.append(next)
            return all
        self.parts = list(reduce(join, self.parts, []))

    def __len__(self):
        return len(self.parts)

    def children(self):
        return self.parts

    def evaluate(self, settings):
        return reduce(lambda r, n: r + str(settings.eval(n)), self.parts, '')
