#!/usr/bin/env python3
"""Environment state checker for one-click-office (开源).

Deterministic environment checks that decide whether a previously executed
step must be re-run. This script only READS the environment (existence,
timestamps, content, size); it never modifies any office file.

Usage:
  python check_step_state.py exists <path>
  python check_step_state.py newer <target> <source>
  python check_step_state.py contains <path> <keyword>
  python check_step_state.py fresh <path> --within <seconds>
  python check_step_state.py size <path> --min-bytes <N>

Exit codes:
  0 = condition TRUE  (e.g. file exists / target newer than source / keyword found)
  1 = condition FALSE
  2 = usage error / read error
"""

import argparse
import os
import sys
import time


def cmd_exists(args):
    ok = os.path.exists(args.path)
    print(f"{'EXISTS' if ok else 'MISSING'}: {args.path}")
    return 0 if ok else 1


def cmd_newer(args):
    if not os.path.exists(args.target):
        print(f"MISSING target: {args.target}")
        return 1
    if not os.path.exists(args.source):
        print(f"MISSING source: {args.source}")
        return 1
    target_mtime = os.path.getmtime(args.target)
    source_mtime = os.path.getmtime(args.source)
    ok = target_mtime >= source_mtime
    print(
        f"{'UP_TO_DATE' if ok else 'STALE'}: "
        f"target={args.target} (mtime={target_mtime:.0f}), "
        f"source={args.source} (mtime={source_mtime:.0f})"
    )
    return 0 if ok else 1


def _read_text(path):
    for enc in ("utf-8", "utf-8-sig", "gbk", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as fh:
                return fh.read()
        except (UnicodeDecodeError, OSError):
            continue
    return None


def cmd_contains(args):
    if not os.path.isfile(args.path):
        print(f"MISSING file: {args.path}")
        return 1
    text = _read_text(args.path)
    if text is None:
        print(f"UNREADABLE: {args.path}")
        return 1
    ok = args.keyword in text
    print(f"{'FOUND' if ok else 'NOT_FOUND'}: keyword={args.keyword!r} in {args.path}")
    return 0 if ok else 1


def cmd_fresh(args):
    if not os.path.exists(args.path):
        print(f"MISSING: {args.path}")
        return 1
    age = time.time() - os.path.getmtime(args.path)
    ok = age <= args.within
    print(f"{'FRESH' if ok else 'STALE'}: {args.path} age={age:.0f}s within={args.within}s")
    return 0 if ok else 1


def cmd_size(args):
    if not os.path.isfile(args.path):
        print(f"MISSING file: {args.path}")
        return 1
    size = os.path.getsize(args.path)
    ok = size >= args.min_bytes
    print(f"{'ENOUGH' if ok else 'TOO_SMALL'}: {args.path} size={size}B min={args.min_bytes}B")
    return 0 if ok else 1


def build_parser():
    p = argparse.ArgumentParser(
        description="one-click-office environment state checker (开源)"
    )
    sub = p.add_subparsers(dest="command", required=True)

    pe = sub.add_parser("exists", help="check whether a path exists")
    pe.add_argument("path")
    pe.set_defaults(func=cmd_exists)

    pn = sub.add_parser("newer", help="check whether target is newer than (or as new as) source")
    pn.add_argument("target")
    pn.add_argument("source")
    pn.set_defaults(func=cmd_newer)

    pc = sub.add_parser("contains", help="check whether a text file contains a keyword")
    pc.add_argument("path")
    pc.add_argument("keyword")
    pc.set_defaults(func=cmd_contains)

    pf = sub.add_parser("fresh", help="check whether a path was modified within N seconds")
    pf.add_argument("path")
    pf.add_argument("--within", type=float, required=True)
    pf.set_defaults(func=cmd_fresh)

    ps = sub.add_parser("size", help="check whether a file is at least N bytes")
    ps.add_argument("path")
    ps.add_argument("--min-bytes", type=int, required=True)
    ps.set_defaults(func=cmd_size)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        sys.exit(args.func(args))
    except OSError as exc:
        print(f"ERROR: {exc}")
        sys.exit(2)


if __name__ == "__main__":
    main()
