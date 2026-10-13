import subprocess

def sh(c, t=6):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

base = "http://127.0.0.1:1984/api"

print("=== 1) mjpeg endpoint (multipart mjpeg stream) ===")
r = sh(f"curl -s -o /dev/null -w 'http=%{{http_code}} time=%{{time_total}}s ctype=%{{content_type}}' --max-time 3 '{base}/stream.mjpeg?src=laptop_camera'")
print("stream.mjpeg:", r.stdout, r.stderr[:100])

print("=== 2) mse endpoint (returns JS for browser MSE) ===")
r = sh(f"curl -s --max-time 3 '{base}/ws?src=laptop_camera'", t=4)
print("ws:", r.stdout[:150])

print("=== 3) check go2rtc version / webrtc support ===")
r = sh(f"curl -s --max-time 3 '{base}/stream.mp4?src=laptop_camera'")
print("mp4 body:", repr(r.stdout[:150]))

print("=== 4) HA camera entity config (stream_source currently mp4) ===")
import json
d = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))
for e in d["data"]["entries"]:
    if e.get("domain") == "generic":
        o = e["options"]
        print(" ", e["entry_id"], "|", e["title"][:20],
              "| stream:", o.get("stream_source"),
              "| still:", o.get("still_image_url"))
