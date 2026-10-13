import json, re

p = "/home/alex/hass_config/.storage/core.config_entries"
raw = open(p, "rb").read()
txt = raw.decode("utf-8", "replace")

print("=== RAW BYTES of generic camera titles ===")
for m in re.finditer(r'"domain":"generic".{0,900}?"title":"(.*?)"', txt, re.S):
    title = m.group(1)
    print("TITLE repr:", repr(title), "len:", len(title), "bytes:", title.encode("utf-8").hex())

print()
print("=== TRUE titles via python json ===")
d = json.loads(txt)
for e in d["data"]["entries"]:
    if e.get("domain") == "generic":
        o = e.get("options", {})
        print("entry:", e["entry_id"])
        print("  title:", repr(e.get("title")))
        print("  still_image_url:", o.get("still_image_url"))
        print("  stream_source:", o.get("stream_source"))
        print("  framerate:", o.get("advanced", {}).get("framerate"))
        print("  content_type:", o.get("content_type"))
