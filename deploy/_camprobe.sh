#!/bin/bash
echo "===RTSP reachability==="
for ip in 192.168.1.49 192.168.1.68; do
  if ping -c1 -W1 "$ip" >/dev/null 2>&1; then P=OK; else P=FAIL; fi
  if timeout 3 bash -c "cat </dev/null >/dev/tcp/$ip/554" 2>/dev/null; then S=OPEN; else S=CLOSED; fi
  echo "$ip  ping=$P  port554=$S"
done
echo
echo "===go2rtc stream detail (producers/consumers/bytes)==="
curl -s -m 6 http://127.0.0.1:1984/api/streams | python3 -m json.tool 2>/dev/null || curl -s -m 6 http://127.0.0.1:1984/api/streams
echo
echo "===ffmpeg processes (full args)==="
ps -eo pid,pcpu,etimes,args | grep '[f]fmpeg'
echo
echo "===load / uptime==="
cat /proc/loadavg; uptime
echo
echo "===go2rtc config as seen by HA container==="
sudo -n docker exec homeassistant sh -c 'cat /config/go2rtc.yaml' 2>/dev/null
