#!/bin/bash
echo "===GO2RTC-YAML==="
sudo -n cat /home/alex/hass_config/go2rtc.yaml
echo
echo "===CAMERA-LINES-in-configuration.yaml==="
sudo -n grep -nE 'camera|go2rtc|stream|rtsp|webrtc' /home/alex/hass_config/configuration.yaml
echo
echo "===CAMERA-ENTITIES-from-registry==="
sudo -n python3 - <<'PYEOF'
import json
p="/home/alex/hass_config/.storage/core.entity_registry"
d=json.load(open(p))
for e in d["data"]["entities"]:
    eid=e.get("entity_id","")
    if eid.startswith("camera."):
        keys=("entity_id","unique_id","platform","original_name","name","device_id","disabled_by")
        print(json.dumps({k:e.get(k) for k in keys},ensure_ascii=False))
PYEOF
echo
echo "===GO2RTC/GENERIC/STREAM-CONFIG-ENTRIES==="
sudo -n python3 - <<'PYEOF'
import json
p="/home/alex/hass_config/.storage/core.config_entries"
d=json.load(open(p))
for e in d["data"]["entries"]:
    if e["domain"] in ("go2rtc","generic","stream"):
        print("DOMAIN:",e["domain"],"| TITLE:",e.get("title"))
        print("  DATA:",json.dumps(e.get("data",{}),ensure_ascii=False))
        print("  OPTIONS:",json.dumps(e.get("options",{}),ensure_ascii=False))
PYEOF
