import subprocess

def sh(c, t=8):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)
    return (r.stdout or "") + (r.stderr or "")

print("=== go2rtc: block in configuration.yaml ===")
print(sh("sudo -n grep -n -A20 '^go2rtc:' /home/alex/hass_config/configuration.yaml 2>/dev/null || echo 'NO go2rtc: block in configuration.yaml'"))
print()
print("=== any camera: platform blocks in configuration.yaml ===")
print(sh("sudo -n grep -n -A6 'platform: go2rtc\\|platform: generic\\|^camera:' /home/alex/hass_config/configuration.yaml 2>/dev/null || echo 'no camera: platform block'"))
print()
print("=== ALL files that mention 'camera.kamera_2' or 'camera.192_168_1_42' (source of stream defs) ===")
print(sh("sudo -n grep -rIl 'camera.kamera_2\\|camera.192_168_1_42' /home/alex/hass_config --include='*.yaml' 2>/dev/null | grep -v '\\.storage' | head"))
print()
print("=== current live streams on BUILT-IN go2rtc (18554) with auth ===")
# extract first temp yaml creds
creds = sh("sudo -n docker exec homeassistant sh -c \"head -30 /tmp/go2rtc-*/go2rtc_*.yaml 2>/dev/null | grep -E 'username|password' | head -2\"")
print("creds:", creds.strip()[:80])
print()
print("=== is manual go2rtc (1984) referenced by built-in? confirm chain: 1984 stream.mp4 now ===")
print(sh("curl -s -o /dev/null -w 'laptop stream.mp4(1984)=%{http_code}\\n' --max-time 4 'http://127.0.0.1:1984/api/stream.mp4?src=laptop_camera'"))
print(sh("curl -s -o /dev/null -w 'cam2 frame.jpeg(1984)=%{http_code}\\n' --max-time 6 'http://127.0.0.1:1984/api/frame.jpeg?src=cam2'"))
print()
print("=== generic camera config_entries (titles are the ??? ones) ===")
import json
d = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))
for e in d["data"]["entries"]:
    if e.get("domain") == "generic":
        print(" entry", e["entry_id"], "| title:", repr(e["title"]))
        print("   options:", json.dumps(e.get("options", {}), ensure_ascii=False))
