import json, urllib.request, sys, re
BASE = "http://192.168.1.23:1880"
flows = json.load(urllib.request.urlopen(BASE + "/flows", timeout=10))
byid = {n["id"]: n for n in flows if "id" in n}
tabs = {n["id"]: n.get("label") for n in flows if n.get("type") == "tab"}
# edges src -> [dst]
out = {}
inn = {}
for n in flows:
    for i, w in enumerate(n.get("wires") or []):
        for dst in w:
            out.setdefault(n["id"], []).append(dst)
            inn.setdefault(dst, []).append(n["id"])

IMPORTANT = ["ym/track","ym/playlist","ym/player/artist","ym/player/state",
             "ym/player/cover_url","yoradio/orange/status","yoradio/orange/playlist"]

def describe(nid):
    n = byid.get(nid, {})
    return "type=%s name=%r topic=%r tab=%r" % (n.get("type"), n.get("name"), n.get("topic"), tabs.get(n.get("z")))

print("== nodes mentioning each IMPORTANT topic (excluding plain mqtt-in/out) ==")
for t in IMPORTANT:
    hits = []
    for n in flows:
        s = json.dumps(n, ensure_ascii=False)
        if t in s and n.get("type") not in ("mqtt in", "mqtt out"):
            hits.append(n)
    print("\n", t)
    for n in hits:
        extra = ""
        if n.get("type") == "function":
            m = re.findall(r'msg\.topic\s*=\s*["\']([^"\']+)["\']', n.get("func", ""))
            if m: extra = " sets topics=%s" % m
        if n.get("type") == "change":
            for r in n.get("rules", []):
                if r.get("pt") == "msg.topic":
                    extra += " setstopic=%r" % (r.get("to"),)
        print("   ", describe(n["id"]), extra)

# Trace: what feeds each fun9, and are stale ones wired?
print("\n== fun9 wiring (inputs) ==")
for n in flows:
    if n.get("type") == "function" and n.get("name") == "fun9":
        srcs = inn.get(n["id"], [])
        print("  fun9 id=%s tab=%r https=%s disabled=%s" % (
            n["id"], tabs.get(n.get("z")), "current.cover" in n.get("func",""), n.get("disabled")))
        for s in srcs:
            print("      <- ", describe(s))

# Для mqtt out с фиксированным топиком IMPORTANT: найти его источник (кто к нему подключён)
print("\n== mqtt out IMPORTANT: source chain ==")
for n in flows:
    if n.get("type") == "mqtt out" and n.get("topic") in IMPORTANT:
        srcs = inn.get(n["id"], [])
        print("  OUT topic=%r retain=%r tab=%r" % (n.get("topic"), n.get("retain"), tabs.get(n.get("z"))))
        for s in srcs:
            print("      <- ", describe(s))
