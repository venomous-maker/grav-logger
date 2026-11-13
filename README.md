# grav-logger

Leveled, structured logging for [Grav](https://github.com/venomous-maker/grav):
named channels, pluggable handlers (a file, daily-rotating files, standard
error, syslog, or several at once) and formatters (a human-readable line, or
one JSON object per line) — Laravel's Log facade and Monolog's handlers, in
one small package with no runtime underneath it but the standard library.

```grav
import "std"
import "grav-logger"

fn main() {
    Logging.toFile("/var/log/app.log")
    Logging.info("server started")
    Logging.warning("low disk space", fields("freeMb", 512))

    let withRequest = Logging.channel().with("requestId", "abc123")
    withRequest.error("request failed")       // ... request failed requestId=abc123
}
```

## Install

```bash
grav add github.com/venomous-maker/grav-logger
```

```grav
import "grav-logger"
use logger.*
```

`std.sys` already has a small built-in `Log`/`Logger`/`LogLevel` (one
destination, five levels); grav-logger's `Logging`/`LogChannel`/`Level` are
named apart from them on purpose, so a program can `import "std"` and
`use logger.*` together without either shadowing the other.

## Levels

Eight, ascending, plus `Off` (as PSR-3's do): `Level.Debug`, `Info`,
`Notice`, `Warning`, `Error`, `Critical`, `Alert`, `Emergency`. A channel (or
a handler) below a level skips it before building anything — a disabled
`debug()` call costs one comparison.

## The facade

```grav
Logging.toStderr()                                  // the default channel, to standard error
Logging.toFile("/var/log/app.log")                  // ... or to a file
Logging.daily("/var/log/app.log", 14)                // ... or rotating daily, 14 days kept
Logging.setLevel(Level.Warning)

Logging.debug("query"); Logging.info("started"); Logging.notice("...")
Logging.warning("slow", fields("ms", 420))          // context: HashMap<string, any>
Logging.error("failed")
Logging.error("request failed", e)                  // an Exception: message, then e.describe()
Logging.critical("..."); Logging.alert("..."); Logging.emergency("...")

Logging.channel("db").toFile("/var/log/db.log").warning("slow query")   // a named channel
Logging.useChannel("db")                             // db becomes what Logging.info etc. use
Logging.stack(["default", "db"]).info("to both")     // fans out to several channels' handlers
```

Where `fields(...)` is your own small `HashMap<string, any>` builder (or
build one by hand); there is no dependency on grav-orbit for this.

## Channels, handlers and formatters

A `LogChannel` is a name, a level, and a list of `Handler`s; each handler has
its own level and `Formatter` too, so one channel can send debug detail to a
file while only warnings and up reach standard error:

```grav
let app = new LogChannel("app")
let toFile = new StreamHandler("/var/log/app.log")
let toStderr = StreamHandler.stderr()
toStderr.minLevel = Level.Warning
app.addHandler(toFile).addHandler(toStderr)
app.info("quiet in the terminal, still in the file")
app.error("loud in both")
```

**Handlers**: `StreamHandler` (a file, or `StreamHandler.stderr()`),
`RotatingFileHandler(path, days)` (a new file each day, old ones pruned),
`SyslogHandler(ident)`, `StackHandler([h1, h2])` (fans out), `NullHandler`
(writes nothing). Write your own by implementing `Handler` (`handle(record)`,
`enabled(level)`).

**Formatters**: `LineFormatter` (the default — a timestamp, the level, the
channel, the message, then `key=value` fields, quoted if a value has a
space) and `JsonFormatter` (one JSON object per line, for an aggregator that
parses structured fields instead of a human reading them):

```grav
let h = new StreamHandler("/var/log/app.jsonl")
h.formatter = new JsonFormatter()
```

## Context

Pass a one-off context map with the call, or `.with(key, value)` for a copy
of the channel that adds it to every call from then on (the original channel
is unaffected):

```grav
app.info("checkout", fields("orderId", 42, "total", 19.99))

let perRequest = app.with("requestId", requestId)
perRequest.info("started")      // ... started requestId=abc123
perRequest.info("finished")     // ... finished requestId=abc123
```

## Tests

```bash
grav test tests/logger.grav
```

Needs nothing external — every handler writes to a temp file or directory
the tests clean up themselves (`SyslogHandler`'s test only checks that
logging through it does not throw).

## License

MIT. See [LICENSE](LICENSE).
