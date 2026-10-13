#!/bin/bash
echo "===HA STATUS==="
sudo -n docker ps --filter name=homeassistant --format '{{.Names}} | {{.Status}}'
echo "===GO2RTC PROCESSES==="
sudo -n ps -eo pid,ppid,args | grep -i go2rtc | grep -v grep
echo "===LISTENING PORTS 1984/18554==="
sudo -n ss -ltnp 2>/dev/null | grep -E ':1984|:18554' || echo "none/ss-unavailable"
echo "===STREAMS via go2rtc API (1984)==="
curl -s --max-time 4 http://127.0.0.1:1984/api/streams 2>&1 | head -c 1200
echo
echo "===STREAMS via built-in go2rtc (18554)==="
curl -s --max-time 4 http://127.0.0.1:18554/api/streams 2>&1 | head -c 1200
echo
echo "===LIVE frame.jpeg laptop_camera (1984)==="
curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s size=%{size_download}B ctype=%{content_type}\n' --max-time 5 'http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera'
echo "===LIVE mjpeg laptop_camera (1984) 3s==="
curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s size=%{size_download}B ctype=%{content_type}\n' --max-time 3 'http://127.0.0.1:1984/api/stream.mjpeg?src=laptop_camera'
echo "===cam2 (.68) reachability==="
ping -c 2 -W 2 192.168.1.68 2>&1 | tail -3
echo "===cam2 frame.jpeg (.68 via go2rtc)==="
curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s size=%{size_download}B\n' --max-time 5 'http://127.0.0.1:1984/api/frame.jpeg?src=cam2'
echo "===cam1 (.49) ping==="
ping -c 2 -W 2 192.168.1.49 2>&1 | tail -3
echo "===HA go2rtc integration log (this boot)==="
sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc|platform=go2rtc|192_168_1_42|kamera' | tail -15
