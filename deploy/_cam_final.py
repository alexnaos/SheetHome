import subprocess

def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== built-in HA go2rtc (port 18554) streams ===")
r = sh("curl -s --max-time 4 http://127.0.0.1:18554/api/streams")
print(" ", r.stdout[:500] or r.stderr[:150])

print("=== manual go2rtc-1.9.9 (1984) cam2 producer status ===")
r = sh("curl -s --max-time 5 'http://127.0.0.1:1984/api/streams?src=cam2'")
print(" ", r.stdout[:400])

print("=== what endpoints does 1984 serve for laptop_camera? ===")
for ep in ["stream.mjpeg", "frame.jpeg", "stream.mp4", "api/stream.mp4", "api/webrtc"]:
    r = sh(f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 4 'http://127.0.0.1:1984/api/{ep}?src=laptop_camera'")
    print(f"   {ep:16s} -> {r.stdout}")

print("=== go2rtc.yaml integration marker (HA reads this) ===")
r = sh("sudo -n head -5 /home/alex/hass_config/go2rtc.yaml")
print(r.stdout)

print("=== is there a native camera entity ANYWHERE (loose search) ===")
r = open("/home/alex/hass_config/.storage/core.entity_registry", encoding="utf-8").read()
for name in ["camera.laptop_camera", "camera.cam2", "go2rtc"]:
    print(f"   contains '{name}':", name in r)
