import subprocess, json

def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== 1) go2rtc /api/streams (state + producers + errors) ===")
r = sh("curl -s --max-time 5 'http://127.0.0.1:1984/api/streams'")
try:
    data = json.loads(r.stdout)
    for sid, s in data.items():
        producers = s.get("producers", [])
        # find tracks
        tracks = s.get("tracks", [])
        print(f"  [{sid}] producers={len(producers)} tracks={len(tracks)}")
        for t in tracks:
            print(f"      codec={t.get('codec')} {t.get('width')}x{t.get('height')}")
except Exception as e:
    print("  parse err:", e, "| raw:", r.stdout[:300], r.stderr[:200])

print("\n=== 2) LIVE mjpeg bytes (3s) for laptop_camera ===")
r = sh("timeout 3 curl -s 'http://127.0.0.1:1984/api/stream.mjpeg?src=laptop_camera' | wc -c")
print("  bytes:", r.stdout.strip(), r.stderr[:100])

print("\n=== 3) frame.jpeg (preview) laptop_camera ===")
r = sh("curl -s -o /dev/null -w 'http=%{http_code} size=%{size_download}B time=%{time_total}s' --max-time 5 'http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera'")
print("  ", r.stdout.strip())

print("\n=== 4) go2rtc stderr tail (errors) ===")
r = sh("sudo -n journalctl -u homeassistant --since '5 min ago' --no-pager 2>/dev/null | grep -iE 'go2rtc|video0|ffmpeg|camera|v4l' | tail -15")
print(r.stdout.strip() or "  (no go2rtc lines in journalctl for homeassistant)")

print("\n=== 5) which video device has the laptop cam? test video1 via ffprobe-free curl ===")
r = sh("sudo -n v4l2-ctl --list-devices 2>/dev/null || echo 'no v4l2-ctl'")
print(r.stdout.strip()[:500])
