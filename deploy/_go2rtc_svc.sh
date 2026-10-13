#!/bin/bash
echo "===HOW GO2RTC RUNS==="
sudo -n systemctl status go2rtc --no-pager 2>/dev/null | head -8 || echo "no systemd go2rtc"
echo
echo "===go2rtc systemd service file==="
sudo -n systemctl cat go2rtc --no-pager 2>/dev/null | head -25 || echo "no unit"
echo
echo "===is there go2rtc service?==="
sudo -n systemctl list-units --type=service --all 2>/dev/null | grep -i go2rtc || echo "no go2rtc service"
echo
echo "===parent of go2rtc pid 48421==="
sudo -n ps -o pid,ppid,args -p 48421 2>/dev/null
echo
echo "===dmesg last video0==="
sudo -n dmesg 2>/dev/null | grep -i video0 | tail -3 || echo "no dmesg access"
