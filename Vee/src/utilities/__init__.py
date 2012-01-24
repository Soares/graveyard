def do(fn, list):
	for _ in map(fn, list): pass


def translate(string):
	return string


def iff(object, fn, *args, **kwargs):
	return fn(object, *args, **kwargs) if object is not None else None


def laxmax(*args):
	args = [a for a in args if a is not None]
	return max(args) if args else None


def laxmin(*args):
	args = [a for a in args if a is not None]
	return min(args) if args else None


def fallback(block, exception, default):
	try:
		return block()
	except exception:
		return default


def ltz(x):
	return x < 0


def always(x):
	return lambda *args, **kwargs: x


def isclass(value):
	return isinstance(value, type)


def isfunc(value):
	return hasattr(value, '__call__') and not isclass(value)
