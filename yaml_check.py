import sys
try:
    import yaml
except Exception as e:
    print("NO yaml:", e); sys.exit(2)
for path in ["/config/packages/map_tracking.yaml","/config/configuration.yaml"]:
    try:
        with open(path) as f:
            docs=list(yaml.safe_load_all(f))
        print(f"OK {path}: {len(docs)} doc(s)")
        # для map_tracking проверим структуру
        if "map_tracking" in path and docs:
            tmpl=docs[0].get("template")
            if tmpl:
                dts=tmpl[0].get("device_tracker",[])
                print("  device_tracker count:", len(dts))
                # проверим уникальность unique_id
                uids=[d.get("unique_id") for d in dts]
                print("  unique unique_id:", len(set(uids))==len(uids))
    except Exception as e:
        print(f"YAML ERROR in {path}: {e}")
