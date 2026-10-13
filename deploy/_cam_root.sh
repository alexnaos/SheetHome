#!/bin/bash
echo "===== 1. go2rtc.yaml (полностью) ====="
cat /home/alex/hass_config/go2rtc.yaml

echo
echo "===== 2. go2rtc / ffmpeg процессы ====="
sudo -n ps -eo pid,ppid,args | grep -iE 'go2rtc|ffmpeg' | grep -v grep

echo
echo "===== 3. manual go2rtc :1984 /api/streams ====="
curl -s --max-time 4 'http://127.0.0.1:1984/api/streams'
echo
echo "-----"

echo "===== 4. built-in go2rtc :18554 /api/streams ====="
curl -s --max-time 4 'http://127.0.0.1:18554/api/streams'
echo
echo "(пустой {} => встроенный go2rtc без потоков)"

echo
echo "===== 5. laptop_camera стабильность (5x frame.jpeg) ====="
for i in 1 2 3 4 5; do
  printf "try%s " "$i"
  curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s size=%{size_download}\n' --max-time 6 'http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera'
done

echo
echo "===== 6. cam2 стабильность (5x frame.jpeg) ====="
for i in 1 2 3 4 5; do
  printf "try%s " "$i"
  curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s size=%{size_download}\n' --max-time 6 'http://127.0.0.1:1984/api/frame.jpeg?src=cam2'
done

echo
echo "===== 7. cam2 прямой RTSP probe (кодек/разрешение/fps) ====="
sudo -n docker exec homeassistant ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 'rtsp://192.168.1.68:554/0/av0' 2>&1 | head -20

echo
echo "===== 8. ffmpeg в контейнере: есть ли h264-энкодер ====="
sudo -n docker exec homeassistant ffmpeg -hide_banner -encoders 2>/dev/null | grep -iE 'h264|libx264' | head

echo
echo "===== 9. go2rtc config entry в .storage ====="
sudo -n python3 - <<'PY'
import json
d=json.load(open('/home/alex/hass_config/.storage/core.config_entries',encoding='utf-8'))
for e in d['data']['entries']:
    if e.get('domain')=='go2rtc':
        print('entry_id',e['entry_id'])
        print('  title',e.get('title'))
        print('  data',e.get('data'))
        print('  options',e.get('options'))
print('go2rtc entries:', sum(1 for e in d['data']['entries'] if e.get('domain')=='go2rtc'))
PY
echo "===== DONE ====="
