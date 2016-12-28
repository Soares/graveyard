# Mite
### A mighty modular site generator that might be a mite useful.

Mite is for compiling directories to new locations. You use it to generate
websites.

Mite integrates tightly with git and helps you maintain production branch. This
is especially useful with `gh-pages`.

Each directory is called a "module" and is run through a single compiler. Every
file in a module (recursively through the tree) goes through the same compiler.
So you can have a `coffee/` module that's compiled with coffeescript and
a `stylus` module that's compiled with stylus.

Modules have a source directory and a destination directory. They may be
different. You may have multiple source directories all render into the root of
your site, for instance.

The internal structure of a module is retained when the module is copied. Every
file in the module is run through the same compiler. If you want some files to
be treated differently, put them in a different module that outputs to the same
place.

Here's an example config:

    root: copy to .
    coffee: js
    stylus: css
    sass: css
    posts: true

Given an input site that looks like this:

    config.yaml
    root/
        favicon.ico
    stylus/
        main.styl
    coffee/
        main.coffee
    sass/
        extra.sass
    posts/
        post1.html
        post2.html
    templates/
        posts.html

Your output site will look like this:

    favicon.ico
    index.md
    css/
        main.css
        extra.css
    js/
        main.js
    posts/
        post1.html
        post2.html

Nifty.

Your yaml file should be a bunch of module configurations. Module
configurations are generally just the destination (a string) or a compiler and
a destination in the form `<compiler> to <destination>`.

You can tweak a number of other variables by using a configuration dictionary.
See __Configuration__ below.

If you omit the destination, the source directory will be copied to
a destination directory of the same name.

If you omit the compiler, mite will look for a compiler in the `compilers/`
directory that has the same name as the module. Failing that, it will fall back
to the `flow` compiler.

Flow is a mite thing. It's a yaml/jinja hybrid that automatically extends the
right template and puts your content in the right `{% block %}`. See below for
details.

If your module is compiled `flow` it will need a template in the `templates/`
dir with the same name as the module.

Mite uses the `flow` compiler by default. `flow` is a yaml/jinja2 hybrid that
makes your life a little easier. It's like `jinja` except it automatically
extends the right template and puts your content in right `{% block %}`. See
__Flow__ below.

## Configuration

The terse example above:

    root: copy to .
    main: markdown to .
    coffee: js
    stylus: css
    sass: css
    posts: true

Is almost exactly equivalent to the following:

    root:
        compiler: copy
        to: .
    main:
        compiler: markdown
        to: .
    coffee:
        compiler: coffee
        to: js
    stylus:
        compiler: stylus
        to: css
    sass:
        compiler: sass
        to: css
    posts:
        compiler: flow
        to: posts

With the caveat that the original leaves the `stylus` `sass` and `coffee`
compilers unspecified (mite will look for compilers of the same name but
fallback to flow) whereas the expanded version specifies them directly
(mite will error if they're missing).

### Site Configuration

The 'site' configuration option is special, and does not configure any modules.
Instead, it configures the site. You can use it to do things like change the
fallback compiler:

    site:
        build: _build        # Will be built to _build instead of .build.
        compiler: markdown
    root: copy to .
    posts: true                # Posts will be compiled with markdown.

The 'site' configuration object takes the following options:

#### Special Directories:

* `build`: The relative path to the build directory (`.build` by default)
* `site`: The config.yaml-relative path to the site root (`.` by default)
* `compilers`: The site-root-relative path to the compilers directory
  (`compilers` by default)
* `templates`: The site-root-relative path to the template directory
  (`templates` by default)
* `modules`: Module configurations. Identical to top-level module
  configurations. Mostly only useful for the purpose of defining a module named
  'site' (which would normally clash with the site config).

#### Local Server Configuration:
* `delay`: The amount of time (in seconds) to pause between checking the file
  system for changes to the site. Set to 'false' to turn off
  auto-recompilation. (default ½ second).
* `refresh`: If `false`, mite will stop trying to refresh browser pages when
  you update the site. (default `true`).

#### Module Defaults

* `compiler`: The default compiler to use (`flow` by default)
* `stub`: The url to serve when an internal page tries to link to a page that
  doesn't yet exist (useful in wiki-like sites) (default `/stub.html`).


### Module Configuration

Module configurations are top-level key: value pairs. The key specifies the
source directory. The value is often of the form `<compiler> to <destination>`:

    root: copy to .

If it's any other string, the string is treated as the destination path:

    stylus: css

If it's a boolean, the compiler is autoselected and the destination path
matches the source path:

    posts: true

It may also be a dictionary containing any or all of the following:

* `from`: The source directory. Defaults to the module name.
* `to`: Output site destination. May be an empty string or a deeply nested
* `compiler`: The compiler to use. Defaults to the module name. May be a list
  of compilers, in which case all are applied.
* `ignore`: A (python-style) regex of files to ignore. Defaults to `^.`, set it
  `false` if you want to include hidden files.
* `template`: The template to use by default when rendering any jinja or
  jinja-descended compiler. Defaluts to the module name.
* `context`: Jinja context in any jinja or jinja-descended compilers. Empty by
  default.
* `stub`: Overrides global `stub` if given.
  path. Should be relative. Defaults to the module name.
* `delay`: Overrides global `delay` if given. (Useful if most directories
  compile fast but one compiles slowly.)
* `filter`: The name of the module jinja2 filter used on urls.

## Compilers

Compilers are responsible for turning the input site into the output site.
Conceptually, they are Python classes which will be fed one module file at
a time and are expected to copy that file (performing transformations as
necessary) from source to destination.

They all inherit from a compiler in `mite.compilers` and have `source`,
`destination`, and `url` attributes. The only method you need to worry about is
`write` (and sometimes `remove` if you're writing complex compilers).

Compiler `<name>` should exist in `compilers/<name>.py`. It should provide
a `Compiler` object.  There are three built-in compilers which don't need to be
in the compilers directory. They are:

* __Copy__: Copies files directly
* __Jinja__: Renders renders files with [jinja2](http://jinja.pocoo.org/docs/)
  and some relevant site context
* __Flow__: A horrifying yaml/jinja hybrid that makes your life much easier

If you've cloned the mite [skeleton](http://github.com/Soares/skeleton.mite),
you'll also find `stylus`, `coffee`, `jauntdown`, `flowdown`, and `kramer`
compilers available to you:

* __Stylus__: [stylus](http://learnboost.github.com/stylus/) compiler.
* __Coffee__: [coffeescript](http://coffeescript.org/) compiler.
* __Jauntdown__: [jinja](http://coffeescript.org/) + python markdown.
* __Flowdown__: flow + python markdown.
* __Kramer__: flow + [kramdown](http://kramdown.rubyforge.org/).

I am not responsible for installing stylus/coffeescript/kramdown/etc. binaries
on your system.

### Writing Compilers

Compilers are pretty simple to write. Check out some examples in the
[skeleton](http://github.com/Soares/skeleton.mite).

You must define a `Compiler` class which extends one of the compilers in
`mite.compilers`.  Basically, you want to override the `write` function, grab
the file from `self.source` and write the modified version to
`self.destination`.

You should set the classes' `EXTENSION` attribute if you plan to generate
something besides `.html` files.

If you want to write to a completely different destination file (beyond just
changing the extension) feel free to change `self.filename`. `self.destination`
will automatically adjust.

You're welcome to write more than just `self.destination` if you want to make
things like magical tag generators.

Compilers should only do one thing. (One module can be given a list of
compilers, so there's no need for one to try to do everything.)

If you want to do formatting on top of jinja templating, inherit the `Jinja`
compiler. Override `parse(text)` and return a `(content, context)` tuple and
the rest is magic.

If you want to hook into the flow magic, inherit `Flow` and override the
`render(text)` function: it will handle setting the context and rendering the
jinja templates.

Javascript/CSS compilers should inherit the `mite.compilers` of the same name.
The `Javascript` and `CSS` compilers already have the right extensions and some
magic to reload the right parts of the web page.

## Flow

Flow is [liquid](http://liquidmarkup.org/)
[jinja](http://jinja.pocoo.org/docs/). Flow templates may have a flow header,
which looks like

    ---
    title: My Title
    template: special-layout
    blocks:
        block1: |
            This is my multiline
            block one text.
    ---

The `template` config is used to select a template to extend. You may leave off
the extension for smart detection by module name.

The `blocks` config can be used to override jinja blocks. It's especially
useful in intermediary templates.

The rest of the configuration variables are put into the page context and can
be used in the template.

Flow takes the header and the rest of the content and generates a jinja file.
The above header would generate a jinja file something like:

    {% extends "special-layout.html" %}
    {% block block1 %}
    This is my multiline
    block one text.
    {% endblock block1 %}
    {% block content %}
    {# PAGE CONTENTS HERE #}
    {% endblock content %}

Jinja templates which expect to be extended by flow templates must include
`{% block content %}`

Flow templates are actually run through jinja *twice*: Each block is expanded
with jinja seperately before being rendered. All blocks are then combined into
a new template which is expanded after extending the layout template. This is
done so that flow renderers (such as markdown) only ever run on expanded text.
You don't need to worry about your markdown compiler choking on jinja syntax
when the blocks are being rendered.

Flow headers may also contain a 'macros' list, which should be the names of
macro files to include before rendering each block (including the content
block).

Flow has a special syntax for linking to other pages in the site. Specifically,

    @module.attribute/some/page/url

expands to

    {{ "/some/page/url"|module("attribute") }}

This is a useful shortcut for using the default module filters.

## About

Mite is inspired by [cactus](https://github.com/koenbok/Cactus) and [jekyll](https://github.com/mojombo/jekyll). It's a personal take on static site generation that is all about the modules.

I'm just a dude.
