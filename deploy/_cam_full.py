import json, subprocess

def sh(c, t=6):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== go2rtc.yaml (current) ===")
try:
    txt = open("/home/alex/hass_config/go2rtc.yaml", encoding="utf-8").read()
    print(txt)
except Exception as e:
    print("ERR:", e)

print("=== go2rtc config entry (port/url) ===")
d = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))
for e in d["data"]["entries"]:
    if e.get("domain") == "go2rtc":
        print("  data:", e.get("data"))
        print("  options:", e.get("options"))

print("=== any go2rtc-platform camera entities? ===")
r = open("/home/alex/hass_config/.storage/core.entity_registry", encoding="utf-8").read()
print("  platform go2rtc count:", r.count('"platform": "go2rtc"') + r.count('"platform":"go2rtc"'))
print("  camera.laptop count:", r.count("camera.laptop"))
print("  entity_ids starting camera.:")
import re
for m in sorted(set(re.findall(r'"entity_id":\s*"(camera\.[^"]+)"', r))):
    print("    ", m)

print("=== RAW bytes of laptop camera title (encoding check) ===")
i = d and open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8").read()
raw = i.encode("utf-8")
j = raw.find(b"\xd0\x9d")  # example
# find the title with ???????
k = i.find("laptop_camera")
print("  context around laptop_camera in config_entries:")
print("   ", repr(i[max(0,k-120):k+40]))
