import os
import shutil
import subprocess
from unittest import TestCase, main
from unittest.mock import MagicMock, patch, call, ANY
import mite.config
import mite.compiler.loader
import mite.sourcetree.crawler
import mite.action.base
import mite.action.clean
import mite.action.build
import mite.action.serve
import mite.action.push
import mite.util.input

class ActionTest(TestCase):
	def setUp(self):
		self.patchers = {p: patch(p) for p in {
				'os.path.isdir',
				'os.makedirs',
				'mite.compiler.loader.Loader',
				'mite.sourcetree.crawler.Crawler'}}
		self.addCleanup(lambda: [p.stop() for p in self.patchers.values()])
		for p in self.patchers.values():
			p.start()

		os.path.isdir.return_value = True

		self.env = None
		self.mockler = MagicMock()
		def saveenv(**kwargs):
			self.env = kwargs['environment']
			return self.mockler
		mite.sourcetree.crawler.Crawler.side_effect = saveenv

		self.mockule = MagicMock()
		self.mockule.name = 'mockule'
		self.mockule.globals.return_value = {'mockule': 'mockule'}
		self.mockule.filters.return_value = {'mockule': lambda _: 'mockule'}

		loadermock = MagicMock()
		mite.compiler.loader.Loader.return_value = loadermock
		loadermock.load = MagicMock(return_value=self.mockule)

		self.config = mite.config.Config({
			'site': {
				'build': '.mybuild',
				'cache': '.mycache',
				'globals': {'sitevar': 'sitevar'},
				'delay': 100,
			},
			'module': True,
		})

	def test_build_directories(self):
		crawler = mite.action.base.crawler(self.config, 1025)
		os.makedirs.assert_has_calls([
			call('.mybuild', exist_ok=True),
			call('.mycache', exist_ok=True)], any_order=True)

	def test_register_modules(self):
		crawler = mite.action.base.crawler(self.config, 1025)
		self.mockler.register.assert_called_with('mockule', self.mockule)

	def test_env_context(self):
		crawler = mite.action.base.crawler(self.config, 1025)
		self.assertIsNotNone(self.env)
		tcheck = self.env.from_string(
			'{{sitevar}} {{mockule}} {{None|mockule}}').render()
		self.assertEqual(tcheck, 'sitevar mockule mockule')

	def moction(self, cls, *args, **kwargs):
		action = cls('test', *args, **kwargs)
		action.enter = MagicMock()
		action.configure = MagicMock(return_value=self.config)
		return action

	@patch('mite.util.input.confirm')
	@patch('shutil.rmtree')
	def test_clean(self, rmtree, confirm):
		self.moction(mite.action.clean.Action, 'clean').execute()
		confirm.assert_called_once_with(ANY, default=True)
		rmtree.assert_has_calls([
			call('.mybuild', True),
			call('.mycache', True)], any_order=True)

	@patch('mite.util.input.confirm')
	@patch('shutil.rmtree')
	def test_clean(self, rmtree, confirm):
		self.moction(mite.action.clean.Action, 'clean', '--force').execute()
		assert not confirm.called
		rmtree.assert_has_calls([
			call('.mybuild', True),
			call('.mycache', True)], any_order=True)

	def test_build(self):
		self.moction(mite.action.build.Action, 'build').execute()
		self.mockler.build.assert_called_once_with()

	@patch('os.path.exists')
	@patch('subprocess.check_output')
	@patch('subprocess.check_call')
	@patch('mite.action.push.current_branch_or_die')
	def test_push(self, getbranch, checkcall, checkout, exists):
		exists.side_effect = lambda f: not f.startswith('.git')
		getbranch.return_value = 'current'
		checkout.return_value = '12345'.encode('utf-8')
		self.moction(mite.action.push.Action, 'push', 'mybranch').execute()
		checkout.assert_called_once_with([
			'git',
			'commit-tree', 'current^{tree}:.mybuild',
			'-m', ANY])
		checkcall.assert_called_once_with([
			'git',
			'update-ref', 'refs/heads/mybranch', '12345'])

	@patch('os.chdir')
	@patch('socketserver.TCPServer')
	def test_serve(self, server, chdir):
		handler = MagicMock()
		self.mockler.watch.side_effect=KeyboardInterrupt
		server.return_value = handler
		self.moction(mite.action.serve.Action, 'serve').execute()
		server.assert_called_once_with(
				('localhost', 1025), ANY, bind_and_activate=False)
		self.mockler.watch.assert_called_once_with(100)
		self.mockler.stop.assert_called_once_with()


if __name__ == '__main__':
	main()
