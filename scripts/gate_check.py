#!/usr/bin/env python3
"""gate_check.py — validate release-gate ledger/report shapes (stdlib only).

Usage: python3 gate_check.py <dir|file> [...]
Convention: a ledger row is a markdown table row carrying a status token;
every FAIL check id must appear in a fix-plan Fix section with "Acceptance:".
"""
import re
import sys
from pathlib import Path

STATUSES = {"pass", "fail", "not assessed", "not-assessed", "na", "n/a", "inconclusive"}
EVID = re.compile(r"\S+:\d+|`[^`]+`|https?://|\bevidence\b|\bproof\b|\bverified\b|\boutput\b|\bcommand\b|\bcmd\b|\blog\b", re.I)
FIXH = re.compile(r"^#{2,4}\s*fix\s*\d*\s*:?\s*(.*?)\s*$", re.I | re.M)
ACC = re.compile(r"acceptance\s*:", re.I)


def targets(args):
    out = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out += sorted(p.glob("*.md"))
        elif p.is_file():
            out.append(p)
        else:
            return None
    return out


def main(argv):
    docs = targets(argv[1:] or ["."])
    if docs is None:
        print("missing path")
        return 2
    bad, fails, plans = [], [], []
    for p in docs:  # ponytail: O(n) single scan of ledger rows; upgrade to an indexed validator only if ledgers exceed ~5k rows.
        try:
            text = p.read_text()
        except OSError as e:
            bad.append(f"{p}: unreadable ({e})")
            continue
        if "fix-plan" in p.name.lower():
            plans.append(text)
        for i, ln in enumerate(text.splitlines(), 1):
            s = ln.strip()
            if not (s.startswith("|") and "|" in s[1:] and "---" not in s):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            st = next((c.lower() for c in cells if c.lower() in STATUSES), None)
            if not st:
                continue
            blob = " | ".join(cells)
            if st == "pass":
                if not EVID.search(blob):
                    bad.append(f"{p}:{i} PASS without evidence: {blob}")
            elif len([c for c in cells if c]) < 3 and not EVID.search(blob):
                bad.append(f"{p}:{i} no evidence-or-reason: {blob}")
            if st == "fail":
                cid = next((c for c in cells if c.lower() not in STATUSES), "")
                fails.append((str(p), i, cid, blob))
    secs = []
    for t in plans:
        bounds = [m.start() for m in FIXH.finditer(t)] + [len(t)]
        secs += [t[a:b] for a, b in zip(bounds, bounds[1:])]
    for p, i, cid, blob in fails:
        if not [s for s in secs if cid and cid.lower() in s.lower() and ACC.search(s)]:
            bad.append(f"{p}:{i} FAIL '{cid}' lacks Fix+Acceptance: {blob}")
    for s in secs:
        if not ACC.search(s):
            title = (FIXH.search(s).group(0) or "Fix?")[:60]
            bad.append(f"fix-plan: {title.strip()} lacks Acceptance line")
    print("\n".join(bad) if bad else f"GATE PASS ({len(docs)} files, {len(fails)} fails mapped)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
