from .dispatch import Signal

splitting = Signal('manager', 'node')
split = Signal('manager', 'node')

closing = Signal('manager', 'node')
closed = Signal('manager')

selecting = Signal('manager', 'node')
selected = Signal('manager', 'node')

moving = Signal('manager', 'node', 'initial', 'destination')
moved = Signal('manager', 'node', 'initial', 'destination')

refreshing = Signal('instance')
refreshed = Signal('instance')
