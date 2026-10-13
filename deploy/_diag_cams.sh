#!/bin/bash
echo "==================== CAMERA ENTITY REGISTRY ===================="
sudo -n python3 - <<'PY'
import json
p="/home/alex/hass_config/.storage/core.entity_registry"
d=json.load(open(p))
for e in d["data"]["entities"]:
    if e.get("entity_id","").startswith("camera."):
        print("entity_id :", e.get("entity_id"))
        print("  platform    :", e.get("platform"))
        print("  unique_id   :", e.get("unique_id"))
        print("  name        :", repr(e.get("name")))
        print("  orig_name   :", repr(e.get("original_name")))
        print("  dev_class   :", e.get("original_device_class"))
        print("---")
PY

echo "==================== GO2RTC PROCESS / LOAD ===================="
ps -eo pid,pcpu,pmem,comm,args | grep -iE 'go2rtc|ffmpeg' | grep -v grep
echo "--- loadavg ---"
cat /proc/loadavg
echo "--- nproc ---"
nproc

echo "==================== /dev/video* (local cam) ===================="
ls -la /dev/video* 2>&1
echo "--- ffmpeg capture test (3s, /dev/video0) ---"
timeout 6 /home/alex/hass_config/go2rtc-1.9.9 --version 2>&1 | head -1 || echo "go2rtc not executable"

echo "==================== CAMERA IP reachability ===================="
for ip in 192.168.1.49 192.168.1.68 192.168.1.42; do
  echo "--- $ip ---"
  ping -c1 -W1 $ip >/dev/null 2>&1 && echo "ping OK" || echo "ping FAIL"
  (timeout 3 bash -c "cat </dev/null >/dev/tcp/$ip/554" 2>/dev/null && echo "port554 OPEN") || echo "port554 closed"
done
