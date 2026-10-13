#!/bin/bash
echo "===ENSURE HA RUNNING==="
if sudo -n docker ps --format "{{.Names}}" | grep -q homeassistant; then
  echo HA_RUNNING
else
  sudo -n docker start homeassistant >/dev/null 2>&1 && echo HA_STARTED_BACK
fi
sleep 2
sudo -n docker ps --filter name=homeassistant --format "{{.Names}} | {{.Status}}"
echo
echo "===GO2RTC API streams==="
curl -s -m 5 http://127.0.0.1:1984/api/streams 2>&1 | head -40
echo
echo "===GO2RTC process==="
sudo -n ps -eo pid,comm,args 2>/dev/null | grep -i go2rtc | grep -v grep
echo
echo "===GO2RTC systemd==="
sudo -n systemctl list-units --type=service --all 2>/dev/null | grep -i go2rtc
echo
echo "===cam1 192.168.1.49==="
ping -c 2 -W 2 192.168.1.49 2>&1 | tail -3
(timeout 3 bash -c 'cat < /dev/null > /dev/tcp/192.168.1.49/554' 2>&1 && echo PORT_554_OPEN) || echo PORT_554_CLOSED
echo
echo "===cam2 192.168.1.68==="
ping -c 2 -W 2 192.168.1.68 2>&1 | tail -3
(timeout 3 bash -c 'cat < /dev/null > /dev/tcp/192.168.1.68/554' 2>&1 && echo PORT_554_OPEN) || echo PORT_554_CLOSED
echo
echo "===laptop /dev/video0==="
ls -la /dev/video0 2>&1
