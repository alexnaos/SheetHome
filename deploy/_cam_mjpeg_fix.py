import json

path = "/home/alex/hass_config/.storage/core.config_entries"
d = json.load(open(path, encoding="utf-8"))

changed = 0
for e in d["data"]["entries"]:
    if e.get("domain") != "generic":
        continue
    o = e["options"]
    ss = o.get("stream_source", "")
    if "stream.mp4" in ss:
        o["stream_source"] = ss.replace("stream.mp4", "stream.mjpeg")
        changed += 1
        print(f"FIXED {e['entry_id']}: {ss} -> {o['stream_source']}")
    else:
        print(f"SKIP  {e['entry_id']}: {ss}")

# save WITHOUT BOM (the BOM lesson)
data = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
with open(path, "w", encoding="utf-8") as f:
    f.write(data)

print(f"TOTAL CHANGED: {changed}")
