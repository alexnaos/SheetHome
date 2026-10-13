import subprocess

def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== how many go2rtc processes? (port 1984 conflict?) ===")
r = sh("sudo -n ps -eo pid,ppid,comm,args | grep -iE 'go2rtc' | grep -v grep")
print(r.stdout or "  none")

print("=== who listens on 1984 ===")
r = sh("sudo -n ss -ltnp 2>/dev/null | grep 1984 || sudo -n netstat -ltnp 2>/dev/null | grep 1984")
print(r.stdout or "  (no info)")

print("=== go2rtc integration SETUP logs (added entities / errors) ===")
r = sh("sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc' | grep -iE 'camera|entit|setup|added|config|streams|error' | grep -viE 'i/o timeout' | tail -30")
print(r.stdout or "  (none)")

print("=== go2rtc integration: does it manage its own server or external? ===")
# config entry options
import json
d = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))
for e in d["data"]["entries"]:
    if e.get("domain") == "go2rtc":
        print("  entry_id:", e["entry_id"])
        print("  source:", e.get("source"), "| data:", e.get("data"), "| options:", e.get("options"))

print("=== all camera entity_ids + platform + disabled_by ===")
r = open("/home/alex/hass_config/.storage/core.entity_registry", encoding="utf-8").read()
import re
# crude parse of camera blocks
for m in re.finditer(r'"entity_id":\s*"(camera\.[^"]+)"(.{0,600})', r):
    eid = m.group(1); blk = m.group(2)
    plat = re.search(r'"platform":\s*"([^"]+)"', blk)
    dis = re.search(r'"disabled_by":\s*(?:"([^"]+)"|null)', blk)
    uniq = re.search(r'"unique_id":\s*"([^"]+)"', blk)
    print(f"  {eid:30s} platform={plat.group(1) if plat else '?':10s} disabled={dis.group(1) if dis and dis.group(1) else 'no'}")
