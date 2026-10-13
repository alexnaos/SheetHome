#!/bin/bash
echo "===== go2rtc process ====="
pgrep -af go2rtc || echo "go2rtc NOT running"
echo
echo "===== go2rtc API /api/streams (localhost:1984) ====="
curl -s --max-time 4 http://127.0.0.1:1984/api/streams || echo "go2rtc API not reachable"
echo
echo "===== go2rtc version banner ====="
curl -s --max-time 4 http://127.0.0.1:1984/ -o /dev/null -w "http=%{http_code}\n" 2>&1 || true
echo
echo "===== RTSP camera reachability ====="
for ip in 192.168.1.49 192.168.1.68 192.168.1.42; do
  printf "ping %s: " "$ip"
  ping -c1 -W2 "$ip" >/dev/null 2>&1 && echo OK || echo FAIL
  printf "  port 554: "
  (timeout 3 bash -c "cat < /dev/null > /dev/tcp/$ip/554" 2>/dev/null && echo OPEN) || echo CLOSED
done
echo
echo "===== /dev/video0 present on this host? ====="
ls -la /dev/video0 2>&1 || echo "no /dev/video0"
echo
echo "===== lovelace dashboards using camera entities ====="
sudo -n grep -rlE "camera\.|go2rtc|webrtc" /home/alex/hass_config/.storage/lovelace* 2>/dev/null | while read f; do echo "FILE: $f"; done
