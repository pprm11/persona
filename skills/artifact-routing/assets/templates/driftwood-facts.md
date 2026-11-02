# Driftwood: canonical sample facts

Driftwood is a fictional command-line tool that rotates and compresses log files. Every sample page in this folder (`tutorial.html`, `how-to.html`, `reference.html`, `explanation.html`, `multi-type.html`) takes its facts from this sheet. When a page needs a new fact, add it here first, then use it. `reference.html` is the fullest page and wins any disagreement.

Version 2.4.0. Commit `9f3c2d1` (fake). As of 2026-11-01. Owner: documentation maintainer. Sample content: never present these facts as real.

## Commands

| ID | Command | Synopsis | Exit codes | Since |
|---|---|---|---|---|
| CMD1 | `driftwood init` | `driftwood init [--dir PATH] [--force]` | 0, 2, 3 | 1.0 |
| CMD2 | `driftwood run` | `driftwood run [--config PATH] [--dry-run] [--verbose]` | 0, 1, 2, 3, 4 | 1.0 |
| CMD3 | `driftwood check` | `driftwood check [--config PATH] [--strict]` | 0, 1, 2 | 1.0 |
| CMD4 | `driftwood restore` | `driftwood restore FILE [--generation N] [--to PATH]` | 0, 3, 5 | 1.2 |

- Global options: OPT1 `--config PATH` (default `./driftwood.toml` or ENV1), OPT2 `--quiet`, OPT3 `--help`, OPT4 `--version` (prints `driftwood 2.4.0`).
- Command options: OPT5 `--dir PATH` (default `.`), OPT6 `--force`, OPT7 `--dry-run` (since 1.3), OPT8 `--verbose`, OPT9 `--strict` (since 2.0), OPT10 `--generation N` (default 1, 1 to `keep`), OPT11 `--to PATH` (default `FILE.restored`).
- `FILE` of `restore` is the Live log name, for example `app.log`. It never overwrites a Live log.

## Configuration file `driftwood.toml`

All keys live in the `[rotate]` table. Lookup order: `--config`, then `DRIFTWOOD_CONFIG`, then the current folder.

| ID | Key | Type | Default | Allowed values |
|---|---|---|---|---|
| CFG1 | `path` | string | none, required | Existing folder that holds the Live logs |
| CFG2 | `keep` | integer | `7` | 1 to 365 |
| CFG3 | `compress` | string | `"gzip"` | `"none"`, `"gzip"`, `"zstd"` (zstd since 2.2) |
| CFG4 | `max_size` | string | `"50MB"` | Integer plus KB, MB or GB, from 1KB to 10GB |
| CFG5 | `schedule` | string | `"daily"` | `"hourly"`, `"daily"`, `"weekly"`, or a 5-field cron expression (cron since 2.1) |

`driftwood init` writes this starter file, with `path = "."`:

```
[rotate]
path = "."
keep = 7
compress = "gzip"
max_size = "50MB"
schedule = "daily"
```

A Live log is due when its size is above `max_size` or the `schedule` time has been reached, whichever comes first.

## Environment variables and files

- ENV1 `DRIFTWOOD_CONFIG` (since 2.3). ENV2 `NO_COLOR`.
- FIL1 `driftwood.toml`. FIL2 `.driftwood/state.json`. FIL3 `NAME.log` (Live log). FIL4 `NAME.log.N.gz` (Generation N; `.zst` for zstd, no suffix for `"none"`; N=1 is the newest). FIL5 `.driftwood/lock` (Lock file, since 2.0).

## Since versions

OPT2 and ENV2 since 1.1. OPT1, OPT3, OPT4, OPT5, OPT6, OPT8, CFG1 to CFG5 (cron in CFG5 since 2.1, zstd in CFG3 since 2.2), FIL1 to FIL4 since 1.0. FIL5, EXIT4, ERR4 and OPT9 since 2.0. CMD4, OPT10, OPT11, EXIT5 and ERR5 since 1.2. OPT7 since 1.3. ENV1 since 2.3. Other messages and exit codes since 1.0.

## Exit codes

0 success. 1 findings (`check` found a due Live log, or `run` skipped a file). 2 config error. 3 permission denied. 4 lock held. 5 restore failed.

## Error messages (exact)

| ID | Message | Exit | Command |
|---|---|---|---|
| ERR1 | `error: config not found` | 2 | run, check |
| ERR2 | `error: permission denied on /var/log/app` | 3 | init, run, restore |
| ERR3 | `error: invalid value for keep: 400 (allowed 1 to 365)` | 2 | run, check |
| ERR4 | `error: another run holds the lock` | 4 | run |
| ERR5 | `error: generation 9 not found for app.log` | 5 | restore |
| ERR6 | `error: unknown compress value "lz4"` | 2 | run, check |
| ERR7 | `error: driftwood.toml already exists` | 2 | init |

## Outputs (exact shapes)

```
$ driftwood init --dir ./logs
wrote ./logs/driftwood.toml

$ driftwood check            # one Live log due, exit 1
config: ./driftwood.toml ok
due  /var/log/app/app.log     62MB > max_size 50MB
ok   /var/log/app/worker.log   4MB
1 file due

$ driftwood check            # nothing due, exit 0
config: ./driftwood.toml ok
ok   ./app.log   0KB
0 files due

$ driftwood run --dry-run    # exit 0
warning: dry run, no files changed
would rotate /var/log/app/app.log -> app.log.1.gz (compress gzip)
would delete app.log.7.gz (would become generation 8, keep is 7)

$ driftwood run              # exit 0
1 file rotated, 0 skipped

$ driftwood run --verbose    # exit 0, one line per file, then the summary
rotated ./app.log -> app.log.1.gz
1 file rotated, 0 skipped

$ driftwood run              # nothing due, exit 0
0 files rotated, 0 skipped

$ driftwood restore app.log --generation 2    # exit 0
restored app.log.2.gz -> app.log.restored
```

Check lines: `due` or `ok`, the Live log path as configured, its size (`62MB`, `81KB`), and for a due file `> max_size LIMIT`. Files are listed by name.

## Glossary (capitalized as terms; one definition each)

| Term | Definition |
|---|---|
| Archive | The set of compressed Generations kept for one Live log. |
| Burst | A short period in which a service writes far above its normal rate. |
| Check interval | The time between two calls of `driftwood run`, set by your scheduler. |
| Dry run | A run that reports what it would do and changes no file. |
| Generation | A numbered Archive copy of a Live log. Generation 1 is the newest. |
| Live log | A log file that an application still writes to. |
| Lock file | The file `.driftwood/lock`, which stops two runs from rotating at once. |
| Overshoot | The amount by which a Live log exceeds `max_size` before a check notices; at most one check interval of writes. |
| Retention | The number of Generations kept per Live log, set by `keep`. |
| Rotation | The act of renaming a Live log to Generation 1 and starting an empty Live log. |
| Sandbox | A throwaway folder where a tutorial runs, so no real file is touched. |
| Size trigger | The Trigger that fires when a Live log is above `max_size`. |
| State file | The JSON file that records the last Rotation time of each Live log. |
| Time trigger | The Trigger that fires when the `schedule` time is reached. |
| Trigger | A condition that makes a Live log due: size above `max_size`, or the `schedule` time reached. |

Abbreviations: CLI (Command-line interface), TOML (Tom's Obvious Minimal Language), ADR (Architecture decision record), UTC (Coordinated Universal Time), SHA (Secure Hash Algorithm; here, the id of a commit).

## Explanation facts

- Worst-case file size, write rate r, schedule period P, check interval c: time only `r x P`; size and time `max_size + r x c`.
- Sample inputs: r = 2.5 MB/s, P = 86400 s (daily), c = 60 s, `max_size = "50MB"`. Time only: 216 GB. Size and time: 200 MB.
- Goals G1 (bounded disk use), G2 (predictable retention). Limits L1 (numbered Generation names, not calendar periods), L2 (check granularity), L3 (rename window: the application writes to the renamed file until it reopens its log). ADR-1 Accepted 2026-10-28. Decisions D1, D2. Open questions Q1 (should `max_size` accept a share of free disk, owner: config format owner), Q2 (should the default `max_size` be lower, owner: release owner).

## Page-only facts

- Tutorial: Sandbox folder `driftwood-sandbox`, `app.log` of 2,000 lines (81 KB), config with `keep = 3` and `max_size = "64KB"`, steps S1 to S6.
- How-to: log folder `/var/log/app` (Windows `C:\logs\app`), failures F1 to F6, hourly scheduler call.
