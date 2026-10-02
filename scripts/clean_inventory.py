#!/usr/bin/env python3
"""ADMWS12: nettoyage strict et normalisation de l'inventaire.
Les sources brutes ne sont jamais modifiées.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

DROP_EXACT = {
    "PSComputerName","CimClass","CimInstanceProperties","CimSystemProperties",
    "CreationClassName","SystemCreationClassName","SystemName","InstallDate",
    "ErrorCleared","ErrorDescription","LastErrorCode","OtherIdentifyingInfo",
    "PassThroughClass","PassThroughIds","PassThroughNamespace","PassThroughServer",
    "NetAdapter","NetCompartment","NetIPv4Interface","NetIPv6Interface","NetProfile",
}
DROP_PATTERNS = tuple(re.compile(x, re.I) for x in (
    r"^ObjectId$","^DeviceID$","^InstanceIdentifier$","^UniqueId$",
    r"^Guid$","^SerialNumber$","^ProcessorId$","^PNPDeviceID$","^MACAddress$",
))

def scalar(v: str) -> Any:
    v=v.strip()
    if not v: return None
    if v.lower() in ("true","false"): return v.lower()=="true"
    if re.fullmatch(r"-?\d+",v):
        try: return int(v)
        except ValueError: pass
    if re.fullmatch(r"-?\d+\.\d+",v):
        try: return float(v)
        except ValueError: pass
    return v

def parse(text: str) -> list[dict[str,Any]]:
    out=[]; cur={}
    for raw in text.splitlines():
        line=raw.rstrip()
        if not line.strip():
            if cur: out.append(cur); cur={}
            continue
        if ":" not in line: continue
        key,val=line.split(":",1); key=key.strip(); val=val.strip()
        if not key or key in DROP_EXACT or any(p.search(key) for p in DROP_PATTERNS): continue
        if not val: continue
        value=scalar(val)
        if key in cur:
            out.append(cur); cur={}
        cur[key]=value
    if cur: out.append(cur)
    return out

def clean(r: dict[str,Any]) -> dict[str,Any]:
    o={}
    for k,v in r.items():
        if v is None: continue
        if isinstance(v,str):
            v=v.strip()
            if not v: continue
            # Ne pas conserver les valeurs qui sont manifestement des identifiants.
            if re.search(r"(?i)(^|[\\#])(?:guid|uuid|serial|deviceid|objectid)",v): continue
            if len(v)>1024: continue
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{1,63}",k):
            o[k]=v
    return o

def dedup(rows):
    seen=set(); out=[]
    for r in rows:
        if not r: continue
        s=json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":"))
        if s not in seen: seen.add(s); out.append(r)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,default=Path("research/platform-inventory"))
    ap.add_argument("--output",type=Path,default=Path("data/normalized"))
    a=ap.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for src in sorted(a.input.rglob("*.txt")):
        rows=dedup([clean(r) for r in parse(src.read_text(encoding="utf-8",errors="replace"))])
        rel=src.relative_to(a.input); dst=a.output/rel.with_suffix(".jsonl")
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in rows),encoding="utf-8")
        manifest.append({"source":rel.as_posix(),"output":dst.relative_to(a.output).as_posix(),"records":len(rows)})
    (a.output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Fichiers traités : {len(manifest)}")
    print(f"Sortie : {a.output}")
if __name__=="__main__": main()
