#!/usr/bin/env python3
"""scan_ports.py — find a responding localhost URL quickly.

Usage:
  python3 scan_ports.py
  python3 scan_ports.py --path /pricing
  python3 scan_ports.py --ports 3000,5173,8080
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from dataclasses import dataclass
from typing import Iterable, Optional


DEFAULT_PORTS = [3000, 5173, 8080, 8000, 4000, 4200, 5000, 6006]


@dataclass
class Result:
    port: int
    url: str
    status: Optional[int]
    ok: bool
    error: Optional[str]


def try_url(url: str, timeout: float) -> tuple[Optional[int], Optional[str]]:
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "ui-visual-polish/scan_ports",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return getattr(resp, "status", None), None
    except Exception as e:
        return None, str(e)


def scan(ports: Iterable[int], path: str, timeout: float) -> list[Result]:
    out: list[Result] = []
    for p in ports:
        url = f"http://localhost:{p}{path}"
        status, err = try_url(url, timeout=timeout)
        ok = status is not None and 200 <= status < 500
        out.append(Result(port=p, url=url, status=status, ok=ok, error=None if ok else err))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ports", type=str, default=",".join(map(str, DEFAULT_PORTS)))
    ap.add_argument("--path", type=str, default="/")
    ap.add_argument("--timeout", type=float, default=0.6)
    args = ap.parse_args()

    try:
        ports = [int(x.strip()) for x in args.ports.split(",") if x.strip()]
    except ValueError:
        print("Invalid --ports value. Example: 3000,5173,8080", file=sys.stderr)
        return 2

    path = args.path if args.path.startswith("/") else "/" + args.path

    results = scan(ports, path=path, timeout=args.timeout)
    ok = [r for r in results if r.ok]

    if ok:
        best = ok[0]
        print(best.url)
        return 0

    # Otherwise print a quick diagnostic table.
    for r in results:
        status = str(r.status) if r.status is not None else "-"
        err = (r.error or "").splitlines()[0][:120]
        print(f"{r.url:32}  status={status:>3}  err={err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
