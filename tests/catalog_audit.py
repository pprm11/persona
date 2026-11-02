from pathlib import Path
import re
import os
import json
import subprocess
import sys

def private_pattern(terms):
    return re.compile('|'.join(re.escape(term) for term in terms), re.IGNORECASE) if terms else None

GENERIC = {
    "user path": re.compile(r"(?i)(?:[a-z]:[\\/]users[\\/]|/home/|/users/)[a-z0-9_.-]+"),
    "secret token": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "credential URL": re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]+@"),
}

LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
# Links inside a fenced block are examples, such as template placeholders, and are not checked.
FENCE_OPEN = re.compile(r'^[ \t]*(`{3,}|~{3,})')
FENCE_CLOSE = re.compile(r'^[ \t]*(`{3,}|~{3,})[ \t]*$')


def outside_fences(text):
    lines = []
    fence = None
    opening_line = None
    for number, line in enumerate(text.splitlines(keepends=True), start=1):
        if fence is None:
            match = FENCE_OPEN.match(line)
            if match and not (match.group(1).startswith("`") and "`" in line[match.end():]):
                fence = match.group(1)
                opening_line = number
                lines.append("\n")
            else:
                lines.append(line)
        else:
            match = FENCE_CLOSE.fullmatch(line.rstrip("\r\n"))
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
                opening_line = None
            lines.append("\n")
    return "".join(lines), opening_line

def link_exists(folder, target):
    # Windows drops trailing dots and spaces from a path segment, so '...' would resolve to the folder itself.
    if any(part not in ('.', '..') and part != part.rstrip('. ') for part in re.split(r'[\\/]', target)):
        return False
    return (folder / target).exists()

def audit_file(path, private_terms=()):
    text = path.read_text(encoding='utf-8')
    errors = []
    for label, generic in GENERIC.items():
        if generic.search(text): errors.append(label)
    pattern = private_pattern(private_terms)
    if pattern and pattern.search(text):
        errors.append('private marker')
    if path.suffix == '.md':
        prose, opening_line = outside_fences(text)
        if opening_line is not None:
            errors.append(f"unclosed fence at line {opening_line}")
        for target in LINK.findall(prose):
            target = target.split('#', 1)[0]
            if target and not re.match(r'^(?:https?://|mailto:|<)', target) and not link_exists(path.parent, target):
                errors.append('broken link: ' + target)
    if path.name == 'SKILL.md':
        parts = text.split('---', 2)
        if len(parts) != 3 or not re.search(r'(?m)^name: '+re.escape(path.parent.name)+r'\s*$', parts[1]):
            errors.append('invalid name')
        if len(parts) != 3 or not re.search(r'(?m)^description: .+', parts[1]):
            errors.append('missing description')
        if len(parts) == 3 and re.search(r'(?m)^level:', parts[1]):
            errors.append('unsupported level')
    return errors


def candidate_files(root):
    output = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"], check=True, capture_output=True).stdout
    return [p for p in output.decode("utf-8").split("\0") if p]


def release(root, pattern_file):
    if not pattern_file:
        print("release audit requires a private pattern file", file=sys.stderr)
        return 2
    try:
        patterns = json.loads(Path(pattern_file).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        print("release audit cannot read a valid private pattern file", file=sys.stderr)
        return 2
    if not isinstance(patterns, list) or not patterns or not all(isinstance(x, str) and x.strip() for x in patterns):
        print("release audit requires a nonempty JSON array of regex patterns", file=sys.stderr)
        return 2
    try:
        compiled = [re.compile(x, re.IGNORECASE) for x in patterns]
    except re.error:
        print("release audit has an invalid private regex", file=sys.stderr)
        return 2
    paths = candidate_files(root)
    found = False
    for relative in filter(None, paths):
        path = root / relative
        if not path.is_file(): continue
        try: text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"unscannable non-UTF-8 file: {relative}", file=sys.stderr); found = True; continue
        errors = audit_file(path)
        if any(pattern.search(text) for pattern in compiled): errors.append("private pattern")
        if errors:
            print(f"{relative}: {', '.join(errors)}"); found = True
    return 1 if found else 0

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    sys.exit(release(root, os.environ.get("PERSONA_PRIVATE_PATTERNS_FILE")))
