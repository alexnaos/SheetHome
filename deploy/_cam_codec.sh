#!/bin/bash
echo "=== 1) ffmpeg доступен? (нужен для H.264/WebRTC) ==="
which ffmpeg && ffmpeg -version 2>/dev/null | head -1 || echo "ffmpeg NOT in PATH"
echo "--- libx264? ---"
ffmpeg -hide_banner -encoders 2>/dev/null | grep -iE 'libx264|h264' | head -5 || echo "(нет h264 энкодера / нет ffmpeg)"
echo
echo "=== 2) go2rtc-1.9.9 (ручной, :1984) — тест H.264 для вебки ==="
echo "--- 2a. stream.mp4 (h264) laptop_camera, текущий mjpeg-конфиг ---"
curl -s -o /dev/null -w 'mp4 http=%{http_code} time=%{time_total}s type=%{content_type}\n' --max-time 4 'http://127.0.0.1:1984/api/stream.mp4?src=laptop_camera'
echo "--- 2b. пробуем добавить h264-кодек на лету через ffmpeg источник (без правки yaml) ---"
curl -s -o /dev/null -w 'mp4-h264 http=%{http_code} time=%{time_total}s\n' --max-time 6 'http://127.0.0.1:1984/api/stream.mp4?src=ffmpeg:device%3Fvideo=/dev/video0%23input=yuv422p%23video=h264%23size=640x480%23aspeed=5' 2>&1 || echo "(провал)"
echo
echo "=== 3) cam2 (.68) — кодек и h264-транскод ==="
curl -s --max-time 4 'http://127.0.0.1:1984/api/streams' | python3 -c 'import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get("cam2",{}),ensure_ascii=False)[:400])' 2>/dev/null || echo "(cam2 нет)"
echo "--- cam2 h264-транскод mp4 ---"
curl -s -o /dev/null -w 'cam2-mp4 http=%{http_code} time=%{time_total}s\n' --max-time 6 'http://127.0.0.1:1984/api/stream.mp4?src=cam2' 2>&1 || echo "(провал)"
echo
echo "=== 4) встроенный go2rtc HA (:18554) — с авторизацией из логов ==="
sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc' | grep -iE 'api|url|token|localhost|11984|18554' | tail -5
echo
echo "=== 5) go2rtc __init__.py — как cameras.yaml/stream маппится (grep) ==="
sudo -n docker exec homeassistant sh -c 'grep -nE "go2rtc.yaml|load_yaml|def async_setup_entry|CONF_URL|external|WebRTCProvider|camera" /usr/src/homeassistant/homeassistant/components/go2rtc/__init__.py' 2>/dev/null | head -30
