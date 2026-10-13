#!/bin/bash
echo "===STATUS==="
sudo -n docker ps --filter name=homeassistant --format '{{.Names}} | {{.Status}}'
echo
echo "===CAMERA/GO2RTC errors in this boot==="
sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc|camera|ffmpeg|still_image|invalid config|error setting up' | tail -30
echo
echo "===current ffmpeg for /dev/video0 (codec check)==="
sudo -n ps -eo args | grep -iE 'ffmpeg.*video0' | grep -v grep | head -3
echo
echo "===go2rtc.yaml now==="
sudo -n cat /home/alex/hass_config/go2rtc.yaml
