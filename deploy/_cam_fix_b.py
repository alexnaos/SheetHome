import json, sys, shutil, time

BASE = "/home/alex/hass_config/.storage"
CE = f"{BASE}/core.config_entries"
ER = f"{BASE}/core.entity_registry"
APPLY = len(sys.argv) > 1 and sys.argv[1] == "apply"

ce = json.load(open(CE, encoding="utf-8"))
er = json.load(open(ER, encoding="utf-8"))

# нормальные имена
NAME_NOUT = "NoutCamera"
NAME_CAM2 = "Camera 68"

changes = []

# --- config_entries: title + framerate ---
for e in ce["data"]["entries"]:
    if e.get("domain") == "generic":
        eid = e["entry_id"]
        if eid == "01KQYY204CPYW0H7ZFAAFQJ9CN":  # NoutCamera
            if e.get("title") != NAME_NOUT:
                changes.append(("CE.title", eid, repr(e.get("title")), repr(NAME_NOUT)))
                e["title"] = NAME_NOUT
            adv = e.setdefault("options", {}).setdefault("advanced", {})
            old_fr = adv.get("framerate")
            if old_fr != 5.0:
                changes.append(("CE.framerate", eid, old_fr, 5.0))
                adv["framerate"] = 5.0
        elif eid == "01KV6A66BE65JGYTGTJDTT7EKC":  # cam2 .68
            if e.get("title") != NAME_CAM2:
                changes.append(("CE.title", eid, repr(e.get("title")), repr(NAME_CAM2)))
                e["title"] = NAME_CAM2

# --- entity_registry: name + original_name ---
ents = er["data"]["entities"]
def each_ent():
    if isinstance(ents, dict):
        for eid, ent in ents.items():
            yield eid, ent
    else:
        for ent in ents:
            yield ent.get("entity_id"), ent

for eid, ent in each_ent():
    if eid == "camera.192_168_1_42":  # NoutCamera
        if ent.get("original_name") != NAME_NOUT:
            changes.append(("ER.original_name", eid, repr(ent.get("original_name")), repr(NAME_NOUT)))
            ent["original_name"] = NAME_NOUT
        # name уже 'NoutCamera' — оставляем, но подстрахуемся
        if ent.get("name") is None:
            ent["name"] = NAME_NOUT
    elif eid == "camera.192_168_1_42_3":  # cam2 .68
        if ent.get("name") != NAME_CAM2:
            changes.append(("ER.name", eid, repr(ent.get("name")), repr(NAME_CAM2)))
            ent["name"] = NAME_CAM2
        if ent.get("original_name") != NAME_CAM2:
            changes.append(("ER.original_name", eid, repr(ent.get("original_name")), repr(NAME_CAM2)))
            ent["original_name"] = NAME_CAM2

print("MODE:", "APPLY" if APPLY else "DRY-RUN")
print("changes found:", len(changes))
for c in changes:
    print("  ", c[0], "|", c[1], "|", c[2], "->", c[3])

if not APPLY:
    print("(dry-run, nothing written)")
    sys.exit(0)

# backups (timestamped)
ts = time.strftime("%Y%m%d_%H%M%S")
for f in (CE, ER):
    shutil.copy2(f, f + f".bak_camfix_{ts}")
print("backups written, ts =", ts)

# write UTF-8 WITHOUT BOM (python default, ensure_ascii=False keeps utf-8 text)
with open(CE, "w", encoding="utf-8") as fh:
    json.dump(ce, fh, ensure_ascii=False, indent=2)
with open(ER, "w", encoding="utf-8") as fh:
    json.dump(er, fh, ensure_ascii=False, indent=2)

# verify (reload + check no BOM)
for f in (CE, ER):
    b = open(f, "rb").read(3)
    bom = (b == b"\xef\xbb\xbf")
    json.load(open(f, encoding="utf-8"))  # will raise if invalid
    print(f"VERIFY {f}: BOM={bom} json_ok=True")

print("DONE")
