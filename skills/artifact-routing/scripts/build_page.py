#!/usr/bin/env python3
"""Build a publishable reader page from a lean source page.

A lean source holds only content and page-specific CSS. It carries two empty
marker pairs where the reader goes:

    /* reader.css */
    /* /reader.css */          (inside the page <style>)

    // reader.js
    // /reader.js              (inside the page <script>)

Usage:
    python -I build_page.py SRC.html -o OUT.html [--autolink] [--prefixes R Q ADR-]

The script copies assets/reader/reader.css and reader.js between the markers
(anything already between them is replaced, so a built or shell page rebuilds
cleanly). With --autolink it then runs autolink.py on the result. When
--prefixes is absent, the prefixes come from the data-id-prefixes attribute of
the page, so the build and the reader agree. Exit code: 0 on success, 1 on a
missing marker or a failed autolink run, 2 on a usage error.
Standard library only.
"""
import argparse
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # python -I does not add the script folder
import autolink  # noqa: E402
READER = HERE.parent / "assets" / "reader"
MARKERS = (
    ("/* reader.css */", "/* /reader.css */", "reader.css"),
    ("// reader.js", "// /reader.js", "reader.js"),
)


class BuildError(Exception):
    pass


def inline_reader(src, reader_dir=READER):
    """Return src with the reader sources placed between their markers."""
    for start, end, name in MARKERS:
        if src.count(start) != 1 or src.count(end) != 1:
            raise BuildError(f"expected exactly one pair of markers {start!r} and {end!r}")
        i = src.index(start)
        j = src.index(end, i)
        if j < i:
            raise BuildError(f"marker {end!r} comes before {start!r}")
        body = (reader_dir / name).read_text(encoding="utf-8").rstrip()
        if name == "reader.js" and "</script" in body.lower():
            raise BuildError("reader.js contains a closing script tag and cannot be inlined")
        src = src[: i + len(start)] + "\n" + body + "\n" + src[j:]
    return src


def page_prefixes(src):
    """Prefixes from data-id-prefixes on the main element, or an empty list (same function as autolink.py)."""
    return autolink.page_prefixes(src)


def run_autolink(path_in, path_out, prefixes):
    cmd = [sys.executable, "-I", str(HERE / "autolink.py"), str(path_in), "-o", str(path_out)]
    if prefixes:
        cmd += ["--prefixes", *prefixes]
    done = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return done.returncode, (done.stdout + done.stderr).strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Inline the reader into a lean page and optionally autolink it.")
    ap.add_argument("source")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--autolink", action="store_true", help="run autolink.py on the built page")
    ap.add_argument("--prefixes", nargs="+", help="ID prefixes for autolink (default: data-id-prefixes of the page)")
    args = ap.parse_args(argv)
    src_path = pathlib.Path(args.source)
    out_path = pathlib.Path(args.output)
    try:
        built = inline_reader(src_path.read_text(encoding="utf-8"))
    except BuildError as e:
        print(f"error: {src_path}: {e}", file=sys.stderr)
        return 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not args.autolink:
        out_path.write_text(built, encoding="utf-8", newline="")
        print(f"built {out_path} ({len(built.encode('utf-8'))} bytes)")
        return 0
    prefixes = args.prefixes if args.prefixes else page_prefixes(built)
    with tempfile.TemporaryDirectory() as tmp:
        stage = pathlib.Path(tmp) / "stage.html"
        stage.write_text(built, encoding="utf-8", newline="")
        staged_out = pathlib.Path(tmp) / "linked.html"
        code, report = run_autolink(stage, staged_out, prefixes)
        if report:
            print(report)
        if not staged_out.exists():
            print("error: autolink.py did not write a page", file=sys.stderr)
            return 1
        out_path.write_text(staged_out.read_text(encoding="utf-8"), encoding="utf-8", newline="")
    print(f"built {out_path} ({out_path.stat().st_size} bytes), autolink exit {code}")
    return 1 if code else 0


if __name__ == "__main__":
    sys.exit(main())
