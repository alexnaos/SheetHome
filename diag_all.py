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
H={"Authorization":"Bearer "+access}

sts=json.load(urllib.request.urlopen(urllib.request.Request(BASE+"/api/states",headers=H),timeout=10))

print("== yandex entities ==")
for s in sts:
    eid=s["entity_id"]
    if "ym" in eid or "yandex" in eid:
        a=s.get("attributes",{})
        print(" ", eid, "|", s["state"], "| pic:", a.get("entity_picture"), "| friendly:", a.get("friendly_name"))

print("== mqtt sensors ==")
for s in sts:
    if s["entity_id"].startswith("sensor.ym"):
        print(" ", s["entity_id"], "|", s["state"])

print("== karta with gps ==")
karta=[s for s in sts if s["entity_id"].startswith("device_tracker.karta_")]
home=[k for k in karta if k["state"]=="home"]
withgps=[k for k in home if k.get("attributes",{}).get("latitude") is not None]
print("  total:",len(karta),"home:",len(home),"home_with_gps:",len(withgps))
for k in withgps[:5]:
    a=k["attributes"]
    print("   ",k["entity_id"],"lat:",a.get("latitude"),"lon:",a.get("longitude"))
