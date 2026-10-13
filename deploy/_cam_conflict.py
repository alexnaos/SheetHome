import subprocess

def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== who is parent 1314? ===")
r = sh("sudo -n ps -o pid,ppid,args -p 1314 2>/dev/null")
print(r.stdout or "  gone")

print("=== full cmdline of both go2rtc ===")
r = sh("sudo -n tr '\\0' ' ' < /proc/1453/cmdline; echo; echo '---1462---'; sudo -n tr '\\0' ' ' < /proc/1462/cmdline; echo")
print(r.stdout)

print("=== ports of BOTH go2rtc (1462 native) ===")
r = sh("sudo -n ss -ltnp 2>/dev/null | grep -E '1453|1462|go2rtc'")
print(r.stdout or "  none")

print("=== native go2rtc (1462) API port probe ===")
r = sh("sudo -n ss -ltnp 2>/dev/null | awk '/go2rtc/{print}'")
print(r.stdout)

print("=== FULL recent go2rtc integration log (no filter) ===")
r = sh("sudo -n docker logs homeassistant 2>&1 | grep -i 'go2rtc' | tail -15")
print(r.stdout or "  none")

print("=== how was go2rtc-1.9.9 started? (systemd/docker/script) ===")
r = sh("sudo -n cat /proc/1314/cmdline 2>/dev/null | tr '\\0' ' '; echo")
print(r.stdout or "  ?")
