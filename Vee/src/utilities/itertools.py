def naturals(start=0):
	i = start
	while True:
		yield i
		i += 1


def posints():
	return naturals(start=1)


def take(n, list):
	iterator = iter(list)
	for _ in range(n):
		yield next(iterator)
