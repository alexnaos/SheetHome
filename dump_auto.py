import json, sys
REG = sys.argv[1] if len(sys.argv) > 1 else "/config/.storage/core.entity_registry"
r = json.load(open(REG, encoding="utf-8"))
for e in r["data"]["entities"]:
    if e.get("domain") == "automation":
        print(e.get("entity_id"), "|", e.get("unique_id"), "| disabled=", bool(e.get("disabled_by")))
