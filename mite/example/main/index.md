---
title: Main
styles:
- '@stylus/main'
scripts:
- '/js/dollar.js'
- '@coffee/test'
blocks:
  aside: |
    This is in the aside! Nifty. It may also reference @posts.title/first.
---
This is the *site index*.

'index' isn't a very good name for what index.html does these days.

And [here](@posts/first) is the first post. It's named @posts.title/first.

You may also use the verbose jinja syntax to reference page titles like
"{{ 'first'|posts('title') }}".
