import json, sys

try:
    import yaml
except ImportError:
    print("PyYAML not available, will handle go2rtc.yaml as text")
    yaml = None

G2RTC = "/home/alex/hass_config/go2rtc.yaml"
CE = "/home/alex/hass_config/.storage/core.config_entries"

# ---------- 1) go2rtc.yaml : laptop_camera mjpeg 320x240 ----------
old_stream = "ffmpeg:device?video=/dev/video0#input=yuv422p#video=h264#size=640x480#aspeed=5"
new_stream = "ffmpeg:device?video=/dev/video0#input=yuv422p#video=mjpeg#size=320x240#aspeed=5"

raw = open(G2RTC, encoding="utf-8").read()
if old_stream in raw:
    raw = raw.replace(old_stream, new_stream)
    open(G2RTC, "w", encoding="utf-8").write(raw)
    print("go2rtc.yaml: laptop_camera -> mjpeg 320x240 OK")
else:
    # maybe already edited or pyyaml path; try yaml
    if yaml:
        d = yaml.safe_load(open(G2RTC, encoding="utf-8"))
        if d and d.get("streams", {}).get("laptop_camera"):
            d["streams"]["laptop_camera"] = [new_stream]
            yaml.safe_dump(d, open(G2RTC, "w", encoding="utf-8"),
                           sort_keys=False, allow_unicode=True)
            print("go2rtc.yaml: laptop_camera set via yaml OK")
    else:
        print("WARN: old_stream not found and no yaml module")

# ---------- 2) core.config_entries : still_image + framerate ----------
d = json.load(open(CE, encoding="utf-8"))
n_cam = 0
for e in d["data"]["entries"]:
    if e.get("domain") != "generic":
        continue
    eid = e["entry_id"]
    o = e.setdefault("options", {})
    adv = o.setdefault("advanced", {})
    if eid == "01KQYY204CPYW0H7ZFAAFQJ9CN":  # NoutCamera / laptop_camera
        o["still_image_url"] = "http://127.0.0.1:1984/api/frame.jpeg?src=laptop_camera"
        adv["framerate"] = 1.0
        n_cam += 1
        print("NoutCamera: still_image_url added, framerate=1.0")
    elif eid == "01KV6A66BE65JGYTGTJDTT7EKC":  # camera .68 / cam2
        adv["framerate"] = 5.0
        n_cam += 1
        print("camera .68: framerate=5.0")

# write WITHOUT BOM, HA style (indent=2, utf-8, keep unicode)
with open(CE, "w", encoding="utf-8") as f:
    f.write(json.dumps(d, ensure_ascii=False, indent=2))
    f.write("\n")

print("config_entries written, cameras updated:", n_cam)

# ---------- verify ----------
b = open(CE, "rb").read()
print("has_BOM:", b[:3] == b"\xef\xbb\xbf")
d2 = json.loads(open(CE, encoding="utf-8").read())
print("entries_total:", len(d2["data"]["entries"]))
for e in d2["data"]["entries"]:
    if e.get("domain") == "generic":
        o = e["options"]
        print(" ", e["entry_id"], "| still:", o.get("still_image_url"), "| fps:", o.get("advanced", {}).get("framerate"))
