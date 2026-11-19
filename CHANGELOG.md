# Changelog

Every release of grav-logger, newest first. Each is a `vX.Y.Z` tag with a GitHub
release carrying its section; the `grav` line in `grav.toml` says which
compiler versions it builds with.

## Unreleased

The first tagged release. Needs grav 1.7.0 or newer.

Leveled, structured logging for [Grav](https://github.com/venomous-maker/grav): named channels, pluggable handlers (a file, daily-rotating files, standard error, syslog, or several at once) and formatters (a human-readable line, or one JSON object per line) — Laravel's Log facade and Monolog's handlers, in one small package with no runtime underneath it but the standard library.
