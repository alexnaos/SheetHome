import json
reg=json.load(open("/config/.storage/core.entity_registry"))
ents=reg["data"]["entities"]
for e in ents:
    eid=e.get("entity_id","")
    if eid.startswith(("device_tracker.","person.")):
        print(eid, "| platform:", e.get("platform"), "| disabled:", e.get("disabled_by"), "| name:", e.get("original_name"))
