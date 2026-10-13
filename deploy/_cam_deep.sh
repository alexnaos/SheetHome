#!/bin/bash
echo "===================================================================="
echo "A) go2rtc.yaml (что читает ручной go2rtc)"
echo "===================================================================="
sudo -n cat /home/alex/hass_config/go2rtc.yaml
echo
echo "===================================================================="
echo "B) Процессы go2rtc: pid / ppid / cmdline / порт"
echo "===================================================================="
sudo -n ps -eo pid,ppid,comm,args | grep -iE 'go2rtc|homeassistant' | grep -v grep
echo
echo "--- кто держит порты 1984 / 18554 ---"
sudo -n ss -ltnp 2>/dev/null | grep -E ':1984|:18554' || echo "(ss не показал)"
echo
echo "--- родитель ручного go2rtc (systemd? cron? HA?) ---"
MPID=$(pgrep -f 'go2rtc-1.9.9' | head -1)
if [ -n "$MPID" ]; then
  echo "manual go2rtc pid=$MPID ppid=$(ps -o ppid= -p $MPID | tr -d ' ')"
  P=$(ps -o ppid= -p $MPID | tr -d ' ')
  echo "parent cmd: $(ps -o args= -p $P 2>/dev/null | head -c 200)"
fi
echo "--- systemd units go2rtc? ---"
sudo -n systemctl list-units --type=service --all 2>/dev/null | grep -i go2rtc || echo "(нет systemd-юнита go2rtc)"
echo "--- crontab go2rtc? ---"
sudo -n crontab -l 2>/dev/null | grep -i go2rtc || echo "(нет в crontab)"
echo
echo "===================================================================="
echo "C) go2rtc API: streams на РУЧНОМ (:1984)"
echo "===================================================================="
curl -s --max-time 4 http://127.0.0.1:1984/api/streams || echo "(1984 недоступен)"
echo
echo "===================================================================="
echo "D) go2rtc API: streams на ВСТРОЕННОМ (:18554)"
echo "===================================================================="
curl -s --max-time 4 http://127.0.0.1:18554/api/streams || echo "(18554 недоступен)"
echo
echo "===================================================================="
echo "E) ИСХОДНИКИ встроенной go2rtc-интеграции (как хранит потоки)"
echo "===================================================================="
for f in __init__.py config_flow.py const.py camera.py; do
  echo "----- homeassistant/components/go2rtc/$f -----"
  sudo -n docker exec homeassistant sh -c "cat /usr/src/homeassistant/homeassistant/components/go2rtc/$f 2>/dev/null | head -160" || echo "(нет файла $f)"
  echo
done
