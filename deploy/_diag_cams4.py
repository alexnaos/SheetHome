#!/usr/bin/env python3
import json, subprocess

def sh(cmd):
    return subprocess.run(["bash","-lc",cmd], capture_output=True, text=True)

print("=== HOW IS MANUAL go2rtc STARTED? ===")
print(systemctl := sh("sudo -n systemctl status go2rtc 2>&1 | head -5").stdout)
print("--- crontab ---")
print(sh("sudo -n crontab -l 2>/dev/null | grep -iE 'go2rtc|1984' || echo 'no crontab entry'").stdout)
print("--- rc.local / bashrc / profile ---")
print(sh("sudo -n grep -riE 'go2rtc' /etc/rc.local /home/alex/.bashrc /home/alex/.profile /etc/profile 2>/dev/null || echo 'no startup-script entry'").stdout)
print("--- systemd units mentioning go2rtc ---")
print(sh("sudo -n grep -rlE 'go2rtc' /etc/systemd/system/ /lib/systemd/system/ 2>/dev/null || echo 'no systemd unit'").stdout)
print("--- who started pid 48421 (parent) ---")
print(sh("sudo -n ps -o pid,ppid,user,args -p 48421 2>/dev/null; PPID_LINE=$(sudo -n ps -o ppid= -p 48421 2>/dev/null | tr -d ' '); echo \"parent=$PPID_LINE\"; [ -n \"$PPID_LINE\" ] && sudo -n ps -o pid,ppid,user,args -p $PPID_LINE 2>/dev/null").stdout)

print("=== DEVICE REGISTRY: cameras ===")
dr = "/home/alex/hass_config/.storage/core.device_registry"
with open(dr, encoding="utf-8") as f:
    drdata = json.load(f)
for dev in drdata["data"]["devices"]:
    nm = dev.get("name") or ""
    ids = str(dev.get("identifiers",""))
    if "generic" in ids.lower() or "Nout" in nm or "?????" in nm or "1.68" in nm or "49" in ids:
        print("device name:", repr(nm), "| by_user:", repr(dev.get("name_by_user")), "| identifiers:", ids, "| manufacturer:", dev.get("manufacturer"))

print("=== WEBCAM /dev/video0 FORMATS (v4l2) ===")
res = sh("sudo -n v4l2-ctl -d /dev/video0 --list-formats-ext 2>&1 | head -40")
print(res.stdout if res.stdout else sh("v4l2-ctl --version 2>&1; echo 'v4l2-ctl not available'").stdout)
