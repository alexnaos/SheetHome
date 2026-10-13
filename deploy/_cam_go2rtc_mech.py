import subprocess
def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== how is manual go2rtc-1.9.9 started? (systemd/cron/rc) ===")
r = sh("sudo -n systemctl list-units --type=service 2>/dev/null | grep -i go2rtc || echo 'no systemd go2rtc'")
print(r.stdout)
r = sh("sudo -n grep -riE 'go2rtc' /etc/systemd /etc/cron* /home/alex/.bashrc /home/alex/.profile /etc/rc.local 2>/dev/null | grep -v '#' | head")
print(r.stdout or "  (no autostart refs in common places)")

print("=== builtin HA go2rtc temp yaml content ===")
r = sh("pid=$(pgrep -f '/bin/go2rtc' | head -1); args=$(sudo -n tr '\\0' ' ' < /proc/$pid/cmdline 2>/dev/null); echo 'ARGS:' $args")
print(r.stdout)
r = sh("f=$(pgrep -f '/bin/go2rtc' | head -1 | xargs -I{} sudo -n cat /proc/{}/cmdline | tr '\\0' '\\n' | grep -A0 'go2rtc_.*yaml' | head -1); echo 'YAML=' $f; sudo -n cat \"$f\" 2>&1 | head -30")
print(r.stdout)

print("=== docker: does HA container mount /dev/video0? ===")
r = sh("sudo -n docker inspect homeassistant --format '{{json .HostConfig.Devices}}' 2>/dev/null")
print(r.stdout[:400])
r = sh("sudo -n docker inspect homeassistant --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{\"\\n\"}}{{end}}' 2>/dev/null | grep -iE 'config|video' | head")
print(r.stdout)
