import subprocess

def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

print("=== go2rtc processes ===")
r = sh("ps -eo pid,ppid,args | grep -i go2rtc | grep -v grep")
print(r.stdout)

print("=== who listens on 1984 ===")
r = sh("sudo -n ss -ltnp 2>/dev/null | grep 1984 || echo none")
print(r.stdout)

print("=== streams API (go2rtc on 1984) ===")
r = sh("curl -s --max-time 4 http://127.0.0.1:1984/api/streams")
print(r.stdout[:600])

print("=== laptop_camera live: producers + frame ===")
r = sh("curl -s --max-time 4 http://127.0.0.1:1984/api/streams?src=laptop_camera")
print("streams?src:", r.stdout[:300])
r = sh("curl -s -o /dev/null -w 'frame.jpeg http=%{http_code} time=%{time_total}s size=%{size_download}B' --max-time 5 http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera")
print("frame.jpeg:", r.stdout)

print("=== cam2 (.68) reachability ===")
r = sh("ping -c 2 -W 2 192.168.1.68 2>&1 | tail -3")
print(r.stdout)
r = sh("timeout 3 bash -c 'cat < /dev/null > /dev/tcp/192.168.1.68/554' 2>&1 && echo PORT_554_OPEN || echo PORT_554_CLOSED")
print(r.stdout)
