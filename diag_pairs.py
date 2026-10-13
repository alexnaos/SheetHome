import json, urllib.request, urllib.parse, sys
BASE="http://localhost:8123"; AUTH="/config/.storage/auth"
d=json.load(open(AUTH)); rts=d["data"].get("refresh_tokens",[])
clients=["http://192.168.1.103:8123/","https://ha.sloboda43.netcraze.pro/"]
access=None
for rt in rts:
    for cid in clients:
        data=urllib.parse.urlencode({"grant_type":"refresh_token","client_id":cid,"refresh_token":rt.get("token")}).encode()
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(BASE+"/auth/token",data=data,headers={"Content-Type":"application/x-www-form-urlencoded"}),timeout=10))
            if r.get("access_token"): access=r["access_token"]; break
        except Exception: pass
    if access: break
if not access: print("NO TOKEN"); sys.exit(1)
H={"Authorization":"Bearer "+access,"Content-Type":"application/json"}

sts=json.load(urllib.request.urlopen(urllib.request.Request(BASE+"/api/states",headers=H),timeout=10))
byid={s["entity_id"]:s for s in sts}

# automations
print("== automations ==")
for s in sts:
    if s["entity_id"].startswith("automation.") and "map" in s["entity_id"]:
        print("  ", s["entity_id"], "|", s["state"])

# source vs karta pairs (sample + counts)
src_ids=[l.strip() for l in open("/config/ids.txt",encoding="utf-8-sig") if l.strip()] if False else None
# fallback: derive from karta entities
karta=[s for s in sts if s["entity_id"].startswith("device_tracker.karta_")]
home_src=0; home_karta=0; matched=0; mismatched=[]
for k in karta:
    src="device_tracker."+k["entity_id"].split("device_tracker.karta_")[1]
    ss=byid.get(src)
    ks=k["state"]
    if ss and ss["state"]=="home": home_src+=1
    if ks=="home": home_karta+=1
    if ss:
        if ss["state"]==ks: matched+=1
        else: mismatched.append((src, ss["state"], k["entity_id"], ks))
print("== summary ==")
print("  karta total:", len(karta), "| karta home:", home_karta, "| source home:", home_src, "| matched:", matched, "| mismatched:", len(mismatched))
for m in mismatched[:40]:
    print("   MISMATCH src=%s(%s) -> %s(%s)" % m)
