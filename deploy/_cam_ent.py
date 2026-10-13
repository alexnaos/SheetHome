import json
p = "/home/alex/hass_config/.storage/core.entity_registry"
d = json.load(open(p, encoding="utf-8"))
print("=== camera entities in registry ===")
for e in d["data"]["entities"]:
    if e.get("entity_id", "").startswith("camera."):
        print("entity_id:", e.get("entity_id"))
        print("  platform:", e.get("platform"))
        print("  unique_id:", e.get("unique_id"))
        print("  original_name:", repr(e.get("original_name")))
        print("  name:", repr(e.get("name")))
        print("  config_entry_id:", e.get("config_entry_id"))
        print()

