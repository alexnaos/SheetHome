#!/bin/bash
echo "===GO2RTC-WEBRTC-CHECK==="
curl -s -o /dev/null -w "webrtc POST endpoint http=%{http_code}\n" --max-time 8 -X POST "http://127.0.0.1:1984/api/webrtc?src=cam2"
echo "===GO2RTC-API-ROOT==="
curl -s --max-time 5 "http://127.0.0.1:1984/" | head -c 300
echo
echo "===DASHBOARDS-referencing-cameras==="
sudo -n grep -rlE "192_168_1_42|ym_karta_oblozhki" /home/alex/hass_config/.storage/lovelace* 2>/dev/null
echo "===HOW-camera-shown (context)==="
sudo -n grep -oaE ".{0,80}(192_168_1_42|192_168_1_42_3).{0,120}" /home/alex/hass_config/.storage/lovelace* 2>/dev/null | head -20
echo "===STREAM-component-in-configuration.yaml==="
sudo -n grep -nE "^stream|webrtc|^api|^default_config|camera:" /home/alex/hass_config/configuration.yaml
