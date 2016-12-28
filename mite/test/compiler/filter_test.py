import logging

from unittest import TestCase, main
from unittest.mock import MagicMock, patch, ANY

from mite.compiler import filter
from mite import color


@patch('logging.warning', autospec=logging.warning)
class FilterTest(TestCase):
	def test_simple(self, warning):
		f = filter.module_url('/base', '.html', {
			'/base/cat.html', '/base/rat.other'})
		self.assertEquals(f('cat'), '/base/cat.html')
		self.assertEquals(f('cat.html'), '/base/cat.html')
		self.assertEquals(f('/cat'), '/base/cat.html')
		self.assertEquals(f('rat'), '/base/rat.html')
		warning.assert_called_with(
				color.color('STUB: /base/rat.html', color.RED))
		self.assertEquals(f('rat.other'), '/base/rat.other')
		self.assertEquals(f('dog'), '/base/dog.html')
		warning.assert_called_with(
				color.color('STUB: /base/dog.html', color.RED))

	def test_attributed(self, warning):
		f = filter.module_context('/house', '.html', {
			'/house/sleeping/cat.html': {'says': 'meow'}
		})
		self.assertEquals(f('sleeping/cat'), '/house/sleeping/cat.html')
		self.assertEquals(f('sleeping/cat', 'says'), 'meow')
		self.assertIsNone(f('sleeping/dog', 'says'))
		warning.assert_called_with(
				color.color('STUB: /house/sleeping/dog.html', color.RED))


if __name__ == '__main__':
	main()
