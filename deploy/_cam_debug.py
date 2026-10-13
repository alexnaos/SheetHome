import subprocess

def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True)

print("=== mp4 body for laptop_camera (error text) ===")
r = sh("curl -s --max-time 4 'http://127.0.0.1:1984/api/stream.mp4?src=laptop_camera'")
print(repr(r.stdout[:300]))

print("=== retry frame.jpeg (warm-up check) ===")
r = sh("curl -s -o /dev/null -w 'http=%{http_code} time=%{time_total}s' 'http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera'")
print(r.stdout)

print("=== go2rtc /api/streams (laptop_camera online?) ===")
r = sh("curl -s 'http://127.0.0.1:1984/api/streams'")
print(r.stdout[:600])
