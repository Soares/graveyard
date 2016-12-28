from unittest import TestCase, main
from unittest.mock import MagicMock, patch, call

from mite.sourcetree.views import FileKnowing


class FileKnowingTest(TestCase):
	def test_knowing(self):
		view = FileKnowing(
				extension='.html',
				destroot='outdir',
				builddir='.build/',
				sourceroot='indir',
				sourcepath='indir/myfile.markdown')
		self.assertEqual(view.source, 'indir/myfile.markdown')
		self.assertEqual(view.destination, '.build/outdir/myfile.html')
		self.assertEqual(view.url, '/outdir/myfile.html')
		self.assertEqual(view.sourcext, '.markdown')
		self.assertEqual(view.destext, '.html')
		other = view.neighbor('nested/other.md')
		self.assertEqual(other.source, 'indir/nested/other.md')
		self.assertEqual(other.destination, '.build/outdir/nested/other.html')

	def test_noext(self):
		view = FileKnowing(
				extension=None,
				destroot='outdir',
				builddir='.build/',
				sourceroot='indir',
				sourcepath='indir/myfile.markdown')
		self.assertEqual(view.sourcext, view.destext)


if __name__ == '__main__':
	main()
