"""Flow: Jinja + Yaml"""
import jinja2
import logging
import os
import re
import yaml

from mite.compiler.jinja import Dynamic

class Flow(Dynamic):
	"""Compiles files using flow."""

	extension = 'html'

	def parse(self, text, context):
		if text.startswith('---\n'):
			header, content = text[4:].split('\n---\n', 1)
			return content, update_context(context, yaml.load(header))
		return text, context

	def publish(self, context):
		return context.get('published', True)

	def template_string(self, text, context, view):
		renderer = lambda content: view.render(content, context)
		# Blocks will be expanded at the same time as content.
		blocks = context.pop('blocks', {})
		# Expand all of the template context valiables.
		# (Someone might have 'scripts: @stylus/main' in their yaml)
		# Jinja will be used to expand these.
		for key, value in context.items():
			context[key] = self.expand_value(value, renderer)
		# Let Flow extenders alter the page context.
		self.contextualize(context, view)
		# Guess what template they want to extend; start the template with that.
		layout = context.get('layout', self.template)
		template = jinja_extend(self.select_template(view, layout))
		# Include all of the jinja macro files that they listed.
		macros = ''.join(jinja_import(self.select_template(view, i))
			for i in context.pop('macros', []))

		# We need to stick the remaining content into jinja blocks.
		# We allow Flow extenders to pre-render using programs such as markdown.
		# We must render each block individually (instead of rendering the
		# final template) because the template will be littered with jinja
		# block/extend tags that will likely confuse the renderer.
		# For the same reason we must render each block using jinja before
		# passing it to the internal renderer because the jinja macros / links
		# may confuse the internal renderer.
		def put_into_block(blocktext, blockname):
			"""
			Puts the text into a jinja block of the appropriate name.
			The text will be rendered into the right type for the jinja tempate.
			(Markdown will be rendered to html, etc.)
			"""
			logging.debug('@@@@@@@@ FLOWING %s @@@@@@@@' % blockname)
			logging.debug(blocktext.rstrip('\n'))
			blocktext = self.render(renderer(flow_expand(blocktext)))
			return BLOCK_TAG.format(name=blockname, block=blocktext)

		# Every block has access to the included macros.
		template += put_into_block(macros + text, DEFAULT_BLOCK)
		for name, block in blocks.items():
			template += put_into_block(macros + block, name)
		# BLOCK_TAG and EXTEND_TAG always add a trailing newline.
		return template.rstrip('\n')

	def select_template(self, view, template):
		"""
		Gets the template that a page should extend.
		The template file will be looked for as is and with all combinations of
		page input/output extensions.
		"""
		if not template:
			return None
		template = view.pick_template(
				template,
				# page.md extending "base" meaning "base.md"
				template + view.sourcext,
				# page.md extending "base" meaning "base.html"
				template + view.destext,
				# page.md extending "base" meaning "base.md.html"
				# read "turning markdown into hmtl"
				template + view.sourcext + view.destext,
				# page.md extending "base" meaning "base.html.md"
				# read "generating html with markdown syntax"
				template + view.destext + view.sourcext)
		view.depend(view.template_path(template))
		return template

	def expand_value(self, value, renderer):
		"""Expand @links into {{ 'filters'|module('attribute') }}."""
		if isinstance(value, list):
			return [self.expand_value(item, renderer) for item in value]
		if isinstance(value, set):
			return {self.expand_value(item, renderer) for item in value}
		if isinstance(value, dict):
			return {k: self.expand_value(v, renderer) for k, v in value.items()}
		if isinstance(value, str):
			return renderer(flow_expand(value))
		return value

	def contextualize(self, data, view):
		"""Adds to the context."""
		return data

	def render(self, text):
		"""Renders the text."""
		return text


def update_context(context, config):
	"""
	Updates a page context (which is loaded with the module configuration)
	with a page configuration (from a flow header).
	Lists/sets are extended, dicts are updated, everything else is clobbered.
	"""
	for key, value in config.items():
		if key not in context:
			context[key] = value
		elif isinstance(value, set):
			context[key] = value.union(context[key])
		elif isinstance(value, list):
			context[key] += value
		elif isinstance(value, dict):
			context[key].update(value)
		else:
			context[key] = value
	return context


def jinja_quote(string):
	"""
	Quotes a string for use in a jinja variable expansion.

	>>> jinja_quote('Foo')
	'"Foo"'
	>>> jinja_quote('She said "hello"')
	'"She said \\\\"hello\\\\""'

	"""
	return '"{}"'.format(string.replace('"', r'\"'))


def flow_expansion(function, first, second=None):
	"""
	The jinja filter from a flow expansion.

	>>> flow_expansion('posts', 'path/to/the/post', 'title')
	'{{ "path/to/the/post"|posts("title") }}'
	>>> flow_expansion('posts', 'my/url', 'attribute')
	'{{ "my/url"|posts("attribute") }}'
	>>> flow_expansion('posts', 'url/with/"quotes"-in-it')
	'{{ "url/with/\\\\"quotes\\\\"-in-it"|posts }}'

	"""
	first = jinja_quote(first)
	if second is not None:
		return '{{ %s|%s(%s) }}' % (first, function, jinja_quote(second))
	return '{{ %s|%s }}' % (first, function)


def flow_expand(string):
	"""
	Wrapper around flow_expand suitable for regex.sub with FLOW_BUILDER.

	>>> flow_expand('''
	... See here: @link[My Title]some/url
	... Styled like @coffee/nested/test.coffee.
	... See also @posts.title/my/post!
	... ''') == '''
	... See here: {{ "some/url"|link("My Title") }}
	... Styled like {{ "nested/test.coffee"|coffee }}.
	... See also {{ "my/post"|posts("title") }}!
	... '''
	True
	"""
	def sub(match):
		function, dotattr, brakattr, path = match.groups()
		if brakattr:
			brakattr = re.sub(r'\\([\\\]])', r'\1', brakattr)
		assert not (dotattr and brakattr)
		return flow_expansion(function, path, dotattr or brakattr)
	return FLOW_EXPANSION.sub(sub, string)


def jinja_extend(template):
	"""
	Creates a jinja {% extends %} tag for the given template.

	>>> jinja_extend(None)
	''
	>>> jinja_extend('base.html')
	'{%- extends "base.html" -%}\\n'

	"""
	return EXTEND_TAG.format(extend=jinja_quote(template)) if template else ''


def jinja_import(template):
	"""
	Creates a jinja {% import %} tag for the given template.

	>>> jinja_import(None)
	''
	>>> jinja_import('macros.html')
	'{%- import "macros.html" as macros -%}\\n'
	"""
	return IMPORT_TAG.format(
			template=jinja_quote(template),
			name=os.path.splitext(template)[0],
	) if template else ''


EXTEND_TAG = '{{%- extends {extend} -%}}\n'
IMPORT_TAG = '{{%- import {template} as {name} -%}}\n'
BLOCK_TAG = '{{%- block {name} -%}}\n{block}\n{{%- endblock {name} -%}}\n'
DEFAULT_BLOCK = 'content'
# Adapted from daringfireball.net/2010/07/improved_regex_for_matching_urls
FLOW_EXPANSION = re.compile(r'''
@				# Beginning marker
(				# Capture 1: The filter name
	[A-Za-z0-9_-]+
)
(?:\.			# A simple argument can be given like .argument
	(			# Capture 2: Simple argument
		[A-Za-z_][A-Za-z0-9_]+
	)
/				# Followed by a slash (ignored).
|
\[				# A complex argument can be given like [with spaces]
	(			# Capture 3: The complex argument.
		(?:[^\\\]]|\\.)*
	)
\]
|
	/			# a trailing slash, ignored.
)
(				# Capture 3: The URL
	(?:			# One or more:
				# Run of non-space, non-()<>
		[^\s()<>]+
	|			# OR
				# Balanced parens, upt to two levels
		\((?:[^\s()<>]+|\([^\s()<>]+\))*\)
	)+
	(?:			# End with:
				# Balanced parens, upt to two levels
		\((?:[^\s()<>]+|\([^\s()<>]+\))*\)
	|			# OR
				# Not a space or (markdown) punctuation
		[^\s`!()\[\]{};:'".,<>?«»“”‘’@*_]
	)
)
''', re.IGNORECASE | re.VERBOSE)
