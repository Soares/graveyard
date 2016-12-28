# Mite

A mighty modular site generator that might be a mite useful.

It's a distant descendant of [cactus](https://github.com/koenbok/Cactus).

The goal is to generate static websites.

The philosophy is simple:

1. __Each directory in your source website holds files of a single type:__
   Javascript, blog posts, whatever.
1. __Each directory has a compiler which processes those files:__
   a Coffeescript compiler, markdown, whatever.
1. __Source directories can map to different output directories:__ You can put
   coffee files in `coffee/` and have them end up in `js/`. You can put
   markdown files in `markdown/` and have them end up at the site root.

Your source layout need not match your dest layout. Each directory holds
a different filetype. It's that simple.

It's going to support deploying your site to
[gh-pages](http://pages.github.com/) pretty soon.

Oh, also, if you're on a Mac and you use the mite local server it will
automatically reload your pages for you when you change your files. It will
add/remove/update only the affected files, so it's quite fast.

It shouldn't be hard to add similar support to other systems. Pull requests are
welcome.

## Configuration

You do your configuration in the site's `config.yaml` file.

There are a few boring options, but mostly you'll be naming directories and
telling mite where to put them. The syntax looks like this:

	posts: true
    stylus: css
	coffee: js
	pages:
		to: ''
		compiler: jinja
	copy: [images]

Most sites will have as simple configuration like this. (Perhaps simpler.)

The above exhibits a number of shortcuts. It is equivalent to the following
expanded configuration:

	posts:
		to: posts
	stylus:
		to: css
	coffee:
		to: js
	pages:
		to: ''
		compiler: jinja
	images:
		to: images
		compiler: copy

The most important configuration options are `to` and `compiler`. If either are
omitted, the module name is used in its stead.

Compiler `<name>` should exist in `compilers/<name>.py`. It should provide
a `Compiler` object which inherits from a compiler in `mite.compilers`.
Built-in compilers include:

* `copy`: Copies files directly
* `jinja`: Renders renders files with [jinja2](http://jinja.pocoo.org/docs/)
  and some relevant site context
* `flow`: A horrifying yaml/jinja hybrid that makes your life much easier

If you've cloned the mite [skeleton](http://github.com/Soares/skeleton.mite),
you'll also find `stylus`, `coffee`, `markdown`, `flowdown`, and `kramer`
compilers available to you.

Flowdown is the Flow compiler rendered using markdown. Kramer is the Flow
compiler rendered using [kramdown](http://kramdown.rubyforge.org/). I am not
responsible for installing these binaries on your system. Flow is a mite thing,
see below.

I'm not entirely sure what the jinja page context is yet. I might know after
I start using mite a bit more?

There are a handful of top-level special keywords (like `copy`) that make your
life easier. They are:

* `build`: The relative path to the build directory (`.build` by default)
* `compiler`: The default compiler to use (`flowdown` by default)
* `compilers`: The relative path to the compilers directory (`compilers` by
  default)
* `copy`: A list of modules to copy directly (useful for static media that you
  want in both places).
* `layouts`: The relative path to the layout directory (`layouts` by default)
* `modules`: A set of module configurations as described above. Most modules
  can be configured on the top level. This is useful if you want to compile
  a directory named `server/` or something and you don't want mite to interpret
  it as a borked attempt at local server configuration.
* `server`: Local server config. May be given `port` (to serve on) and `delay`
  (between checking for updates, ½ second default).
* `site`: The relative path to the source site (current directory by default)
* `stub`: The url to serve when an internal page tries to link to a page that
  doesn't yet exist (useful in wiki-like sites) (default `/stub.html`).

Each module actually takes a number of parameters beyond `to` and `compiler`,
actually. The full list is:

* `compiler`: The compiler to use. Defaults to the module name.
* `context`: Jinja context in any jinja or jinja-descended compilers. Empty by
  default.
* `delay`: Overrides global `delay` if given. (Useful if most directories
  compile fast but one compiles slowly.)
* `from`: The source directory. Defaults to the module name.
* `ignore`: A (python-style) regex of files to ignore. Defaults to `^.`, set it
  `false` if you want to include hidden files.
* `layout`: The layout to use by default when rendering any jinja or
  jinja-descended compiler. Defaluts to the module name.
* `stub`: Overrides global `stub` if given.
* `to`: Output site destination. May be an empty string or a deeply nested
  path, but should be relative to the top of the site. Defaults to the module
  name.


## Compilers

Compilers are pretty simple to write. Check out some examples in the
[skeleton](http://github.com/Soares/skeleton.mite).

You must define a `Compiler` class which extends `mite.compilers.Compiler`.

Basically, you want to override the `write` function, grab the file from
`self.source` and write the modified version to `self.destination`.

You're welcome to change `self.filename` (`self.url` and `self.destination` are
python properties, they'll stay correct). It's suggested that you do such
things in `__init__`.

You should set the classes' `EXTENSION` attribute if you plan to generate
something besides `.html` files. It's hard to guess output extensions from
input files.

You're welcome to write more than just `self.destination` if you want to make
things like magical tag generators. The `compiler` setting on modules may take
a list of compilers, so your tag compiler need not also do the writing. (In
fact, it shouldn't.)

If you want to do formatting on top of jinja templating, inherit the `Jinja`
compiler (which extends `Compiler`). Overide `parse(text)` and return
a `(content, context)` tuple.

If you want to hook into the flow magic, inherit `Flow` and override the
`render(text)` function.

Javascript/CSS compilers should inherit the `mite.compilers` of the same name.
They've already got the right extensions and some magic to reload the right
parts of the web page.

## Flow

Flow is like [liquid](http://liquidmarkup.org/)
[jinja](http://jinja.pocoo.org/docs/). Flow templates may have a flow header,
which looks like

    ---
	yaml: magic!
	title: My Title
	layout: mylayout
	blocks:
		block1: |
			This is my multiline
			block one text.
	---

The `layout` config is used to select a layout to extend. (You may leave off
the extension for smart detection.) Note that directories can be given default
layouts in `config.yaml`.

The `blocks` config can be used to override jinja blocks. It's especially
useful in intermediary templates.

Flow takes this header and the rest of the content and generates a jinja file.
The above header would generate a jinja file something like:

    {% extends "mylayout.html" %}
	{% block block1 %}
	This is my multiline
	block one text.
	{% endblock block1 %}
	{% block content %}
	{# PAGE CONTENTS HERE #}
	{% endblock content %}

Which is then rendered with the remaining configuration variables as page
context.
