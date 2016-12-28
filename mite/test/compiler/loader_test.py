import os
import imp

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from mite import Misconfigured
from mite.compiler import Loader, Copier, Flow

class TestLoader(TestCase):
	def setUp(self):
		self.patchers = {p: patch(p) for p in {
				'imp.load_source',
				'os.path.isdir',
				'os.path.exists'}}
		self.addCleanup(lambda: [p.stop() for p in self.patchers.values()])
		for p in self.patchers.values():
			p.start()

		os.path.isdir.return_value = True
		os.path.exists.return_value = True
		self.fakemodule = MagicMock()
		self.fakemodule.Compiler = MagicMock()
		self.custom = MagicMock()
		self.fakemodule.Compiler.return_value = self.custom
		imp.load_source.return_value = self.fakemodule
		self.loader = Loader('flow', 'compilers')

	def test_get_builtin_compiler(self):
		self.assertEquals(self.loader.compiler('flow', None), Flow)

	def test_get_existing_compiler(self):
		self.assertEqual(
				self.loader.compiler('preferred', 'module'),
				self.fakemodule.Compiler)
		imp.load_source.assert_called_once_with(
				'mite.compiler.preferred', 'compilers/preferred.py')

	def test_get_module_compiler(self):
		os.path.exists.side_effect = lambda f: f == 'compilers/module.py'
		self.assertEqual(
				self.loader.compiler(None, 'module'),
				self.fakemodule.Compiler)
		imp.load_source.assert_called_once_with(
				'mite.compiler.module', 'compilers/module.py')

	def test_get_fallback_compiler(self):
		os.path.exists.return_value = False
		self.assertEqual(self.loader.compiler(None, 'module'), Flow)

	def test_get_list_compiler(self):
		multi = self.loader.compiler(['flow', 'custom'], 'module')
		multi = multi('module', MagicMock())
		self.assertTrue(self.custom in multi.compilers)
		self.assertTrue(any(c for c in multi.compilers if isinstance(c, Flow)))

	def test_get_missing_compiler(self):
		os.path.exists.return_value = False
		self.assertRaises(
				Misconfigured, self.loader.compiler, 'preferred', 'module')


if __name__ == '__main__':
	main()
