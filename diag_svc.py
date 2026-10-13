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

try:
    req=urllib.request.Request(BASE+"/api/services/device_tracker", headers={"Authorization":"Bearer "+access})
    svc=json.load(urllib.request.urlopen(req,timeout=10))
    svcs=set()
    for reg in svc:
        svcs.update(reg.get("services",{}).keys())
    print("device_tracker services:", sorted(svcs))
except Exception as e:
    print("services endpoint error:", e)

req=urllib.request.Request(BASE+"/api/states", headers={"Authorization":"Bearer "+access})
sts=json.load(urllib.request.urlopen(req,timeout=10))
dts=[s for s in sts if s["entity_id"].startswith("device_tracker.")]
print("device_tracker states:", len(dts))
for s in dts:
    a=s.get("attributes",{})
    print(" ", s["entity_id"], "|", s["state"], "| lat:", a.get("latitude"), "| lon:", a.get("longitude"))
pers=[s for s in sts if s["entity_id"].startswith("person.")]
for s in pers:
    a=s.get("attributes",{})
    print("PERSON", s["entity_id"], "|", s["state"], "| lat:", a.get("latitude"), "| lon:", a.get("longitude"))

