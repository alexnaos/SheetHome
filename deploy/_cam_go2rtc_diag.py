import subprocess

def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== go2rtc integration logs (startup) ===")
r = sh("sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc' | tail -30")
print(r.stdout or r.stderr[:200])

print("=== go2rtc API reachable from HA container? ===")
r = sh("sudo -n docker exec homeassistant sh -c 'curl -s -o /dev/null -w \"api=%{http_code}\" --max-time 4 http://127.0.0.1:1984/api/streams'")
print("  container curl streams:", r.stdout, r.stderr[:120])

print("=== go2rtc streams list (from host) ===")
r = sh("curl -s --max-time 4 http://127.0.0.1:1984/api/streams")
print("  streams:", r.stdout[:400])

print("=== cam2 (.68) reachability ===")
r = sh("ping -c 2 -W 2 192.168.1.68 2>&1 | tail -3")
print(r.stdout)
r = sh("(timeout 3 bash -c 'cat </dev/null >/dev/tcp/192.168.1.68/554' 2>&1 && echo RTSP_554_OPEN) || echo RTSP_554_CLOSED")
print("  ", r.stdout)
