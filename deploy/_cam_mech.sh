#!/bin/bash
echo "===== A. кто родитель go2rtc процессов (ppid цепочка) ====="
sudo -n ps -eo pid,ppid,comm,args | grep -iE 'go2rtc' | grep -v grep
echo "--- родители ---"
for p in $(pgrep -f go2rtc); do
  ppid=$(ps -o ppid= -p "$p" | tr -d ' ')
  echo "pid=$p ppid=$ppid -> $(ps -o args= -p "$ppid" 2>/dev/null | head -c 120)"
done

echo
echo "===== B. встроенный go2rtc temp-yaml (что он реально читает) ====="
tdir=$(ls -dt /tmp/go2rtc-* 2>/dev/null | head -1)
echo "tempdir=$tdir"
ls -la "$tdir" 2>/dev/null
echo "--- содержимое ---"
cat "$tdir"/*.yaml 2>/dev/null

echo
echo "===== C. .storage/go2rtc* или api-конфиг интеграции ====="
sudo -n ls -la /home/alex/hass_config/.storage/ | grep -i go2rtc
echo "--- core.config_entries go2rtc (data/options) ---"
sudo -n python3 - <<'PY'
import json
d=json.load(open('/home/alex/hass_config/.storage/core.config_entries',encoding='utf-8'))
for e in d['data']['entries']:
    if e.get('domain')=='go2rtc':
        print(json.dumps(e, ensure_ascii=False, indent=1))
PY

echo
echo "===== D. go2rtc-интеграция: строки setup в логе ====="
sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc' | tail -20

echo
echo "===== E. кто держит порт 1984 и 18554 ====="
sudo -n ss -ltnp 2>/dev/null | grep -E ':1984|:18554' || sudo -n netstat -ltnp 2>/dev/null | grep -E ':1984|:18554'

echo "===== DONE ====="
