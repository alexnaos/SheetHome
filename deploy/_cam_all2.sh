#!/bin/bash
echo "===LIVE frame.jpeg laptop_camera (1984)==="
curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s size=%{size_download}B ctype=%{content_type}\n' --max-time 5 'http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera'
echo "===LIVE mjpeg laptop_camera (1984) 3s==="
curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s size=%{size_download}B ctype=%{content_type}\n' --max-time 3 'http://127.0.0.1:1984/api/stream.mjpeg?src=laptop_camera'
echo "===STREAMS via 1984==="
curl -s --max-time 4 'http://127.0.0.1:1984/api/streams' | head -c 1200
echo
echo "===STREAMS via built-in 18554==="
curl -s --max-time 4 'http://127.0.0.1:18554/api/streams' | head -c 1200
echo
echo "===cam2 (.68) ping==="
ping -c 2 -W 2 192.168.1.68 | tail -3
echo "===cam2 frame.jpeg (.68)==="
curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s size=%{size_download}B\n' --max-time 6 'http://127.0.0.1:1984/api/frame.jpeg?src=cam2'
echo "===cam1 (.49) ping==="
ping -c 2 -W 2 192.168.1.49 | tail -3
