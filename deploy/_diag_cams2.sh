#!/bin/bash
echo "=== WHO OWNS PORT 1984 ==="
sudo -n ss -ltnp 2>/dev/null | grep -E ':1984' || echo "no listener on 1984 (ss)"
echo
echo "=== go2rtc integration temp config (in /tmp) ==="
sudo -n find /tmp -maxdepth 2 -iname 'go2rtc*.yaml' 2>/dev/null -exec sudo -n sh -c 'echo "--- {} ---"; cat "{}"' \;
echo
echo "=== go2rtc API: streams ==="
curl -s --max-time 5 http://127.0.0.1:1984/api/streams || echo "API unreachable"
echo
echo
echo "=== /dev/video0 exists? (laptop webcam) ==="
sudo -n ls -la /dev/video0 2>&1 || echo "NO /dev/video0"
echo
echo "=== ffmpeg present? ==="
which ffmpeg 2>&1 || echo "no ffmpeg in PATH"
echo
echo "=== CPU load (transcode cost) ==="
uptime
