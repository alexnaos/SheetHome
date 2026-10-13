#!/usr/bin/env python3
import json, glob, os

# 1) generic camera config entries
ce = "/home/alex/hass_config/.storage/core.config_entries"
with open(ce, encoding="utf-8") as f:
    data = json.load(f)
print("=== GENERIC CAMERA CONFIG ENTRIES ===")
for e in data["data"]["entries"]:
    if e.get("domain") == "generic":
        print("entry_id :", e["entry_id"])
        print("title repr:", repr(e.get("title")))
        print("title utf8 hex:", e.get("title","").encode("unicode_escape").decode())
        print("options  :", json.dumps(e.get("options", {}), ensure_ascii=False))
        print("---")

print()
print("=== go2rtc.yaml ===")
gp = "/home/alex/hass_config/go2rtc.yaml"
if os.path.exists(gp):
    with open(gp, encoding="utf-8") as f:
        print(f.read())
print("=== go2rtc process ===")
os.system("ps -eo pid,comm,args | grep -i '[g]o2rtc' || echo 'go2rtc NOT running'")
