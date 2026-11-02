"""Scan documents or a built page for data that must not be published.

Usage:
    python -I privacy_scan.py FILE ... [--pack br] [--allow-prefix PREFIX]...

FILE is Markdown, HTML or any text file. HTML is read with its entities decoded, attributes included.
Reports, with file and line, then exits 1 when anything is found:
  email            e-mail addresses
  phone            international numbers (+ and 7 to 15 digits, with or without spaces, dots or dashes)
                   and common national shapes: area code in brackets, dashed groups, trunk prefix 0
  card             13 to 19 digit numbers, with spaces or dashes, that pass the Luhn check
  token            API keys and tokens (sk-, ghp_, github_pat_, AKIA, AIza, xox, JWT) and
                   key = "value" assignments for api key, secret, token or password
  private_key      -----BEGIN ... PRIVATE KEY----- headers
  url_credentials  URLs with user:password@ (databases, https, ftp)
  slack            workspace links on slack.com
--pack br   adds Brazilian formats: cpf, cnpj, phone_br (country code 55 + area code + 8 or 9 digits).
            More packs would be added to PACKS; none are on by default.
--allow-prefix P   skip a match that starts with P (repeatable). Use it for synthetic test data, for
            example --allow-prefix 55629900 or --allow-prefix test.user@. A leading "+" and separators are
            ignored when comparing digits.
A clean result is not a guarantee: names, street addresses, national IDs outside the enabled packs,
health data and free-text secrets are not detected. The RESULT line says so.
"""
import argparse
import html
import re
import sys

PATTERNS = {
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}",
    "phone": (r"(?<![\w+])\+[1-9](?:[ .-]?\(?\d{1,4}\)?){2,6}(?!\d)"
              r"|(?<![\d(])\(\d{3}\)[ .-]?\d{3}[ .-]\d{4}(?!\d)"
              r"|(?<![\d.])\d{3}[ .-]\d{3}[ .-]\d{4}(?![\d.])"
              r"|(?<![\d.-])0\d{1,4}[ .-]\d{3,4}[ .-]\d{3,4}(?![\d.-])"),
    "card": r"(?<![\d.-])\d(?:[ -]?\d){12,18}(?![\d-])",
    "token": (r"sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_\w{20,}|AKIA[0-9A-Z]{16}|AIza[\w-]{35}"
              r"|eyJ[\w-]{20,}\.[\w-]{10,}|xox[abpr]-[\w-]{10,}"
              r"|(?i:(?:api[_-]?key|secret|token|password|passwd)\w*)\s*[:=]\s*[\"']?[A-Za-z0-9/+_.=-]{16,}"),
    "private_key": r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----",
    "url_credentials": r"\b[a-z][a-z0-9+.-]*://[^\s/:@\"'<>]+:[^\s/@\"'<>]+@",
    "slack": r"https://[a-z0-9-]+\.slack\.com/\S+",
}
PACKS = {
    "br": {
        "cpf": r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)",
        "cnpj": r"(?<!\d)\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}(?!\d)",
        "phone_br": r"(?<!\d)55\d{10,11}(?!\d)",
    },
}


def luhn_ok(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2:
            n = n * 2 - 9 if n * 2 > 9 else n * 2
        total += n
    return total % 10 == 0


def _squash(s):
    return re.sub(r"[\s.()-]", "", s).lstrip("+")


def allowed(match, prefixes):
    plain, squashed = match.lower(), _squash(match)
    return any(plain.startswith(p.lower()) or (_squash(p) and squashed.startswith(_squash(p))) for p in prefixes)


def scan_text(text, patterns, allow=()):
    """Yield (line number, kind, matched text)."""
    for n, line in enumerate(text.splitlines(), 1):
        for kind, pat in patterns.items():
            for m in re.finditer(pat, line):
                s = m.group(0)
                if kind == "card":
                    digits = re.sub(r"\D", "", s)
                    if not (13 <= len(digits) <= 19 and luhn_ok(digits)):
                        continue
                if allowed(s, allow):
                    continue
                yield n, kind, s


def main(argv=None):
    ap = argparse.ArgumentParser(description="Scan files for data that must not be published.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--pack", action="append", default=[], choices=sorted(PACKS), help="country pack, e.g. br")
    ap.add_argument("--allow-prefix", action="append", default=[], metavar="PREFIX",
                    help="skip matches that start with PREFIX (repeatable), for synthetic test data")
    args = ap.parse_args(argv)
    patterns = dict(PATTERNS)
    for pack in args.pack:
        patterns.update(PACKS[pack])
    found = 0
    for f in args.files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if f.lower().endswith((".html", ".htm")):
            text = html.unescape(text)
        for n, kind, s in scan_text(text, patterns, args.allow_prefix):
            print(f"{f}:{n}: {kind}:")
            found += 1
    checked = ", ".join(patterns)
    limits = "names, street addresses, national IDs outside the enabled packs, health data, free-text secrets"
    if found:
        print(f"RESULT: FOUND {found} (checked: {checked}; not checked: {limits})")
    else:
        print(f"RESULT: CLEAN (checked: {checked}; not checked: {limits})")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
