from utilities.itertools import take

def scruncher(get_affected, direction):
	def scrunch_group(group, initial, shift, scale):
		amount = initial
		group = list(group)
		for index, next in enumerate(group):
			if amount <= 0:
				return amount
			space = next.hspace()
			if not space:
				continue
			delta = min(space, amount)
			scale(next, -delta)
			for g in get_affected(group, index):
				shift(g, delta * direction)
			amount -= space
		return initial - amount
	return scrunch_group

scrunch_left = scruncher(lambda g, i: g[:i], -1)
scrunch_right = scruncher(lambda g, i: g[:i], 1)
shift_left = scruncher(lambda g, i: g[i:], 1)
shift_right = scruncher(lambda g, i: g[i:], -1)

def divide(amount, among):
	counts = list(among)
	count = sum(counts)
	base = amount // count
	extra = amount % count
	given = (base + (1 if i < extra else 0) for i in range(count))
	for num in counts:
		yield sum(take(num, given))
