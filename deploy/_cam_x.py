import json

ce = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))

print("=== GENERIC CAMERA ENTRIES ===")
for e in ce["data"]["entries"]:
    if e.get("domain") == "generic":
        o = e.get("options", {})
        print(f"title={e['title']!r}")
        print(f"  still_image_url = {o.get('still_image_url')}")
        print(f"  stream_source   = {o.get('stream_source')}")
        print(f"  framerate       = {o.get('advanced',{}).get('framerate')}")
        print(f"  content_type    = {o.get('content_type')}")
        print(f"  auth            = {o.get('advanced',{}).get('authentication')}")

print()
print("=== go2rtc CONFIG ENTRY (native integration) ===")
found = False
for e in ce["data"]["entries"]:
    if e.get("domain") == "go2rtc":
        found = True
        print("  title:", e.get("title"))
        print("  options:", e.get("options"))
        print("  source:", e.get("source"))
if not found:
    print("  NO go2rtc native config entry!")

print()
print("=== ALL DOMAINS PRESENT ===")
doms = sorted(set(e["domain"] for e in ce["data"]["entries"]))
print(" ", ", ".join(doms))
