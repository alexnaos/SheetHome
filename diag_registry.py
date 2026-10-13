import json
reg=json.load(open("/config/.storage/core.entity_registry"))
ents=[e for e in reg["data"]["entities"] if e.get("entity_id","").startswith("device_tracker.")]
mt=[e for e in ents if "map_track" in e.get("unique_id","")]
print("device_tracker entities in registry:", len(ents))
print("map_track entries:", len(mt))
for e in mt[:8]:
    print(" ", e["entity_id"], "| unique_id:", e.get("unique_id"), "| disabled:", e.get("disabled_by"))
# также ищем по имени 'Карта'
kr=[e for e in ents if "Карта" in str(e.get("name",""))+str(e.get("original_name",""))]
print("name contains 'Карта':", len(kr))
for e in kr[:8]:
    print(" ", e["entity_id"], e.get("original_name"), e.get("disabled_by"))
