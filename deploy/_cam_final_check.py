import subprocess, time

def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== 1) go2rtc process alive? ===")
r = sh("ps -eo pid,args | grep -i go2rtc | grep -v grep")
print(r.stdout.strip() or "GO2RTC NOT FOUND")

print("\n=== 2) stream.mjpeg for laptop_camera (live video check) ===")
# count bytes in 3s - live mjpeg stream should keep producing frames
r = sh("timeout 3 curl -s 'http://127.0.0.1:1984/api/stream.mjpeg?src=laptop_camera' | wc -c")
print("mjpeg bytes in 3s:", r.stdout.strip())

print("\n=== 3) frame.jpeg (still preview) ===")
r = sh("curl -s -o /dev/null -w 'http=%{http_code} size=%{size_download}B time=%{time_total}s' --max-time 4 'http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera'")
print("frame.jpeg:", r.stdout.strip())

print("\n=== 4) cam2 (RTSP) still preview ===")
r = sh("curl -s -o /dev/null -w 'http=%{http_code} size=%{size_download}B time=%{time_total}s' --max-time 5 'http://127.0.0.1:1984/api/frame.jpeg?src=cam2'")
print("cam2 frame.jpeg:", r.stdout.strip())

print("\n=== 5) this-boot camera/go2rtc errors in HA log ===")
r = sh("sudo -n docker logs --since 2026-10-12T18:45:00 homeassistant 2>&1 | grep -iE 'go2rtc|camera|stream|generic' | grep -iE 'error|fail|warn|exception|500' | tail -15")
print(r.stdout.strip() or "NO camera/go2rtc errors this boot")
