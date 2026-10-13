#!/usr/bin/env python3
import json, urllib.request, urllib.parse, urllib.error, sys
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
if not access: print("NO TOKEN"); sys.exit(0)

def gs(eid):
    return json.load(urllib.request.urlopen(urllib.request.Request(f"{BASE}/api/states/{eid}",headers={"Authorization":"Bearer "+access}),timeout=10))

def list_states():
    return json.load(urllib.request.urlopen(urllib.request.Request(f"{BASE}/api/states",headers={"Authorization":"Bearer "+access}),timeout=20))

print("=== ALL device_tracker (live) ===")
allst=list_states()
for s in allst:
    eid=s.get("entity_id","")
    if eid.startswith("device_tracker."):
        at=s.get("attributes",{})
        lat=at.get("latitude"); lon=at.get("longitude")
        st=s.get("state")
        stype=at.get("source_type")
        gps=at.get("gps_accuracy")
        fn=at.get("friendly_name","")
        has_coords = "YES" if (lat is not None and lon is not None) else "no"
        print(f"{eid}\n   state={st!r} source_type={stype!r} coords={has_coords} lat={lat} lon={lon} gps_acc={gps} name={fn!r}")

print("\n=== zone.* (live) ===")
for s in allst:
    if s.get("entity_id","").startswith("zone."):
        at=s.get("attributes",{})
        print(f"{s['entity_id']} state={s.get('state')!r} lat={at.get('latitude')} lon={at.get('longitude')} radius={at.get('radius')}")

print("\n=== person.* (live) ===")
for s in allst:
    if s.get("entity_id","").startswith("person."):
        at=s.get("attributes",{})
        print(f"{s['entity_id']} state={s.get('state')!r} lat={at.get('latitude')} lon={at.get('longitude')} gps={at.get('gps_accuracy')}")
