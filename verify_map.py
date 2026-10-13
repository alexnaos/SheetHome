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

def api(path):
    return json.load(urllib.request.urlopen(urllib.request.Request(f"{BASE}{path}",headers={"Authorization":"Bearer "+access}),timeout=20))

allst=api("/api/states")
karta=[s for s in allst if s["entity_id"].startswith("device_tracker.karta_")]
print(f"=== template 'Карта' трекеров: {len(karta)} ===")
with_coords=0; home=0
for s in karta:
    at=s.get("attributes",{})
    lat=at.get("latitude"); lon=at.get("longitude")
    st=s.get("state")
    if lat is not None and lon is not None: with_coords+=1
    if st=="home": home+=1
print(f"  С координатами (на карте): {with_coords}")
print(f"  В состоянии home: {home}")
print("\nПримеры (первые 8):")
for s in karta[:8]:
    at=s.get("attributes",{})
    print(f"  {s['entity_id']} state={s.get('state')!r} lat={at.get('latitude')} lon={at.get('longitude')}")

# keenetic-источники в home
print("\n===keenetic-источники сейчас home ===")
ks=[s for s in allst if s["entity_id"].startswith("device_tracker.") and s.get("state")=="home" and not s["entity_id"].startswith("device_tracker.karta_")]
for s in ks:
    print(f"  {s['entity_id']} = {s.get('state')}")
