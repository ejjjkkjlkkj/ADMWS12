#!/usr/bin/env python3
"""Validate normalized ADMWS12 inventory without modifying source data."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

SENSITIVE_KEY=re.compile(r"(?i)(guid|uuid|serial|processorid|pnpdeviceid|macaddress|objectid|deviceid)")
SENSITIVE_VALUE=re.compile(r"(?i)(guid|uuid|serial|deviceid|objectid)")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,default=Path("data/normalized"))
    a=ap.parse_args()
    errors=[]; files=records=empty=duplicates=0
    for p in sorted(a.input.rglob("*.jsonl")):
        files+=1; seen=set()
        for n,line in enumerate(p.read_text(encoding="utf-8",errors="replace").splitlines(),1):
            if not line.strip(): continue
            try: obj=json.loads(line)
            except Exception as e:
                errors.append(f"{p}:{n}: invalid JSON: {e}"); continue
            records+=1
            if not isinstance(obj,dict) or not obj:
                empty+=1; errors.append(f"{p}:{n}: empty/non-object record"); continue
            canon=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))
            if canon in seen: duplicates+=1; errors.append(f"{p}:{n}: duplicate record")
            seen.add(canon)
            for k,v in obj.items():
                if SENSITIVE_KEY.search(k): errors.append(f"{p}:{n}: sensitive key retained: {k}")
                if isinstance(v,str) and SENSITIVE_VALUE.search(v): errors.append(f"{p}:{n}: possible sensitive identifier in value")
    print(json.dumps({"files":files,"records":records,"empty_records":empty,"duplicates":duplicates,"errors":len(errors)},indent=2))
    for e in errors[:100]: print(e)
    return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())
