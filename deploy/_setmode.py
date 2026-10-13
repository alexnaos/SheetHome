import json
import shutil

p = "/home/alex/hass_config/.storage/core.config_entries"

with open(p, "r", encoding="utf-8") as f:
    data = json.load(f)

changed = False
for e in data["data"]["entries"]:
    if e.get("domain") == "sonoff":
        old = e.get("options", {}).get("mode")
        e.setdefault("options", {})["mode"] = "cloud"
        print(f"sonoff: mode {old} -> cloud")
        changed = True

if not changed:
    print("WARNING: sonoff entry not found!")

# Write WITHOUT BOM (utf-8, not utf-8-sig). json.dump guarantees valid JSON.
with open(p, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Verify round-trip
with open(p, "r", encoding="utf-8") as f:
    chk = json.load(f)
n = len(chk["data"]["entries"])
smode = [e["options"].get("mode") for e in chk["data"]["entries"] if e.get("domain") == "sonoff"]
print(f"VERIFY: entries={n} sonoff_mode={smode} json=OK")
