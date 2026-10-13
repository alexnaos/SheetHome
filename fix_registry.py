import json, shutil, sys
REG = sys.argv[1] if len(sys.argv) > 1 else "/config/.storage/core.entity_registry"
ACTIVE={"map_keenetic_state","map_keenetic_reconcile"}
shutil.copy(REG, REG+".bak_cleanup")
with open(REG, encoding="utf-8") as f:
    reg = json.load(f)
ents = reg["data"]["entities"]
before = len(ents)
def stale(e):
    if e.get("domain")!="automation": return False
    uid=e.get("unique_id") or ""
    eid=e.get("entity_id","")
    # удаляем только map_* автоматизации, которых больше нет в активном конфиге
    return uid.startswith("map_") and uid not in ACTIVE and eid.startswith("automation.map_")
reg["data"]["entities"]=[e for e in ents if not stale(e)]
after=len(reg["data"]["entities"])
with open(REG,"w",encoding="utf-8") as f:
    json.dump(reg,f,indent=2,ensure_ascii=False)
print(f"registry: {before} -> {after} (removed {before-after})")

