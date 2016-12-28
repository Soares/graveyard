"""Source tree management."""
import os

from mite.util.either import Right, Left


class Tree:
	"""A source tree handler."""

	def __init__(self):
		self._children = {}
		self._pending = {}

	def __contains__(self, child):
		return child in self._pending or child in self._children

	def __iter__(self):
		keys = set(self._pending)
		keys.update(self._children)
		return iter(keys)

	def __getitem__(self, child):
		"""
		Returns the subtree at 'child' if 'child' is a directory.
		Returns None if 'child' is a file.
		Raises KeyError if 'child' is not in the tree.
		"""
		return self._pending.get(child, self._children.get(child))

	def __setitem__(self, child, value):
		"""Sets a child to a value."""
		assert isinstance(value, (float, Tree))
		self._pending[child] = value

	def __delitem__(self, child):
		"""Removes 'child' from the tree."""
		if child in self._pending:
			del self._pending[child]
		if child in self._children:
			del self._children[child]

	def get(self, child, default=False):
		"""
		Get the subtree/mtime beneath 'child' without complaining.
		Returns a float (mtime) if the chidl exists and is a file.
		Returns a subtree if child exists and is a directory.
		Returns default (False) if child does not exist.
		"""
		return self[child] if child in self else default

	def leaves(self, root):
		"""Flattens out the tree, yielding paths rooted in root."""
		for child in self:
			path = os.path.join(root, child)
			if self.hasfile(child):
				yield path
			else:
				yield from child.leaves(path)

	def noneof(self, children):
		"""Elements in the tree not in the given children iterable."""
		return set(self).difference(children)

	def hasfile(self, child):
		"""Whether the child exists and describes a file."""
		return child in self and isinstance(self[child], float)

	def hasdir(self, child):
		"""Whether the child exists and describes a directory."""
		return child in self and isinstance(self[child], Tree)

	def markfile(self, child, mtime):
		"""
		Marks 'child' as a file last changed at 'mtime'.
		Returns the old value of 'child'.
		"""
		self._pending[child] = mtime
		return self._children.get(child)

	def markdir(self, child):
		"""
		Marks 'child' as a directory last changed at 'mtime'.
		Re-uses the existing directory if it exists.
		Returns 'True' if 'child' used to be a file.
		"""
		old = self.get(child)
		self._pending[child] = old if isinstance(old, Tree) else Tree()
		return not isinstance(old, Tree)

	def walk(self, root='.', ignore=None):
		"""
		Walks the tree, yielding files that have changed or been removed.
		Paths are yielded relative to root. Changed files are Right, removed
		files are Left (see mite.either). mtime is used to determine if
		a change has occured (see os.path.getmtime). Unchanged directories are
		not visited.
		"""
		assert os.path.isdir(root), '{} is not a directory'.format(root)
		self._pending = {}
		ignore = ignore or (lambda f: False)
		children = [child for child in os.listdir(root) if not ignore(child)]
		for child in children:
			path = os.path.join(root, child)
			if os.path.isfile(path):
				mtime = os.path.getmtime(path)
				if self.hasfile(child) and self[child] == mtime:
					continue
				if self.hasdir(child):  # It used to be a directory!
					yield from map(Left, self[child].leaves(path))
				self[child] = mtime
				yield Right(path)  # This files has been changed.
			else:
				if self.hasfile(child):  # File turned into directory.
					yield Left(path)
				if not self.hasdir(child):  # New directory.
					self[child] = Tree()
				yield from self[child].walk(path)
		for removed in self.noneof(children):
			path = os.path.join(root, removed)
			if ignore(removed):
				continue
			elif self.hasfile(removed):
				yield Left(path)
			else:
				yield from map(Left, self[removed].leaves(path))
			del self[removed]

	def commit(self):
		self._children.update(self._pending)
		self._pending = {}
		for child in self:
			if isinstance(self[child], Tree):
				self[child].commit()
