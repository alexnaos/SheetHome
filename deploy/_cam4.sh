#!/bin/bash
echo "===DASHBOARD-FILES-with-cameras==="
sudo -n grep -rlE "192_168_1_42|ym_karta_oblozhki" /home/alex/hass_config/.storage/lovelace* 2>/dev/null
echo "===HOW-CAMERAS-SHOWN-ON-DASH==="
sudo -n grep -oaE ".{0,70}(192_168_1_42|ym_karta_oblozhki).{0,110}" /home/alex/hass_config/.storage/lovelace* 2>/dev/null | head -30
echo "===STREAM-WEBRTC-CAMERA-in-configuration.yaml==="
sudo -n grep -nE "^stream|webrtc|^api:|default_config|camera:" /home/alex/hass_config/configuration.yaml
echo "===GO2RTC-STREAMS-ALIVE==="
curl -s --max-time 5 "http://127.0.0.1:1984/api/streams" | python3 -c "import sys,json; d=json.load(sys.stdin); [print(k, [p.get("url","ffmpeg-local") for p in v.get("producers",[])]) for k,v in d.items()]"
