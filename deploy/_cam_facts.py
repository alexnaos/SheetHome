import json, subprocess

def run(c, t=8):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)

reg = json.load(open("/home/alex/hass_config/.storage/core.entity_registry", encoding="utf-8"))
print("=== ALL CAMERA ENTITIES (entity_registry) ===")
for e in reg["data"]["entities"]:
    if e.get("entity_id","").startswith("camera."):
        print(f"  {e['entity_id']}")
        print(f"     platform={e.get('platform')} unique_id={e.get('unique_id')}")
        print(f"     original_name={e.get('original_name')!r} name={e.get('name')!r}")
        oc = e.get("original_device_class")
        print(f"     orig_device_class={oc}")

ce = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))
print("\n=== go2rtc config entry ===")
for e in ce["data"]["entries"]:
    if e.get("domain")=="go2rtc":
        print("  title:", e.get("title"))
        print("  data :", json.dumps(e.get("data"), ensure_ascii=False))
        print("  opts :", json.dumps(e.get("options"), ensure_ascii=False))

print("\n=== generic camera config entries ===")
for e in ce["data"]["entries"]:
    if e.get("domain")=="generic":
        o = e.get("options",{})
        print(f"  {e['entry_id']} title={e.get('title')!r}")
        print(f"     still={o.get('still_image_url')}")
        print(f"     stream={o.get('stream_source')}")
        print(f"     framerate={o.get('framerate')} verify_ssl={o.get('verify_ssl')}")

print("\n=== process tree (go2rtc/ffmpeg/homeassistant) ===")
print(run("ps -eo pid,ppid,comm,args | grep -iE 'go2rtc|ffmpeg|homeassistant --config' | grep -v grep").stdout)
