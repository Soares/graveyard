class OutOfBounds(Exception):
	pass


class NotEnoughSpace(Exception):
	def __init__(self, provided=None, required=None, *, missing=None, message=None):
		self.provided, self.required = provided, required
		self.missing = missing
		if missing is None and required is not None and provided is not None:
			self.missing = required - provided
		if message is not None:
			self.message = message
