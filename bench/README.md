# grav-logger against PHP's and Python's plain file logging

The same work, against the same kind of destination: [`bench.grav`](bench.grav)
(a `LogChannel` with one `StreamHandler`, structured context included),
[`bench.php`](bench.php) (`fopen`/`fwrite`/`fflush` per line — what PHP code
does for this without pulling in a framework and Monolog), and
[`bench.py`](bench.py) (Python's standard `logging` module, a `FileHandler`).
20,000 log lines, each flushed before the next.

```bash
grav bench.grav --release -o logger_bench --emit bin && ./logger_bench 20000 /tmp/out.log
php bench.php 20000 /tmp/out.log
python3 bench.py 20000 /tmp/out.log
```

## Results

Best of 3. Milliseconds (lower is better); memory is peak RSS in MB.

| | grav-logger (`--release`) | plain PHP | Python `logging` |
|---|---:|---:|---:|
| 20,000 lines | 61 | **46** | 464 |
| peak memory (MB) | **3.9** | 39.5 | 13.0 |

The PHP script does less work than grav-logger's benchmark: it interpolates
one number straight into the line, where grav-logger's formats a structured
context map (a real `HashMap`, looked up and quoted-if-needed per field) —
closer to what a program actually logs. Even so the two land in the same
few-microseconds-per-line range; both are dominated by the same `fwrite` +
`fflush` per line. Python's `logging` module, going through its own
formatter and handler chain in the interpreter, is about 8–10× slower for
the same work.

Memory is the clear difference: grav-logger peaks at about a tenth of
PHP's and under a third of Python's, for the same 20,000 lines — no
interpreter or framework runtime underneath it.
