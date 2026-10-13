import json

ce = json.load(open("/home/alex/hass_config/.storage/core.config_entries", encoding="utf-8"))
reg = json.loads(open("/home/alex/hass_config/.storage/core.entity_registry", encoding="utf-8").read())

def hexdump_utf8(s):
    # show raw utf-8 bytes for a string
    return " ".join(f"{b:02x}" for b in s.encode("utf-8"))

print("=== config_entry title (generic) ===")
for e in ce["data"]["entries"]:
    if e.get("domain") == "generic":
        t = e["title"]
        print(f"  title={t!r}")
        print(f"    len={len(t)}  hex[:60]={hexdump_utf8(t)[:60]}")
        print(f"    is_all_qmarks={all(c=='?' for c in t)}")

print()
print("=== entity_registry original_name for camera.192_168_1_42 ===")
for k, v in reg["data"]["entities"].items():
    if k == "camera.192_168_1_42":
        on = v.get("original_name") or ""
        nm = v.get("name") or ""
        print(f"  name        ={nm!r}  hex={hexdump_utf8(nm)[:40]}")
        print(f"  orig_name   ={on!r}")
        print(f"    len={len(on)} hex[:80]={hexdump_utf8(on)[:80]}")
        print(f"    is_all_qmarks={all(c=='?' for c in on)}")

print()
print("=== is it real '?' (0x3f) or broken utf-8 cyrillic? ===")
for e in ce["data"]["entries"]:
    if e.get("domain") == "generic":
        t = e["title"].encode("utf-8")
        print(f"  contains 0x3f (question mark)? {b'?' in t}")
        print(f"  contains 0xd0/0xd1 (utf8 cyrillic prefix)? {(0xd0 in t) or (0xd1 in t)}")
