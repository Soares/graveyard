# Hume
## Basic Utilities

### Hume is not yet stable.

Hume is a core set of basic utilities for vim plugins. It standardizes some
workflows that I've found useful.

It helps you do things like:

* Define a bunch of script default variables
* Access certain settings in a safe way independent of vim version.
* Define inclusions settings, which are settings that a user can turn on or off
  (globally) as well as turning off (except for a whitelist) or on (except for
  a blacklist). Whitelisting is signaled by setting the variable to a list.
  Blacklisting is signaled by setting the variable to a dict where excluded
  items are keys with zero-values in the dict.

Hume is designed to be included in a bunch of different plugins. Don't worry;
the way vim autoload scripts work hume will only be loaded once, no matter how
many plugins have copied it.

However, this flexibility comes with the limitation that if you have multiple
hume versions available only the first one that vim finds (essentially at
random) will be loaded. That's why there's the weird versioning of functions,
and that's why you'll have to call functions with hume#<version>#<function>.
