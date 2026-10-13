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

# 1) automation states
sts=json.load(urllib.request.urlopen(urllib.request.Request(BASE+"/api/states",headers=H),timeout=10))
autos=[s for s in sts if s["entity_id"].startswith("automation.")]
print("automation entities:", len(autos))
for s in autos:
    if "map" in s["entity_id"] or "map" in str(s.get("attributes",{}).get("friendly_name","")).lower():
        print("  ", s["entity_id"], "|", s["state"], "|", s.get("attributes",{}).get("friendly_name"))

# 2) direct see call for antix1 (source is home)
def see(dev_id, host, loc, gps=None):
    payload={"dev_id":dev_id,"host_name":host,"location_name":loc,"source_type":"router"}
    if gps: payload["gps"]=gps
    req=urllib.request.Request(BASE+"/api/services/device_tracker/see",data=json.dumps(payload).encode(),headers=H)
    try:
        json.load(urllib.request.urlopen(req,timeout=10)); return "OK"
    except Exception as e:
        return "ERR "+str(e)

print("direct see antix1 ->", see("karta_antix1","antix1","home",[55.586173527410885,39.4296419620514]))

# 3) read back karta_antix1
sts2=json.load(urllib.request.urlopen(urllib.request.Request(BASE+"/api/states/device_tracker.karta_antix1",headers=H),timeout=10))
a=sts2.get("attributes",{})
print("karta_antix1 now:", sts2["state"], "| lat:", a.get("latitude"), "| lon:", a.get("longitude"))
