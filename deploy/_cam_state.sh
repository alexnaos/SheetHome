#!/bin/bash
echo "===== 1. ps go2rtc ====="
ps -eo pid,ppid,args | grep -i go2rtc | grep -v grep
echo
echo "===== 2. how manual go2rtc launches ====="
echo "--- systemd units ---"; systemctl list-unit-files 2>/dev/null | grep -i go2rtc
echo "--- crontab ---"; crontab -l 2>/dev/null | grep -i go2rtc
echo "--- rc.local ---"; grep -i go2rtc /etc/rc.local 2>/dev/null
echo "--- yaml launch refs ---"; grep -rnE "go2rtc-1.9.9|1984|go2rtc.yaml|go2rtc " /home/alex/hass_config/*.yaml 2>/dev/null | head -30
echo "--- bashrc/profile ---"; grep -i go2rtc /home/alex/.bashrc /home/alex/.profile 2>/dev/null
echo
echo "===== 3. go2rtc camera.py (how WebRTC cameras are created) ====="
sudo -n docker exec homeassistant bash -lc 'D=$(find / -path "*components/go2rtc/camera.py" 2>/dev/null | head -1); echo "PATH=$D"; cat "$D"'
echo
echo "===== 4. go2rtc __init__.py (auto-read yaml? auto-create cameras?) ====="
sudo -n docker exec homeassistant bash -lc 'D=$(find / -path "*components/go2rtc/__init__.py" 2>/dev/null | head -1); cat "$D"'
