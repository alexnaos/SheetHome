#!/usr/bin/env python3
import json, os, shutil

ST = "/home/alex/hass_config/.storage"
paths = {n: os.path.join(ST, f) for n, f in {
    "dev": "core.device_registry",
    "ent": "core.entity_registry",
    "cfg": "core.config_entεες".replace("εε",""),  # guard below
}.items() if False}

# explicit paths
p_dev = os.path.join(ST, "core.device_registry")
p_ent = os.path.join(ST, "core.entity_registry")
p_cfg = os.path.join(ST, "core.config_entries")

# backups
for p in (p_dev, p_ent, p_cfg):
    shutil.copy2(p, p + ".bak_before_names")
print("backups made")

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)
def dump(obj, p):
    with open(p, "w", encoding="utf-8") as f:   # python writes UTF-8 WITHOUT BOM
        json.dump(obj, f, ensure_ascii=False, indent=2)

NOUT_ID  = "01KQYY204CPYW0H7ZFAAFQJ9CN"   # laptop_camera
CAM68_ID = "01KV6A66BE65JGYTGTJDTT7EKC"   # cam2
STILL_NOUT = "http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera"

# --- device_registry: set name_by_user (persistent device rename) ---
dev = load(p_dev)
for d in dev["data"]["devices"]:
    ids = str(d.get("identifiers", ""))
    if NOUT_ID in ids:
        d["name_by_user"] = "NoutCamera"; d["name"] = "NoutCamera"
        print("dev NOUT ->", d["name_by_user"])
    elif CAM68_ID in ids:
        d["name_by_user"] = "Камера .68"; d["name"] = "Камера .68"
        print("dev CAM68 ->", d["name_by_user"])
dump(dev, p_dev)

# --- entity_registry: set names ---
ent = load(p_ent)
for e in ent["data"]["entities"]:
    eid = e.get("entity_id")
    if eid == "camera.192_168_1_42":
        e["name"] = "NoutCamera"; print("ent", eid, "-> ", e["name"])
    elif eid == "camera.192_168_1_42_3":
        e["name"] = "Камера .68"; print("ent", eid, "-> ", e["name"])
dump(ent, p_ent)

# --- config_entries: fix titles + add still_image_url to NoutCamera ---
cfg = load(p_cfg)
for e in cfg["data"]["entries"]:
    if e["entry_id"] == NOUT_ID:
        e["title"] = "NoutCamera"
        e.setdefault("options", {})["still_image_url"] = STILL_NOUT
        print("cfg NOUT title -> NoutCamera, still_image_url added")
    elif e["entry_id"] == CAM68_ID:
        e["title"] = "Камера .68"
        print("cfg CAM68 title ->", e["title"])
dump(cfg, p_cfg)

print("ALL WRITES DONE")
