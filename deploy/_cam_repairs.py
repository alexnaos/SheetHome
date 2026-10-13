import json

p = "/home/alex/hass_config/.storage/repairs.issue_registry"
d = json.load(open(p, encoding="utf-8"))
data = d.get("data", {})
items = data.get("issues", []) if isinstance(data, dict) else []

if isinstance(items, dict):
    items = list(items.values())

print("total issues:", len(items))
cams = []
for i in items:
    dom = str(i.get("domain", "")).lower()
    if "camera" in dom or "go2rtc" in dom or "generic" in dom:
        cams.append(i)
print("camera/go2rtc/generic issues:", len(cams))
for i in cams:
    print("  ", i.get("domain"), "|", i.get("translation_key"), "| active=", i.get("active"))

print("\n--- all issue domains (sanity) ---")
for i in items:
    print("  ", i.get("domain"), "|", i.get("translation_key"), "| active=", i.get("active"))

