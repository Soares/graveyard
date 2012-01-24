from ..nodes.window import Window
import exceptions

class Controller:
	new_window = lambda self, node, manager: Window(manager, *node.position)

	def manager(self, node):
		if node.manager is None:
			return None
		if getattr(node.manager, 'controller', None) == self:
			return node.manager
		return self.manager(node.manager)

	def split(self, into, node):
		newnode = node.manager.encapsulate(into, node)
		window = self.new_window(node, newnode)
		newnode.add(window)
		return newnode, window

	def select_near(self, node, direction):
		assert direction in (1, -1)
		m = self.manager(node)
		if not m:
			raise exceptions.OutOfBounds
		current = node.current()
		x, y = current.canvas.point
		x += current.position.x
		y += current.position.y
		try:
			m.select_near(x, y, direction)
		except exceptions.OutOfBounds:
			return self.select_near(m, direction)

	def __str__(self):
		return self.__class__.__name__
