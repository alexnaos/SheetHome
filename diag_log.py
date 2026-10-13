import subprocess, sys
out = subprocess.run(["docker","logs","--since","20m","homeassistant"], capture_output=True, text=True, errors="replace")
lines = (out.stdout + out.stderr).splitlines()
keys = ("see service", "map_keenetic", "not supported", "Error executing script", "Traceback", "invalid config", "DeviceTracker")
hits = [l for l in lines if any(k.lower() in l.lower() for k in keys)]
print("total lines:", len(lines), "hits:", len(hits))
for l in hits[:40]:
    print(l)
