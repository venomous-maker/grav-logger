#!/usr/bin/env python3
# bench.py — the same work as bench.grav and bench.php, through Python's
# standard logging module (a FileHandler, flushed every record). See
# bench/README.md.
import logging
import os
import sys
import time

n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/grav_logger_bench.log"
try:
    os.remove(path)
except FileNotFoundError:
    pass

logger = logging.getLogger("bench")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(path)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
logger.addHandler(handler)

t0 = time.monotonic()
for i in range(n):
    logger.info("request handled in %dms i=%d", i, i)
    handler.flush()
ms = int((time.monotonic() - t0) * 1000)
print(f"pylog: {n} lines in {ms}ms")
try:
    os.remove(path)
except FileNotFoundError:
    pass
