#!/bin/bash
echo "===configuration.yaml go2rtc section==="
sudo -n grep -nA20 '^go2rtc:' /home/alex/hass_config/configuration.yaml 2>/dev/null || echo "NO go2rtc: section in configuration.yaml"
echo
echo "===cameras.yaml==="
sudo -n cat /home/alex/hass_config/cameras.yaml 2>/dev/null || echo "no cameras.yaml"
echo
echo "===built-in go2rtc temp yaml (what 18554 loaded)==="
TMP=$(sudo -n ls -d /tmp/go2rtc-* 2>/dev/null | head -1)
echo "tmpdir=$TMP"
sudo -n cat "$TMP"/go2rtc_*.yaml 2>/dev/null | head -c 800
echo
echo "===packages: any go2rtc/camera platform==="
sudo -n grep -rniE 'platform:.*go2rtc|platform:.*generic|stream_source|go2rtc:' /home/alex/hass_config/configuration.yaml /home/alex/hass_config/packages/ 2>/dev/null | head -30
echo
echo "===go2rtc integration log (full, this boot)==="
sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc' | tail -25
