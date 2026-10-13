import json

path = "/home/alex/hass_config/.storage/core.config_entries"
raw = open(path, "rb").read()

bom = raw[:3] == b"\xef\xbb\xbf"
print("has_BOM:", bom)
print("len:", len(raw))

d = json.loads(raw.decode("utf-8"))
print("JSON_VALID")
print("entries:", len(d["data"]["entries"]))

for e in d["data"]["entries"]:
    if e.get("domain") == "generic":
        o = e["options"]
        print(" ", e["entry_id"], "| stream:", o.get("stream_source"),
              "| still:", o.get("still_image_url"))
