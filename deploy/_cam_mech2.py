import subprocess
def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== FULL cmdline both go2rtc ===")
r = sh("ps -eo pid,ppid,lstart,args | grep -i go2rtc | grep -v grep")
print(r.stdout)

print("=== does builtin go2rtc (18554) see our streams? ===")
r = sh("curl -s --max-time 4 http://127.0.0.1:18554/api/streams")
print("18554 streams:", r.stdout[:400] or "(empty/err)")

print("=== manual go2rtc (1984) streams (known good) ===")
r = sh("curl -s --max-time 4 http://127.0.0.1:1984/api/streams")
print("1984 streams:", r.stdout[:300])

print("=== go2rtc integration HA logs (this boot) ===")
r = sh("sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc' | tail -30")
print(r.stdout or "(no go2rtc lines)")
