import subprocess
def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

for host, name in [("192.168.1.49", "Камера 1 (.49)"), ("192.168.1.68", "cam2 (.68)")]:
    print(f"=== {name} ===")
    r = sh(f"ping -c 2 -W 2 {host} 2>&1 | tail -2")
    print(r.stdout.strip())
    r = sh(f"timeout 3 bash -c 'cat < /dev/null > /dev/tcp/{host}/554' 2>&1 && echo '  554=OPEN' || echo '  554=CLOSED'")
    print(r.stdout.strip())
    # try reading a bit of the rtsp stream via ffprobe if available
    r = sh(f"timeout 6 ffprobe -v error -rtsp_transport tcp -show_entries stream=codec_type,codec_name -of default=nw=1 'rtsp://{host}:554/0/av0' 2>&1 | head -6")
    print("  ffprobe:", (r.stdout.strip() or r.stderr.strip())[:200] or "no output")
