#!/usr/bin/env python3
import json, os, subprocess

def sh(cmd):
    return subprocess.run(["bash","-lc",cmd], capture_output=True, text=True).stdout

# 1) entity registry blocks for the camera entities
er = "/home/alex/hass_config/.storage/core.entity_registry"
with open(er, encoding="utf-8") as f:
    erdata = json.load(f)
print("=== CAMERA ENTITY REGISTRY ===")
for ent in erdata["data"]["entities"]:
    if ent.get("entity_id","").startswith("camera."):
        print("entity_id    :", ent["entity_id"])
        print("platform     :", ent.get("platform"))
        print("unique_id    :", ent.get("unique_id"))
        print("name         :", repr(ent.get("name")))
        print("original_name:", repr(ent.get("original_name")))
        print("disabled_by  :", ent.get("disabled_by"))
        print("---")

# 2) go2rtc integration temp config
print("=== go2rtc integration temp config ===")
tmp = sh("find /tmp -maxdepth 2 -iname 'go2rtc*.yaml' 2>/dev/null | head -3")
for p in tmp.split():
    print("---", p, "---")
    try:
        with open(p, encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print("read err:", e)

# 3) any go2rtc-platform entities?
print("=== go2rtc-platform entities? ===")
found = False
for ent in erdata["data"]["entities"]:
    if ent.get("platform") == "go2rtc":
        print(ent["entity_id"], "|", repr(ent.get("original_name")))
        found = True
if not found:
    print("NONE (go2rtc integration created no entities)")

# 4) go2rtc integration config entry
print("=== go2rtc config entry ===")
ce = "/home/alex/hass_config/.storage/core.config_entries"
with open(ce, encoding="utf-8") as f:
    cedata = json.load(f)
for e in cedata["data"]["entries"]:
    if e.get("domain") == "go2rtc":
        print("entry_id:", e["entry_id"], "| title:", repr(e.get("title")), "| disabled_by:", e.get("disabled_by"))
        print("data    :", json.dumps(e.get("data", {}), ensure_ascii=False))
        print("options :", json.dumps(e.get("options", {}), ensure_ascii=False))

# 5) CPU info (HW encode?)
print("=== CPU ===")
print(sh("grep -c '^processor' /proc/cpuinfo").strip(), "cores |", sh("grep -m1 'model name' /proc/cpuinfo | cut -d: -f2").strip())
