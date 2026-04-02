"""
Shared utilities for HTTP requests, caching, rate limiting, and file IO.
"""
import os
import time
import json
import hashlib
import random
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, Callable
import requests
from requests.adapters import HTTPAdapter, Retry

DEFAULT_UA = "research-discovery-agent/1.0 (+https://example.invalid)"
OUT_DIR = os.environ.get("RDA_OUT_DIR", "./out")

def ensure_out(path: str = OUT_DIR) -> None:
    os.makedirs(path, exist_ok=True)

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def json_dump(obj: Any, path: str) -> None:
    ensure_out(os.path.dirname(path) or OUT_DIR)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def json_load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def session_with_retries(total: int = 3, backoff: float = 0.3) -> requests.Session:
    s = requests.Session()
    retries = Retry(total=total, backoff_factor=backoff, status_forcelist=[429, 500, 502, 503, 504])
    s.headers.update({"User-Agent": DEFAULT_UA})
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s

def get_json(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 20) -> Dict[str, Any]:
    s = session_with_retries()
    h = headers or {}
    r = s.get(url, params=params, headers=h, timeout=timeout)
    r.raise_for_status()
    return r.json()

def get_html(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 20) -> str:
    s = session_with_retries()
    h = headers or {}
    r = s.get(url, params=params, headers=h, timeout=timeout)
    r.raise_for_status()
    return r.text

def polite_sleep(min_s: float = 0.7, max_s: float = 1.8) -> None:
    time.sleep(random.uniform(min_s, max_s))

def getenv(name: str, default: Optional[str] = None, required: bool = False) -> str:
    val = os.environ.get(name, default)
    if required and not val:
        raise RuntimeError(f"Missing required environment var: {name}")
    return val

@dataclass
class Score:
    value: float
    detail: Dict[str, float]

def bounded(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def normalize(value: float, min_v: float, max_v: float) -> float:
    if max_v == min_v:
        return 0.0
    return (value - min_v) / (max_v - min_v)

def write_csv(rows, header, path):
    import csv
    ensure_out(os.path.dirname(path) or OUT_DIR)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
