import os

from unittest import TestCase, main
from unittest.mock import MagicMock, patch, call

from mite import config
import mite.compiler

class ConfigTest(TestCase):
	def setUp(self):
		self.patchers = {p: patch(p) for p in {
				'os.path.isdir',
				'mite.compiler.loader.Loader'}}
		self.addCleanup(lambda: [p.stop() for p in self.patchers.values()])
		for p in self.patchers.values():
			p.start()
		os.path.isdir.return_value = True

	def test_site_vars(self):
		conf = config.Config({'site': {
				'build': '.mybuild',
				'cache': '.mycache',
				'templates': 'mytemplates',
				'compilers': 'mycompilers',
				'delay': 1,
				'lag': 1,
				'compiler': 'mydefault',
				'globals': {'key': 'value'}}})
		self.assertEqual(conf.builddir, '.mybuild')
		self.assertEqual(conf.cachedir, '.mycache')
		self.assertEqual(conf.templatedir, 'mytemplates')
		self.assertEqual(conf.delay, 1)
		self.assertEqual(conf.lag, 1)
		self.assertEqual(conf.globals, {'key': 'value'})
		mite.compiler.loader.Loader.assert_called_once_with(
				'mydefault', 'mycompilers')

	def test_load_modules(self):
		loader = MagicMock()
		mite.compiler.loader.Loader.return_value = loader
		conf = config.Config({'a': True, 'b': True})
		loader.load.assert_has_calls(
				(call('a', {'to': 'a'}), call('b', {'to': 'b'})),
				any_order=True)

	def test_module_config_dict(self):
		self.assertEquals(
				config.module_config_dict('a', True),
				{'to': 'a'})
		self.assertEquals(
				config.module_config_dict('a', 'flow to A'),
				{'compiler': 'flow', 'to': 'A'})
		conf = {'compiler': 'flow', 'to': 'bar'}
		self.assertEquals(config.module_config_dict('a', conf), conf)


if __name__ == '__main__':
	main()
