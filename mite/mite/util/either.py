"""Basically haskell's either.."""
from abc import ABCMeta
from functools import partial


class Either(metaclass=ABCMeta):
	"""Coproduct."""
	right = property(lambda self: False)
	left = property(lambda self: False)

	def __init__(self, value):
		self.__value = value

	def __call__(self):
		return self.__value

	def __eq__(self, other):
		if not isinstance(other, Either):
			return False
		return (self.left == other.left) and self() == other()

	def __hash__(self):
		return hash((self.left, self()))

	def __repr__(self):
		return '{}({})'.format(self.__class__.__name__, self())


class Left(Either):
	"""
	Left coproduct. Usually the less common / "bad" one.

	>>> Left(1)
	Left(1)
	>>> Left(1).left
	True
	>>> Left(1).right
	False
	>>> Left(1)()
	1
	"""
	left = property(lambda self: True)



class Right(Either):
	"""
	Right coproduct. Usually the more common / "good" one.

	>>> Right(10)
	Right(10)
	>>> Right(10).left
	False
	>>> Right(10).right
	True
	>>> Right(10)()
	10
	"""
	right = property(lambda self: True)


def rights(eithers):
	"""
	Get all the rights from an iterable.

	>>> list(rights((Right(0), Left(1), Right(2), Left(3))))
	[0, 2]
	"""
	return (either() for either in eithers if either.right)


def lefts(eithers):
	"""
	Get all the lefts from an iterable.

	>>> list(lefts((Right(0), Left(1), Right(2), Left(3))))
	[1, 3]
	"""
	return (either() for either in eithers if either.left)


def partitioner(empty, add, eithers):
	"""
	Partition an either iterable into two collections.
	'empty' is used to generate an empty collection, 'add' is used to add to it.

	>>> eithers = [Right(0), Left(1), Right(2), Left(3)]
	>>> partitioner(list, list.append, eithers)
	([1, 3], [0, 2])
	>>> partitioner(set, set.add, eithers) == ({1, 3}, {0, 2})
	True
	"""
	lefts, rights = empty(), empty()
	for either in eithers:
		add(rights if either.right else lefts, either())
	return lefts, rights


partition = partial(partitioner, list, list.append)
sets = partial(partitioner, set, set.add)
