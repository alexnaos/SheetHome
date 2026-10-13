#!/bin/bash
echo "===STATUS==="
sudo -n docker ps --filter name=homeassistant --format '{{.Names}} | {{.Status}}'
echo
echo "===BOOT ERRORS since 08:28:30==="
sudo -n docker logs --since 2026-10-13T08:28:30 homeassistant 2>&1 \
  | grep -iE 'invalid config|error setting up|traceback|corrupt|unexpected' \
  | tail -20
echo "(end errors)"
echo
echo "===NoutCamera / cam2 preview liveness==="
echo -n "laptop_camera frame.jpeg: "; curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s\n' --max-time 4 'http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera'
echo -n "cam2 frame.jpeg:         "; curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s\n' --max-time 4 'http://127.0.0.1:1984/api/frame.jpeg?src=cam2'
