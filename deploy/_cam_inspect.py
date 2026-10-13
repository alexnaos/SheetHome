import json
CE="/home/alex/hass_config/.storage/core.config_entries"
ER="/home/alex/hass_config/.storage/core.entity_registry"
ce=json.load(open(CE,encoding="utf-8"))
er=json.load(open(ER,encoding="utf-8"))
print("=== generic config entries (full options) ===")
for e in ce["data"]["entries"]:
    if e.get("domain")=="generic":
        print("entry_id:",e["entry_id"])
        print("  title:",repr(e.get("title")))
        print("  options:",json.dumps(e.get("options",{}),ensure_ascii=False))
print("=== camera entities in registry ===")
for ent in er["data"]["entities"]:
    eid=ent.get("entity_id","")
    if eid.startswith("camera."):
        print(" ",eid,"| platform:",ent.get("platform"),"| name:",repr(ent.get("name")),"| original_name:",repr(ent.get("original_name")),"| unique_id:",ent.get("unique_id"))
