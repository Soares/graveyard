import os

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from mite.util.either import Right, Left, sets
from mite.sourcetree.tree import Tree


class TestTree(TestCase):
	def setUp(self):
		self.dirs = {
			'.': ['fileA', 'fileB', 'dir1', 'dir2'],
			'./dir1': ['file1A', 'file1B'],
			'./dir2': ['file2A', 'file2B'],
		}
		self.filemap = {
			'./fileA', './fileB',
			'./dir1/file1A', './dir1/file1B',
			'./dir2/file2A', './dir2/file2B',
		}
		self.dirmap = {'.', './dir1', './dir2'}
		self.tree = Tree()

	@patch('os.path.isfile')
	@patch('os.path.isdir')
	@patch('os.listdir')
	@patch('os.path.getmtime')
	def test_walk(self, getmtime, listdir, isdir, isfile):
		listdir.side_effect = lambda p: self.dirs[p]
		getmtime.side_effect = lambda _: 0.0
		isdir.side_effect = lambda d: d in self.dirmap
		isfile.side_effect = lambda f: f in self.filemap

		walker = self.tree.walk('.')
		self.assertEqual(next(walker), Right('./fileA'))
		os.listdir.assert_called_with('.')
		os.path.isfile.assert_called_with('./fileA')
		os.path.getmtime.assert_called_with('./fileA')
		self.assertEqual(self.tree['fileA'], 0.0)
		self.assertEqual(next(walker), Right('./fileB'))
		self.assertEqual(next(walker), Right('./dir1/file1A'))
		self.assertEqual(next(walker), Right('./dir1/file1B'))
		self.assertEqual(next(walker), Right('./dir2/file2A'))
		self.assertEqual(next(walker), Right('./dir2/file2B'))
		self.assertRaises(StopIteration, next, walker)
		self.tree.commit()

		# Nothing has changed.
		self.assertEqual(set(self.tree.walk()), set())

		def change_fileA(p):
			return 10.0 if p == './fileA' else 0.0
		getmtime.side_effect = change_fileA

		# File A has changed.
		isfileA = lambda f: f == 'fileA'
		self.assertEqual(set(self.tree.walk(ignore=isfileA)), set())
		self.tree.commit()
		self.assertEqual(set(self.tree.walk()), {Right('./fileA')})
		self.tree.commit()
		self.assertEqual(self.tree['fileA'], 10.0)
		self.assertEqual(self.tree['fileB'], 0.0)

		# Everything except File A has changed!
		os.path.getmtime.side_effect = lambda _: 10.0
		# dir1 has had all its contents removed!
		self.dirs['./dir1'] = []
		# dir2 has become a file!
		del self.dirs['./dir2']
		self.dirmap.remove('./dir2')
		self.filemap.add('./dir2')

		walker = self.tree.walk()
		removed, changed = sets(self.tree.walk())
		self.tree.commit()
		self.assertEqual(removed, {
			'./dir1/file1B', './dir1/file1A',
			'./dir2/file2B', './dir2/file2A',
		})
		self.assertEqual(changed, {'./fileB', './dir2'})


if __name__ == '__main__':
	main()
