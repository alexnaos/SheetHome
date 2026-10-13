#!/usr/bin/env python3
# Включает отключённые keenetic device_tracker'ы через Entity Registry API (websocket).
import json, urllib.request, urllib.parse, sys, ssl, time

BASE="http://localhost:8123"
AUTH="/config/.storage/auth"
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

# Списокkeenetic device_tracker из реестра, которые нужно включить
reg=json.load(open("/config/.storage/core.entity_registry"))
targets=[e["entity_id"] for e in reg["data"]["entities"]
         if e.get("entity_id","").startswith("device_tracker.")
         and e.get("platform")=="keenetic_ndms2"
         and e.get("disabled_by")=="integration"]
print(f"К включению: {len(targets)}keenetic-трекеров")

# Websocket
import socket, base64, os
try:
    import websocket  # type: ignore
    HAVE_WS=True
except Exception:
    HAVE_WS=False
print("websocket-client available:", HAVE_WS)

if not HAVE_WS:
    print("Установите websocket-client или включите трекеры через UI"); sys.exit(2)

ws=websocket.create_connection("ws://localhost:8123/api/websocket", timeout=15)
def recv(): return json.loads(ws.recv())
print("hello:", recv().get("ha_version"))
ws.send(json.dumps({"type":"auth","access_token":access}))
print("auth:", recv().get("type"))

msgid=1
enabled=0; failed=0
for eid in targets:
    ws.send(json.dumps({"id":msgid,"type":"config/entity_registry/update",
                        "entity_id":eid,"disabled_by":None}))
    # ждём ответ с нашим id
    while True:
        m=recv()
        if m.get("id")==msgid:
            if m.get("success"): enabled+=1
            else:
                failed+=1; print("FAIL", eid, m.get("error"))
            break
    msgid+=1
print(f"Включено: {enabled}, ошибок: {failed}")
ws.close()
