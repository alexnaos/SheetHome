import json

base = "/home/alex/hass_config/.storage"

print("=== 1) config_entries domains related to camera/go2rtc ===")
ce = json.load(open(f"{base}/core.config_entries", encoding="utf-8"))
for e in ce["data"]["entries"]:
    dom = e.get("domain", "")
    if dom in ("go2rtc", "generic", "camera", "stream", "onvif", "rtsp_to_webrtc"):
        o = e.get("options", {})
        print(f"  domain={dom} | title={e.get('title')}")
        print(f"     stream_source={o.get('stream_source')}")
        print(f"     still_image_url={o.get('still_image_url')}")
        print(f"     entry_id={e.get('entry_id')}")

print("\n=== 2) camera entities in registry ===")
er = json.load(open(f"{base}/core.entity_registry", encoding="utf-8"))
ents = er["data"]["entities"]
if isinstance(ents, dict):
    ents = list(ents.values())
for e in ents:
    if e.get("entity_id", "").startswith("camera."):
        print(f"  {e.get('entity_id')} | platform={e.get('platform')} | orig={e.get('original_name')} | unique={e.get('unique_id')}")

print("\n=== 3) go2rtc config check ===")
import os
for f in ["go2rtc.yaml", "go2rtc-1.9.9"]:
    p = os.path.join("/home/alex/hass_config", f)
    print(f"  {f}: exists={os.path.exists(p)}")
