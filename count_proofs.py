#!/usr/bin/env python3
"""
count_proof_lines.py — count lines enclosed by Proof. and Qed./Admitted. in a Rocq file.
Only counts blocks that have a matching Proof. opener.
Blank lines and single-line comment-only lines are excluded.
"""

import re
import sys


# A comment-only line: optional whitespace, then one or more (* ... *) blocks
# with optional whitespace between them, and nothing else.
COMMENT_ONLY = re.compile(r'^\s*(\(\*.*?\*\)\s*)*$')

def count_proof_lines(path: str) -> int:
    proof_open  = re.compile(r'^\s*Proof\b')
    proof_close = re.compile(r'^\s*(Qed|Admitted)\s*\.')

    total  = 0
    inside = False

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            is_comment_only = bool(COMMENT_ONLY.match(stripped))

            if not inside:
                if not is_comment_only and proof_open.match(stripped):
                    inside = True       # don't count the "Proof." line itself
            else:
                if not is_comment_only and proof_close.match(stripped):
                    inside = False      # don't count the "Qed."/"Admitted." line
                elif not is_comment_only:
                    total += 1          # count only non-comment lines inside block

    return total


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.v>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    try:
        n = count_proof_lines(path)
        print(f"{n} proof line(s) in '{path}'")
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)