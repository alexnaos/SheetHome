#!/usr/bin/env python3
import subprocess, time

def test(url, label):
    t0 = time.time()
    r = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code} %{size_download}",
                        "--max-time","12", url], capture_output=True, text=True)
    dt = time.time() - t0
    print(f"{label:20s} -> {r.stdout:15s} in {dt:.2f}s")

base = "http://127.0.0.1:1984"
print("=== go2rtc frame.jpeg timings ===")
test(f"{base}/api/frame.jpeg?src=laptop_camera", "laptop_camera")
test(f"{base}/api/frame.jpeg?src=cam2", "cam2 (.68)")
test(f"{base}/api/frame.jpeg?src=cam1", "cam1 (.49)")
print()
print("=== go2rtc API health ===")
print(subprocess.run(["curl","-s","--max-time","5",f"{base}/api/streams"],
      capture_output=True,text=True).stdout)
