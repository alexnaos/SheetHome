import subprocess

def sh(c, t=8):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)
    return (r.stdout or "") + (r.stderr or "")

print("=== built-in go2rtc temp yaml (inside container) ===")
print(sh("sudo -n docker exec homeassistant sh -c 'cat /tmp/go2rtc-*/go2rtc_*.yaml 2>/dev/null'"))
print()
print("=== go2rtc integration setup log (this boot) ===")
print(sh("sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc|Setting up|Discover' | grep -iE 'go2rtc' | tail -25"))
print()
print("=== /config/go2rtc.yaml current (raw) ===")
print(sh("sudo -n cat /home/alex/hass_config/go2rtc.yaml"))
print()
print("=== how does /config/go2rtc-1.9.9 get launched? open its cmdline env ===")
print(sh("sudo -n tr '\\0' ' ' < /proc/1453/environ 2>/dev/null | head -c 400"))
print()
print("=== parent chain of 1453 already known: 1314 (HA). Check HA go2rtc integration module ===")
print(sh("sudo -n docker exec homeassistant sh -c 'ls /config/custom_components/ 2>/dev/null; echo ---; ls /config/www/community 2>/dev/null | head'"))
