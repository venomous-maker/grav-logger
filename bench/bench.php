<?php
// bench.php — the same work as bench.grav and bench.py: a line per call,
// flushed, to a file (what PHP code does for this without a framework
// pulling in Monolog). See bench/README.md.
$n = isset($argv[1]) ? (int)$argv[1] : 20000;
$path = $argv[2] ?? '/tmp/grav_logger_bench.log';
@unlink($path);

$f = fopen($path, 'a');
$t0 = microtime(true);
for ($i = 0; $i < $n; $i++) {
    $line = date('Y-m-d H:i:s') . " INFO     request handled in {$i}ms i=$i\n";
    fwrite($f, $line);
    fflush($f);
}
$ms = (int)((microtime(true) - $t0) * 1000);
fclose($f);
echo "phplog: $n lines in {$ms}ms\n";
@unlink($path);
