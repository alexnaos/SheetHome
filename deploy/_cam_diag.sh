#!/bin/bash
echo "===WHERE GO2RTC LISTENS==="
sudo -n ss -ltnp 2>/dev/null | grep 1984 || echo "port 1984 not in ss"
echo
echo "===GO2RTC PROCESS==="
ps -eo pid,pcpu,pmem,args | grep -iE 'go2rtc' | grep -v grep | head -3
echo
echo "===FRAME SPEED: laptop_camera (currently yuv422p->h264)==="
timeout 4 curl -s -o /dev/null -w "laptop_camera frame.jpeg: http=%{http_code} t_total=%{time_total}s size=%{size_download}\n" "http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera"
echo "===FRAME SPEED: cam2 (RTSP .68, has still_image_url)==="
timeout 5 curl -s -o /dev/null -w "cam2 frame.jpeg: http=%{http_code} t_total=%{time_total}s size=%{size_download}\n" "http://127.0.0.1:1984/api/frame.jpeg?src=cam2"
echo "===FRAME SPEED: cam1 (RTSP .49)==="
timeout 5 curl -s -o /dev/null -w "cam1 frame.jpeg: http=%{http_code} t_total=%{time_total}s size=%{size_download}\n" "http://127.0.0.1:1984/api/frame.jpeg?src=cam1"
echo
echo "===GO2RTC STREAMS API==="
curl -s --max-time 4 "http://127.0.0.1:1984/api/streams"
echo
echo "===RTSP 554 REACHABILITY==="
for ip in 192.168.1.49 192.168.1.68; do
  if timeout 3 bash -c "cat < /dev/null > /dev/tcp/$ip/554" 2>/dev/null; then echo "$ip:554 OPEN"; else echo "$ip:554 CLOSED"; fi
done
