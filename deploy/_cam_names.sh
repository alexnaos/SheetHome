#!/bin/bash
echo "===REAL CAMERA TITLES from config_entries==="
python3 - <<'PY'
import json
p="/home/alex/hass_config/.storage/core.config_entries"
d=json.load(open(p))
for e in d["data"]["entries"]:
    if e["domain"] in ("generic","onvif","rtsp_camera","go2rtc"):
        print("domain=%s | title=%s | entry=%s" % (e["domain"], e["title"], e["entry_id"]))
        o=e.get("options") or {}
        for k in ("stream_source","still_image_url","content_type"):
            if k in o: print("    %s=%s" % (k,o[k]))
        if o.get("advanced"):
            print("    advanced=%s" % json.dumps(o["advanced"]))
PY
echo
echo "===REGISTRY friendly_name for camera.*==="
python3 - <<'PY'
import json
p="/home/alex/hass_config/.storage/core.entity_registry"
d=json.load(open(p))
for e in d["data"]["entities"]:
    if e.get("entity_id","").startswith("camera."):
        print("entity_id=%s | name=%s | platform=%s | orig=%s" % (
            e.get("entity_id"), e.get("name"), e.get("platform"),
            (e.get("original_name") or "")))
PY
