import json

d = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))

print("=== GO2RTC native integration present? ===")
found = False
for e in d["data"]["entries"]:
    if e.get("domain") == "go2rtc":
        found = True
        print("  YES go2rtc entry:", e["entry_id"], "| title:", e["title"])
print("  go2rtc_entry_present =", found)

print()
print("=== generic (MJPEG) cameras ===")
for e in d["data"]["entries"]:
    if e.get("domain") == "generic":
        o = e["options"]
        print("  title:", repr(e["title"]))
        print("    stream_source:", o.get("stream_source"))
        print("    still_image_url:", o.get("still_image_url"))
        print("    framerate:", o.get("advanced", {}).get("framerate"))
