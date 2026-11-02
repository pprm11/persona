"""Write diagrams.json (every mermaid block of the given files) to the current directory.

Usage: python extract.py FILE.md|FILE.html ...
Reads fenced ```mermaid blocks from Markdown and <pre class="mermaid"> blocks from HTML pages (the text is
HTML-unescaped). Any other extension is tried with both patterns. A file with no block prints a warning on
stderr; if it mentions mermaid anyway (a div with class mermaid, an unclosed fence) the exit code is 1.
Copy measure.html and search.js to that directory, then serve it (python -m http.server) and open measure.html; in the console run
  await measure({tight: true})      -> [id, width, height] per block
  await best(1000, 1300)             -> best direction per flowchart for a 1000 px column
"""
import html
import json
import os
import re
import sys

FENCE = re.compile(r"```mermaid\n(.*?)```", re.S)
PRE = re.compile(r"<pre\b[^>]*\bclass\s*=\s*(?:\"[^\"]*\bmermaid\b[^\"]*\"|'[^']*\bmermaid\b[^']*')[^>]*>(.*?)</pre\s*>",
                 re.S | re.I)


def blocks_of(path, text):
    """Mermaid sources found in one file's text, in document order."""
    text = text.replace("\r\n", "\n")
    ext = os.path.splitext(path)[1].lower()
    if ext in (".md", ".markdown"):
        return [m.group(1) for m in FENCE.finditer(text)]
    found = [html.unescape(m.group(1)).strip("\n") + "\n" for m in PRE.finditer(text)]
    if ext in (".html", ".htm"):
        return found
    return found + [m.group(1) for m in FENCE.finditer(text)]


def main(argv, out_dir=None):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    out, code = [], 0
    for f in argv:
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        found = blocks_of(f, text)
        if not found:
            print(f"warning: no mermaid blocks found in {f}", file=sys.stderr)
            if re.search(r"mermaid", text, re.I):
                print(f"error: {f} mentions mermaid but no block matched (expected <pre class=\"mermaid\"> "
                      "or a ```mermaid fence)", file=sys.stderr)
                code = 1
        for i, src in enumerate(found):
            out.append({"f": os.path.splitext(os.path.basename(f))[0], "i": i + 1, "src": src})
    here = out_dir or os.getcwd()
    with open(os.path.join(here, "diagrams.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh)
    print(len(out), "blocks")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
