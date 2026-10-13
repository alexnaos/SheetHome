import json, urllib.request, urllib.parse, sys
BASE="http://localhost:8123"; AUTH="/config/.storage/auth"
out=open("/config/verify_result.txt","w",encoding="utf-8")
def w(*a): print(*a,file=out,flush=True)
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
if not access:
    w("NO TOKEN"); out.close(); sys.exit(1)

def api(path):
    return json.load(urllib.request.urlopen(urllib.request.Request(f"{BASE}{path}",headers={"Authorization":"Bearer "+access}),timeout=20))

allst=api("/api/states")
karta=[s for s in allst if s["entity_id"].startswith("device_tracker.karta_")]
w(f"template 'Карта' трекеров: {len(karta)}")
with_coords=sum(1 for s in karta if s.get("attributes",{}).get("latitude") is not None)
home=sum(1 for s in karta if s.get("state")=="home")
w(f"  С координатами (попадут на карту): {with_coords}")
w(f"  В состоянии home: {home}")
w("Примеры (первые 6):")
for s in karta[:6]:
    at=s.get("attributes",{})
    w(f"  {s['entity_id']} state={s.get('state')!r} lat={at.get('latitude')} lon={at.get('longitude')}")
ks=[s for s in allst if s["entity_id"].startswith("device_tracker.") and s.get("state")=="home" and not s["entity_id"].startswith("device_tracker.karta_")]
w(f"\nkeenetic-источники home (всего {len(ks)}):")
for s in ks:
    w(f"  {s['entity_id']}")
out.close()
