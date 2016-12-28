from unittest import TestCase, main
from unittest.mock import MagicMock

from mite import refresher

class TestRefresher(TestCase):
	def setUp(self):
		refresher.execute = MagicMock()
		self.refresher = refresher.Refresher()

	def test_reload(self):
		self.refresher.reload('foo')
		self.refresher.reload('foo')
		self.refresher.execute()
		refresher.execute.assert_called_once_with(
				refresher.RELOAD, 'http://localhost:1025', 'foo')

	def test_restyle(self):
		self.refresher.restyle('foo')
		self.refresher.restyle('foo')
		self.refresher.execute()
		refresher.execute.assert_called_once_with(
				refresher.RESTYLE, 'http://localhost:1025', 'foo')

	def test_reload_beats_restyle(self):
		self.refresher.reload('foo')
		self.refresher.restyle('foo')
		self.refresher.execute()
		refresher.execute.assert_called_once_with(
				refresher.RELOAD, 'http://localhost:1025', 'foo')

	def test_restyle_all_beats_restyle_one(self):
		self.refresher.restyle()
		self.refresher.restyle('foo')
		self.refresher.restyle('bar')
		self.refresher.execute()
		refresher.execute.assert_called_once_with(
				refresher.RESTYLE, 'http://localhost:1025')

	def test_reload_all_beats_everything(self):
		self.refresher.reload()
		self.refresher.reload('foo')
		self.refresher.restyle('bar')
		self.refresher.execute()
		refresher.execute.assert_called_once_with(
				refresher.RELOAD, 'http://localhost:1025')


if __name__ == '__main__':
	main()
