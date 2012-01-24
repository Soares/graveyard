from cm.library import Library
from cm.elements import Element
from cm import ConversionError
library = Library()


@library.register('internal')
class Internal(Element):
    arguments = 'action',

    def setup(self):
        self.attributes.setdefault('method', []).append('post')
        self.body = self.cm.join(('{%csrf_token%}', self.body))
        self.tag = 'form'


@library.register('section')
class Section(Element):
    def setup(self):
        try:
            title, self.args = self.args[0], self.args[1:]
        except IndexError:
            raise ConversionError('You must give a title to section elements')
        self.tag = 'fieldset'
        self.body = self.cm.converter.render('parts/section', {
            'title': title,
            'body': self.body
        })
        self.attributes.setdefault('class', []).append('section')


@library.register('goto')
class Goto(Element):
	def setup(self):
		try:
			object, self.args = self.args[0], self.args[1:]
		except IndexError:
			raise ConversionError('You must give an object to goto elements')
		self.tag = 'a'
		if not self.body:
			self.body = '{{%s}}' % object
		self.attributes.setdefault('href', []).append('{{%s.get_absolute_url}}' % object)


@library.register('url')
class Url(Element):
	def setup(self):
		try:
			view, self.args = self.args[0], self.args[1:]
		except IndexError:
			raise ConversionError('You must give a view to url elements')
		self.tag = 'a'
		self.attributes.setdefault('href', []).append('{%% url %s %%}' % view)
