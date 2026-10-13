import json, urllib.request, sys

BASE = "http://192.168.1.23:1880"
APPLY = "--apply" in sys.argv

# 1. backup
flows = json.load(urllib.request.urlopen(BASE + "/flows", timeout=15))
backup_name = "/home/alex/hass_config/nodered_flows_backup_retain_%s.json" % (
    __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S"))
with open(backup_name, "w", encoding="utf-8") as f:
    json.dump(flows, f, ensure_ascii=False)
print("backup saved:", backup_name, "nodes:", len(flows))

RETAIN_TOPICS = {"yoradio/orange/status", "yoradio/orange/playlist", "ym/player/cover_url", "ym/track"}
OLD_COVER = 'let coverLink = trackId ? "http://192.168.1.23:1880/" + trackId + ".jpg" : "";'
NEW_COVER = 'let coverLink = current.cover || (trackId ? "http://192.168.1.23:1880/" + trackId + ".jpg" : "");'

changed = []
for n in flows:
    # retain на нужных mqtt-out
    if n.get("type") == "mqtt out" and n.get("topic") in RETAIN_TOPICS:
        if n.get("retain") != "true":
            n["retain"] = "true"
            changed.append("retain -> %s (node %s)" % (n.get("topic"), n.get("id")))
    # фикс старых fun9 (нет current.cover приоритета)
    if n.get("type") == "function" and n.get("name") == "fun9":
        func = n.get("func", "")
        if OLD_COVER in func and "current.cover ||" not in func:
            n["func"] = func.replace(OLD_COVER, NEW_COVER)
            changed.append("fun9 fixed -> %s" % n.get("id"))

print("changes (%d):" % len(changed))
for c in changed:
    print("  ", c)

if not APPLY:
    print("DRY-RUN (no --apply). Nothing deployed.")
    sys.exit(0)

req = urllib.request.Request(
    BASE + "/flows",
    data=json.dumps(flows).encode("utf-8"),
    headers={"Content-Type": "application/json", "Node-RED-Deployment-Type": "full"},
    method="POST",
)
try:
    r = urllib.request.urlopen(req, timeout=30)
    print("deploy HTTP", r.status, r.read()[:200])
except Exception as e:
    print("deploy error:", e)
    if hasattr(e, "read"):
        print("body:", e.read()[:500])
