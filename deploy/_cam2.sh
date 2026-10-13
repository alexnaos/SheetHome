#!/bin/bash
echo ===LATENCY-laptop===
curl -s -o /dev/null -w "laptop total=%{time_total}s http=%{http_code} bytes=%{size_download}\n" --max-time 25 "http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera"
echo ===LATENCY-cam2===
curl -s -o /dev/null -w "cam2 total=%{time_total}s http=%{http_code} bytes=%{size_download}\n" --max-time 25 "http://127.0.0.1:1984/api/frame.jpeg?src=cam2"
echo ===MOJIBAKE-ORIGINAL-NAME===
sudo -n grep -a -o "original_name[^,]*" /home/alex/hass_config/.storage/core.entity_registry | grep -a -i -E "Nout|Cam|192|Ноут|Камер"
echo ===HEX-FIRST-CAMERA-NAME===
sudo -n python3 - <<'PYEOF'
import json
p="/home/alex/hass_config/.storage/core.entity_registry"
d=json.load(open(p, encoding="utf-8"))
for e in d["data"]["entities"]:
    eid=e.get("entity_id","")
    if eid.startswith("camera."):
        on=e.get("original_name")
        nm=e.get("name")
        print(eid, "| original_name hex:", (on or "").encode("utf-8").hex(), "| name:", nm)
PYEOF
