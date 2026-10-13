import json, subprocess, time

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

print("=== this-boot (2026-10-12) camera/go2rtc errors ===")
out = sh("sudo -n docker logs homeassistant 2>&1 | grep '2026-10-12' | grep -iE 'go2rtc|camera|ffmpeg|invalid config|error setting' | tail -12")
print(out.stdout.strip() or "(none)")

print()
print("=== still preview timing via go2rtc ===")
for src in ["laptop_camera", "cam2"]:
    r = sh(f"curl -s -o /dev/null -w 'http=%{{http_code}} time=%{{time_total}}s size=%{{size_download}}B' "
           f"'http://127.0.0.1:1984/api/frame.jpeg?src={src}'")
    print(f"{src}: {r.stdout.strip()}")

print()
print("=== stream.mp4 timing (live preview first bytes) ===")
for src in ["laptop_camera", "cam2"]:
    r = sh(f"curl -s -o /dev/null -w 'http=%{{http_code}} time=%{{time_total}}s size=%{{size_download}}B' "
           f"--max-time 3 'http://127.0.0.1:1984/api/stream.mp4?src={src}'")
    print(f"{src}: {r.stdout.strip()}")

print()
print("=== ffmpeg video0 process (should be gone or mjpeg) ===")
out = sh("ps -eo args | grep video0 | grep -v grep")
print(out.stdout.strip() or "(no ffmpeg video0 process)")
