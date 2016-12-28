import os

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from mite.util.input import confirm


class TestConfirm(TestCase):
	def setUp(self):
		self.response = ''
		self.prompt = None
		def respond(*args, **kwargs):
			return self.response
		def set_prompt(p, *args, **kwargs):
			self.prompt = p
		if isinstance(__builtins__, dict):
			# We're being run with nose.
			__builtins__['input'] = MagicMock(side_effect=respond)
			__builtins__['print'] = MagicMock(side_effect=set_prompt)
		else:
			# We're being run as __main__.
			__builtins__.input = MagicMock(side_effect=respond)
			__builtins__.print = MagicMock(side_effect=set_prompt)

	def test_confirm_default_false(self):
		self.assertEquals(confirm(), False)

	def test_confirm_default_true(self):
		self.assertEquals(confirm(default=True), True)

	def test_confirm_respond_true(self):
		self.response = 'y'
		self.assertEquals(confirm(), True)

	def test_confirm_respond_false(self):
		self.response = 'n'
		self.assertEquals(confirm(default=True), False)

	def test_confirm_prompt(self):
		confirm('Launch the nukes?')
		self.assertTrue(self.prompt.startswith('Launch the nukes?'))


if __name__ == '__main__':
	main()
