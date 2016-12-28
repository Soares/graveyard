import os
import jinja2
import subprocess

from unittest import TestCase, main
from unittest.mock import MagicMock, patch, ANY
from mite.util.either import Right, Left

from mite import Misconfigured
from mite import refresher
from mite.sourcetree import crawler
from mite.sourcetree import tree
from mite.sourcetree import views


class TestCrawler(TestCase):
	def setUp(self):
		self.environment = MagicMock(spec=jinja2.Environment)
		self.refresher = MagicMock(spec=refresher.Refresher)

		self.patchers = {p: patch(p) for p in {
				'os.path.isdir',
				'os.path.getmtime',
				'os.walk',
				'mite.sourcetree.crawler.read_cachefile',
				'mite.sourcetree.crawler.write_cachefile',
				'subprocess.Popen',
				'mite.sourcetree.tree.Tree.walk'}}
		self.patchers['subprocess.Popen'].spec = subprocess.Popen
		self.addCleanup(lambda: [p.stop() for p in self.patchers.values()])
		for p in self.patchers.values():
			p.start()

		os.path.getmtime.return_value = 'now'
		os.path.isdir.return_value = True

		def treewalk(path='.', ignore=None):
			yield Right(os.path.join(path, 'changed'))
			yield Left(os.path.join(path, 'removed'))
		tree.Tree.walk.side_effect = treewalk

		def oswalk(path):
			yield (path, ['dir'], ['top.ext'])
			yield (os.path.join(path, 'dir'), [], ['nested'])
		os.walk.side_effect = oswalk

		self.crawler = crawler.Crawler(
				'.build', '.cache', 'templates',
				self.environment, self.refresher, 0.5)
		self.views = []

	def mockule(self):
		mockule = MagicMock()
		def saveview(view):
			self.views.append(view)
		mockule.initialize.side_effect = saveview
		mockule.compile.side_effect = saveview
		mockule.remove.side_effect = saveview
		mockule.extension = '.html'
		mockule.destroot = 'out'
		return mockule

	def test_register(self):
		self.views.clear()
		mockule = self.mockule()
		# This should call us with 'top' and 'dir/nested'
		self.crawler.register('a', mockule)
		self.assertEqual(len(self.views), 2)
		self.assertEqual(self.views[0].source, 'a/top.ext')
		self.assertRaises(AttributeError, getattr, self.views[1], 'reload')

	def test_no_reregister(self):
		mockule = self.mockule()
		self.crawler.register('a', mockule)
		self.assertRaises(Misconfigured, self.crawler.register, 'a', mockule)

	def test_register_none(self):
		# Mostly tests that nobody tries to call None.initialize()
		self.crawler.register('a', None)

	def test_build(self):
		mockule = self.mockule()
		self.crawler.register('a', mockule)
		self.views.clear()
		self.crawler.build()
		self.assertEqual(len(self.views), 2)
		self.assertEqual(self.views[0].source, 'a/removed')
		self.assertEqual(self.views[1].source, 'a/changed')

	def test_init_functionality(self):
		mockule = self.mockule()
		iview = None
		def initialize(view):
			nonlocal iview
			if view.source.endswith('top.ext'):
				iview = view
		mockule.initialize.side_effect = initialize
		self.crawler.register('a', mockule)
		self.assertEqual(iview.source, 'a/top.ext')
		self.assertEqual(iview.url, '/out/top.html')
		self.assertIsNotNone(iview.read)

	def test_remove_functionality(self):
		mockule = self.mockule()
		self.crawler.register('a', mockule)
		self.views.clear()
		self.crawler.build()
		view = next(v for v in self.views if isinstance(v, views.Removing))
		self.assertEqual(view.source, 'a/removed')
		self.assertEqual(view.destination, '.build/out/removed.html')
		self.assertEqual(view.neighbor('nother').source, 'a/nother')
		self.assertIsNotNone(view.execute)
		self.assertIsNotNone(view.reload)
		self.assertIsNotNone(view.restyle)

	def test_compile_functionality(self):
		amockule = self.mockule()
		bmockule = self.mockule()
		aview = None
		def compilea(view):
			nonlocal aview
			aview = view
		amockule.compile.side_effect = compilea
		self.crawler.register('a', amockule)
		self.crawler.register('b', bmockule)
		self.views.clear()
		self.crawler.build()
		self.assertEqual(aview.source, 'a/changed')
		self.assertEqual(aview.destination, '.build/out/changed.html')
		self.assertIsNotNone(aview.neighbor)
		self.assertIsNotNone(aview.reload)
		self.assertIsNotNone(aview.restyle)
		self.assertIsNotNone(aview.execute)
		self.assertIsNotNone(aview.read)
		self.assertIsNotNone(aview.write)
		self.assertIsNotNone(aview.depend)
		self.assertEquals(aview.modules, {'a', 'b'})

	def test_refreshing(self):
		mockule = self.mockule()
		self.crawler.register('a', mockule)
		self.views.clear()
		self.crawler.build()
		view = next(v for v in self.views if isinstance(v, views.Compiling))
		view.reload()
		view.restyle()
		self.refresher.reload.assert_called_once_with(None)
		self.refresher.restyle.assert_called_once_with(None)

	def test_subprocesses(self):
		mockule = self.mockule()
		def compile_execute(view):
			view.execute(['dummy', 'process'])
		mockule.compile = MagicMock(side_effect=compile_execute)
		self.crawler.register('a', mockule)
		self.crawler.build()
		subprocess.Popen.assert_called_with(['dummy', 'process'])

	def test_silence(self):
		mockule = self.mockule()
		self.crawler.register('a', mockule)
		self.crawler.build()
		self.views.clear()
		tree.Tree.walk.side_effect = lambda _: ()
		self.crawler.build()
		self.assertEqual(len(self.views), 0)

	@patch('os.path.isfile')
	def test_rendering(self, isfile):
		isfile.side_effect = lambda t : t == 'templates/yes'
		mocklate = MagicMock()
		mocklate.render = MagicMock()
		self.environment.from_string = MagicMock(return_value=mocklate)
		mockule = self.mockule()
		def compile_render(view):
			self.assertEquals(view.environment, self.environment)
			self.assertEquals(view.template_path('foo'), 'templates/foo')
			self.assertEquals(view.pick_template('no', 'yes'), 'yes')
			view.render('foo', {'key': 'value'})
			self.environment.from_string.assert_called_once_with('foo')
			mocklate.render.assert_called_once_with({'key': 'value'})
		mockule.compile = MagicMock(side_effect=compile_render)
		self.crawler.register('a', mockule)
		self.crawler.build()
		mockule.compile.assert_called_once_with(ANY)

	def test_dependencies(self):
		amockule = self.mockule()
		bmockule = self.mockule()
		def compile_depend(view):
			if view.source == 'a/1':
				view.depend('b/2')
				view.depend('templates/a')
			if view.source == 'b/2':
				view.depend('a/3')
			self.views.append(view)
		amockule.compile = MagicMock(side_effect=compile_depend)
		bmockule.compile = MagicMock(side_effect=compile_depend)
		self.crawler.register('a', amockule)
		self.crawler.register('b', bmockule)
		self.crawler.register('templates', None)

		def walk(root, ignore=None):
			if root == 'a':
				return [Right('a/1'), Right('a/3')]
			if root == 'b':
				return [Right('b/2')]
			if root == 'templates':
				return [Right('templates/a')]
		tree.Tree.walk.side_effect = walk
		self.views.clear()
		self.crawler.build()
		self.assertIsNotNone(next(v for v in self.views if v.source == 'a/1'))
		self.assertIsNotNone(next(v for v in self.views if v.source == 'b/2'))
		self.assertIsNotNone(next(v for v in self.views if v.source == 'a/3'))
		self.assertEqual(len(self.views), 3)  # Templates is not watched.

		# Test that 1, 2, and 3 update when 3 updates.
		def walk(root, ignore=None):
			if root == 'a':
				return [Right('a/3')]
			return []
		tree.Tree.walk.side_effect = walk
		self.views.clear()
		self.crawler.build()
		self.assertIsNotNone(next(v for v in self.views if v.source == 'a/1'))
		self.assertIsNotNone(next(v for v in self.views if v.source == 'b/2'))
		self.assertIsNotNone(next(v for v in self.views if v.source == 'a/3'))
		self.assertEqual(len(self.views), 3)

		# Remove 2 and change 3: 1 no longer updates.
		def walk(root, ignore=None):
			if root == 'a':
				return [Right('a/3')]
			if root == 'b':
				return [Left('b/2')]
			return []
		tree.Tree.walk.side_effect = walk
		self.views.clear()
		self.crawler.build()
		self.assertIsNotNone(next(v for v in self.views if v.source == 'b/2'))
		self.assertIsNotNone(next(v for v in self.views if v.source == 'a/3'))
		self.assertEqual(len(self.views), 2)

		# Touch the template. Only a1 changes.
		def walk(root, ignore=None):
			if root == 'templates':
				return [Right('templates/a')]
			return []
		tree.Tree.walk.side_effect = walk
		self.views.clear()
		self.crawler.build()
		self.assertIsNotNone(next(v for v in self.views if v.source == 'a/1'))
		self.assertEqual(len(self.views), 1)

		# A stops caring about the template. Touch it again. No updates.
		amockule.compile = MagicMock()
		self.views.clear()
		self.crawler.build()
		self.assertEqual(len(self.views), 0)


if __name__ == '__main__':
	main()
