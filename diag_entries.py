import json
ce=json.load(open("/config/.storage/core.config_entries"))
tmpl=[e for e in ce["data"]["entries"] if e.get("domain")=="template"]
print("template config_entries:", len(tmpl))
for e in tmpl:
    print(" ", e.get("title"), "| source:", e.get("source"), "| disabled:", e.get("disabled_by"), "| entry_id:", e.get("entry_id"))
# проверим также все домены с source=package
pk=[e for e in ce["data"]["entries"] if e.get("source")=="package"]
print("entries from package:", len(pk))
for e in pk[:10]:
    print(" ", e.get("domain"), e.get("title"))
