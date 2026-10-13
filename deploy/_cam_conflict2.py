import subprocess

def sh(c, t=8):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)
    return (r.stdout or "") + (r.stderr or "")

print("=== built-in go2rtc 18554 /api/streams (raw) ===")
print(sh("curl -s --max-time 4 http://127.0.0.1:18554/api/streams"))
print("=== built-in 18554 /api ===")
print(sh("curl -s --max-time 4 http://127.0.0.1:18554/api | head -c 300"))
print()
print("=== all go2rtc processes (pid, parent, cmd) ===")
print(sh("sudo -n ps -eo pid,ppid,comm,args | grep -i go2rtc | grep -v grep"))
print()
print("=== how is manual go2rtc-1.9.9 started? (systemd service?) ===")
print(sh("sudo -n systemctl list-units --type=service --all 2>/dev/null | grep -i go2rtc || echo 'no systemd go2rtc service'"))
print("--- any unit file? ---")
print(sh("sudo -n ls -la /etc/systemd/system/*go2rtc* 2>/dev/null || echo 'no unit file'"))
print()
print("=== does HA integration read go2rtc.yaml? check config_entries go2rtc entry ===")
import json
d = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))
for e in d["data"]["entries"]:
    if e.get("domain") == "go2rtc":
        print("go2rtc entry:", e["entry_id"], "| title:", e["title"], "| source:", e.get("source"))
        print("   data:", json.dumps(e.get("data", {}), ensure_ascii=False))
        print("   options:", json.dumps(e.get("options", {}), ensure_ascii=False))
print()
print("=== port 1984 owner & 18554 owner ===")
print(sh("sudo -n ss -ltnp 2>/dev/null | grep -E ':1984|:18554' || echo 'ss not showing ports'"))
