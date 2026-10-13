import json

raw = open("/home/alex/hass_config/.storage/core.entity_registry", encoding="utf-8").read()
d = json.loads(raw)

# find camera entities and print their registry record (name, unique_id, platform, etc.)
for ent in d["data"]["entities"]:
    if ent.get("entity_id", "").startswith("camera."):
        print("entity_id:", ent.get("entity_id"))
        print("  unique_id:", ent.get("unique_id"))
        print("  platform :", ent.get("platform"))
        print("  name     :", repr(ent.get("name")))
        print("  orig_name:", repr(ent.get("original_name")))
        print("  orig_icon:", ent.get("original_icon"))
        print("  device_id:", ent.get("device_id"))
        print()
