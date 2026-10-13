import json, subprocess

def sh(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

d = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))
entries = d["data"]["entries"]

print("=== go2rtc integration entry ===")
for e in entries:
    if e.get("domain") == "go2rtc":
        print("entry_id:", e["entry_id"], "| title:", e["title"])
        print("  data:", json.dumps(e.get("data", {}), ensure_ascii=False))
        print("  options:", json.dumps(e.get("options", {}), ensure_ascii=False))

print("\n=== generic camera entries (platform=generic) ===")
for e in entries:
    if e.get("domain") == "generic":
        o = e.get("options", {})
        print("title:", e["title"][:40])
        print("  still_image_url:", o.get("still_image_url"))
        print("  stream_source :", o.get("stream_source"))
        print("  framerate     :", o.get("advanced", {}).get("framerate"))
        print("  content_type  :", o.get("content_type"))
        print("  verify_ssl    :", o.get("advanced", {}).get("verify_ssl"))
        print("  ---")

print("\n=== built-in go2rtc 18554 streams (retry) ===")
r = sh("curl -s --max-time 4 http://127.0.0.1:18554/api/streams")
print(repr(r.stdout[:600]) if r.stdout else "EMPTY/NO-RESPONSE", "| rc:", r.returncode)

print("\n=== how go2rtc integration was set up (log: config loaded) ===")
r = sh("sudo -n docker logs homeassistant 2>&1 | grep -iE 'go2rtc' | grep -iE 'load|config|stream|listen|server|start|api:' | tail -15")
print(r.stdout[:1500] if r.stdout else "(none)")
