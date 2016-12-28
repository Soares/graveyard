import os
from jinja2 import Environment, DictLoader

from unittest import TestCase, main
from unittest.mock import MagicMock, patch, call

from mite.refresher import Refresher
from mite.sourcetree.dependencies import Graph
from mite.sourcetree.views import Compiling, Initializing
from mite.compiler.flow import Flow
from mite.compiler.filter import module_url, module_context

class FlowTest(TestCase):
	def setUp(self):
		self.patchers = {p: patch(p) for p in {
				'os.path.isfile'}}
		self.addCleanup(lambda: [p.stop() for p in self.patchers.values()])
		for p in self.patchers.values():
			p.start()
		os.path.isfile.side_effect = lambda t: os.path.basename(t) in TEMPLATES

		self.module = Flow('mymodule', {
			'to': 'outdir',
			'extension': '.html',
			'context': {'modulevar': 'modulevar'},
		})
		testfile = 'test.markdown'
		self.init = Initializing(
				builddir='.build/',
				sourceroot=self.module.name,
				sourcepath=os.path.join(self.module.name, testfile),
				destroot=self.module.destroot,
				extension=self.module.extension)
		env = Environment(loader=DictLoader(TEMPLATES))
		env.filters = FILTERS
		env.globals = GLOBALS
		self.view = Compiling(
				env=env,
				modules=MODULES,
				templatedir='templates',
				builddir='.build/',
				sourceroot=self.module.name,
				sourcepath=os.path.join(self.module.name, testfile),
				destroot=self.module.destroot,
				extension=self.module.extension,
				processes=MagicMock(),
				dependencies=MagicMock(autospec=Graph),
				refresher=MagicMock(autospec=Refresher))
		self.module.render = MagicMock(side_effect=self.module.render)

	def executeTest(self, spec):
		INITIAL, *RENDERED, TEMPLATE, FINAL = spec

		# Test the entire pipeline.
		self.init.read = MagicMock(return_value=INITIAL)
		self.view.read = MagicMock(return_value=INITIAL)
		self.module.initialize(self.init)
		self.view.write = MagicMock()
		self.module.compile(self.view)
		self.view.write.assert_called_once_with(FINAL)

		# Test the intermediary templates.
		text, content = self.module.parse(INITIAL, dict(self.module.context))
		template = self.module.template_string(text, content, self.view)
		for v in RENDERED:
			self.module.render.assert_any_call(v)
		self.assertEqual(template, TEMPLATE)

	def test_simple(self):
		self.executeTest(SIMPLE)

	def test_complex(self):
		self.executeTest(BLOCKHEAD)


GLOBALS = {'sitevar': 'sitevar'}
MODULES = ['mymodule', 'coffee', 'expand']
FILTERS = {
	'coffee': module_url('/js', '.js', ['/js/test.js']),
	'link': '[{1}](/posts/{0}.html)'.format,
	'expand': module_context('/expand', '.html', {
		'/expand/u/r/l.html': {},
		'/expand/reference.html': {'attribute': 'ATTRIBUTE'},
	}),
}
TEMPLATES = {
	'mymodule.html': '{% block content %}{% endblock %}',
	'one.html': '',
	'two.custom': '',
	'custom.ext': """TITLE: {{ title }}
SCRIPTS:
{%- for script in scripts %}
{{ script }}
{% endfor -%}
CONTENT:
{% block content %}{% endblock %}
ALPHA:
{% block alpha %}{% endblock %}""",
}


SIMPLE = (
"""Flow""",
"""Flow""",
"""{%- extends "mymodule.html" -%}
{%- block content -%}
Flow
{%- endblock content -%}""",
'Flow')


BLOCKHEAD = (
"""---
title: Block Head
blocks:
  alpha: |
    This is block alpha.
    It has an @expand/u/r/l.
scripts:
- '@coffee/test'
macros:
- one
- two.custom
layout: custom.ext
---
The body with an @expand.attribute/reference!
And a @link[My Title]post/url.
It also references {{ scripts[0] }}.
And {{ sitevar }} and {{ modulevar }}.""",

"""The body with an ATTRIBUTE!
And a [My Title](/posts/post/url.html).
It also references /js/test.js.
And sitevar and modulevar.""",

"""This is block alpha.
It has an /expand/u/r/l.html.""",

"""{%- extends "custom.ext" -%}
{%- block content -%}
The body with an ATTRIBUTE!
And a [My Title](/posts/post/url.html).
It also references /js/test.js.
And sitevar and modulevar.
{%- endblock content -%}
{%- block alpha -%}
This is block alpha.
It has an /expand/u/r/l.html.
{%- endblock alpha -%}""",

"""TITLE: Block Head
SCRIPTS:
/js/test.js
CONTENT:
The body with an ATTRIBUTE!
And a [My Title](/posts/post/url.html).
It also references /js/test.js.
And sitevar and modulevar.
ALPHA:
This is block alpha.
It has an /expand/u/r/l.html.""")


if __name__ == '__main__':
	main()
