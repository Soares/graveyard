from distutils.core import setup

setup(
	name='Mite',
	version='0.1.0',
	description='A mighty modular site generator that might be a mite useful.',
	author='Nate Soares',
	author_email='nate@so8r.es',
	packages=[
		'mite',
		'mite.action',
		'mite.compiler',
		'mite.sourcetree',
		'mite.util'],
	scripts=['scripts/mite'],
	requires=['pyyaml', 'jinja2'],
)
