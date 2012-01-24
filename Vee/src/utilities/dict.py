def combine(*dicts):
	new = {}
	for dict in dicts:
		new.update(dict)
	return new
