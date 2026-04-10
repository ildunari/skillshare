#!/usr/bin/env python3
"""
security_scanner.py
-------------------
Scan Swift code for common security issues:
- ATS disabled or broad exceptions (Info.plist pattern)
- Insecure hashes (MD5/SHA1) in security contexts
- Hard-coded secrets (naive regex)
- Weak Keychain accessibility (kSecAttrAccessibleAlways)
- Deprecated UIWebView usage or insecure WKWebView configuration

Usage:
  python security_scanner.py --path . --out security.json
"""
import argparse, os, re, json
from typing import List, Dict

ATS_ALLOW = re.compile(r"NSAppTransportSecurity|NSAllowsArbitraryLoads")
MD5_SHA1 = re.compile(r"\b(MD5|sha1|CC_MD5|kCCAlgorithmMD5)\b", re.IGNORECASE)
SECRET_RX = re.compile(r"(?i)(api[_-]?key|secret|token|pwd|password)\s*[:=]\s*['\"][A-Za-z0-9_\-\./+=]{12,}['\"]")
KEYCHAIN_WEAK = re.compile(r"kSecAttrAccessibleAlways\b")
UIWEBVIEW = re.compile(r"UIWebView\b")
WK_INSECURE = re.compile(r"WKWebView" )

def list_files(root: str) -> List[str]:
    out=[]
    for r,_,fs in os.walk(root):
        for f in fs:
            if f.endswith(('.swift', '.plist', '.strings', '.json')):
                out.append(os.path.join(r,f))
    return out

def analyze_file(path: str) -> List[Dict]:
    findings=[]
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            content=f.read()
    except Exception as e:
        return [{"file": path, "line": 0, "severity":"P1","rule":"read_error","message":str(e)}]

    if path.endswith('.plist') and ATS_ALLOW.search(content):
        findings.append({"file": path, "line": 1, "severity":"P1","rule":"ats_exceptions","message":"ATS exceptions found. Avoid NSAllowsArbitraryLoads; use per-domain pins."})

    for i, ln in enumerate(content.splitlines(), 1):
        if MD5_SHA1.search(ln):
            findings.append({"file": path, "line": i, "severity":"P1","rule":"insecure_hash","message":"Avoid MD5/SHA1; use CryptoKit (SHA256+) and modern constructions."})
        if SECRET_RX.search(ln) and '/Tests/' not in path:
            findings.append({"file": path, "line": i, "severity":"P1","rule":"hardcoded_secret","message":"Hard-coded secret detected. Move to secure storage/env with rotation."})
        if KEYCHAIN_WEAK.search(ln):
            findings.append({"file": path, "line": i, "severity":"P1","rule":"weak_keychain","message":"kSecAttrAccessibleAlways is insecure/deprecated. Use WhenUnlocked or AfterFirstUnlockThisDeviceOnly."})
        if UIWEBVIEW.search(ln):
            findings.append({"file": path, "line": i, "severity":"P2","rule":"uiwebview_deprecated","message":"UIWebView is deprecated. Migrate to WKWebView."})

    # WKWebView heuristic: warn to validate content mode/JS policies (not full static check)
    if 'WKWebView' in content and 'WKPreferences' not in content:
        findings.append({"file": path, "line": 1, "severity":"P3","rule":"wkwebview_hardening","message":"Harden WKWebView: limit JS, set contentMode, restrict navigation delegate."})

    return findings

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--path', default='.')
    ap.add_argument('--out', default='security.json')
    args=ap.parse_args()

    results=[]
    for fp in list_files(args.path):
        results.extend(analyze_file(fp))

    with open(args.out,'w',encoding='utf-8') as f:
        json.dump({"security": results}, f, indent=2)
    print(f"Wrote {len(results)} security findings to {args.out}")

if __name__=='__main__':
    main()
