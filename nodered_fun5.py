import json, urllib.request
flows = json.load(urllib.request.urlopen("http://192.168.1.23:1880/flows", timeout=10))
for n in flows:
    if n.get("name") == "fun5":
        print("=== fun5 id=%s tab=%s ===" % (n.get("id"), n.get("z")))
        print(n.get("func"))
