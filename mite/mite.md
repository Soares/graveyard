Mite is for compiling directories to new locations. You use it to generate websites.

It integrates tightly with git and helps you maintain a branch which is just the compiled site. (This is especially useful with `gh-pages`.)

<!--Mite compiles your site from a number of directories.--> Each directory is called a "module" and is run through a single compiler.

Every file in a module (recursively through the tree) goes through the same compiler. So you can have a `coffee/` module that's compiled with coffeescript and a `stylus` module that's compiled with stylus.

Module destinations may overlap. A top-level module (in your source) may output to a deeply nested directory in your site. But the module directory structure will be the same in both the module and the output directory and all files will be run through one compiler. So, for example, you might want a config like this:

    root: copy to .
	main: markdown to .
	stylus: css
	coffee: js

Then your input site may look like this:

    config.yaml
	root/
		favicon.ico
	main/
		index.md
	stylus/
		main.styl
	coffee/
		main.coffee

And your output site will look like this:

	favicon.ico
	index.md
	css/
		main.css
	js/
		main.js

Nifty.

Module configuration is essentially choosing a compiler and a destination. (There are more options, but don't worry too much about those). The standard configuration syntax is `compiler to destination`. If you leave the compiler off, a compiler that matches the directory name will be used. (In the above example, the `stylus/` and `coffee/` directories are compiled using the `stylus` and `coffee` compilers respectively.)

Any directories which you don't specify will be copied verbatim. You can tell mite to ignore directories with the `ignore` list in your `config.yaml`.

If you leave both of (i.e. `posts: true`) then both the destination and the compiler will take on the module name.

If the compiler is not specified nor found, the `flow` compiler will be used. Flowdown is a mite thing.

Mite has `copy`, `jinja`, and `flow` compilers baked in. The mite skeleton comes with a bunch of other useful compilers. You may provide your own compilers in the `compilers` directory. They should be python files which provide a `Compiler` object. Check out the ones in the skeleton for examples, they're easy to write.

Mite uses the `flow` compiler by default. `flow` is a yaml/jinja2 hybrid that makes your life a little easier. It's like `jinja` except it automatically extends the right template and puts your content in right `{% block %}`. See below for details. Flow templates in modules extend the layout file in `layouts/` which shares a name with the module.
