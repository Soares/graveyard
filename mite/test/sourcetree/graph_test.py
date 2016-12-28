from unittest import TestCase, main

from mite.sourcetree import dependencies


class GraphTest(TestCase):
	def setUp(self):
		self.graph = dependencies.Graph()

	def test_graph(self):
		self.assertEqual(set(self.graph['a']), set())
		# Dependancies:
		# A --> B --> C
		#        \--> D --> E
		self.graph.update('a', ['b'])
		self.graph.update('b', ['c', 'd'])
		self.graph.update('d', ['e'])
		self.assertEqual(set(self.graph['a']), set())
		self.assertEqual(set(self.graph['b']), {'a'})
		self.assertEqual(set(self.graph['c']), {'a', 'b'})
		self.assertEqual(set(self.graph['d']), {'a', 'b'})
		self.assertEqual(set(self.graph['e']), {'a', 'b', 'd'})
		del self.graph['d']
		self.assertEqual(set(self.graph['e']), set())

	def test_cycle(self):
		# A -> B -> A
		self.graph.update('a', ['b'])
		self.graph.update('b', ['a'])
		self.assertEqual(set(self.graph['a']), {'b'})
		self.assertEqual(set(self.graph['b']), {'a'})


if __name__ == '__main__':
	main()
