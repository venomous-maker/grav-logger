# Changelog

Every release of grav-logger, newest first. Each is a `vX.Y.Z` tag with a GitHub
release carrying its section; the `grav` line in `grav.toml` says which
compiler versions it builds with.

## Unreleased

## 0.2.1 (2026-11-20)

### Performance

- `LineFormatter` and `JsonFormatter` walk a record's context with a loop
  instead of a closure made for every line, and the line formatter reserves
  its buffer up front: about 20% fewer instructions per logged line (the
  benchmark's 5,000 lines: 30.0M to 25.0M, the rest is its own string
  building and the `write` per line).

## 0.2.0 (2026-11-20)

### Requirements

- Needs grav 1.9.0 or later, and uses the 0.2.0 releases of the packages it
  depends on.

## 0.1.0 (2026-11-19)

The first tagged release. Needs grav 1.7.0 or newer.

Leveled, structured logging for [Grav](https://github.com/venomous-maker/grav): named channels, pluggable handlers (a file, daily-rotating files, standard error, syslog, or several at once) and formatters (a human-readable line, or one JSON object per line) — Laravel's Log facade and Monolog's handlers, in one small package with no runtime underneath it but the standard library.
