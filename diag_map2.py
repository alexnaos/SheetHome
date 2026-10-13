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

def api(path):
    return json.load(urllib.request.urlopen(urllib.request.Request(f"{BASE}{path}",headers={"Authorization":"Bearer "+access}),timeout=20))

# Все person (детали - к какому device_tracker привязан)
print("=== person config ===")
try:
    persons=api("/api/config/person/config")
    for p in persons:
        print(f"  {p.get('id')} name={p.get('name')!r} device_trackers={p.get('device_trackers')} gps={p.get('gps_accuracy')} lat={p.get('latitude')} lon={p.get('longitude')}")
except Exception as e:
    print("person err:", e)

# Зона home точные координаты
print("\n=== zone home ===")
try:
    z=api("/api/states/zone.home")
    at=z.get("attributes",{})
    print(f"  lat={at.get('latitude')} lon={at.get('longitude')} radius={at.get('radius')} passive={at.get('passive')}")
except Exception as e:
    print("zone err:", e)

# Конфигурация keenetic интеграции (опции)
print("\n=== keenetic config entry ===")
import os
try:
    ce=json.load(open("/config/.storage/core.config_entries"))
    for e in ce["data"]["entries"]:
        if e.get("domain")=="keenetic_ndms2":
            print(f"  title={e.get('title')} options={e.get('options')}")
except Exception as e:
    print("ce err:", e)
