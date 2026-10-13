#!/bin/bash
echo "===STREAM-WEBRTC-in-configuration.yaml==="
sudo -n grep -nE "^stream|webtc|^api:|default_config|camera:" /home/alex/hass_config/configuation.yaml
echo "===stream-dir-in-storage==="
sudo -n ls -la /home/alex/hass_config/.storage/ | grep -iE "stream|camera"
