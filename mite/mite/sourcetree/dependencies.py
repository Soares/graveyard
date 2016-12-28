"""
Easy dependency management.
You put "file -> files it depends upon" into the dependency manager,
and you get "file -> files that depend upon it" out.
"""


class Graph:
	"""
	Dependency manager object.
	Saves dependencies in both directions, to allow eassy access in both the
	"file -> depends upon" and "file -> dependants" directions.
	"""

	def __init__(self):
		# dependencies is the format that is easy for them to hand us.
		# (dependant file -> files it depends upon.)
		self._dependants = {}
		# dependants is the format that is useful to us.
		# (changed file -> other files which need changing.)
		self._dependencies = {}

	def update(self, key, deps):
		"""Marks 'key' as dependant upon 'deps'."""
		self._dependencies.setdefault(key, set()).update(deps)
		for dep in self._dependencies[key]:
			self._dependants.setdefault(dep, set()).add(key)

	def __getitem__(self, key):
		"""Gets files dependant upon 'key'."""
		seen = {key}
		def dependants(current):
			children = self._dependants.get(current, set())
			for dependant in children.difference(seen):
				seen.add(dependant)
				yield dependant
				yield from dependants(dependant)
		return dependants(key)

	def __delitem__(self, key):
		"""
		Removes 'key' from dependency tracking.
		Other dependencies may still depend upon 'key', but 'key' will no
		longer depend upon anything.
		"""
		if key not in self._dependencies:
			return
		for dep in self._dependencies[key]:
			assert dep in self._dependants
			assert key in self._dependants[dep]
			self._dependants[dep].remove(key)
		del self._dependencies[key]
