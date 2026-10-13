import json, urllib.request, urllib.parse, sys
import websocket
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

ws=websocket.create_connection("ws://localhost:8123/api/websocket",timeout=30)
def recv(): return json.loads(ws.recv())
def wait_id(mid):
    while True:
        m=recv()
        if m.get("id")==mid: return m
recv()
ws.send(json.dumps({"type":"auth","access_token":access})); recv()

# Полный пересмотр YAML-конфигурации (перечитает packages и template)
ws.send(json.dumps({"id":20,"type":"config/core/check_config"}))
# Если не поддерживается, используем reload_config_entry через сервис домена homeassistant
ws.send(json.dumps({"id":21,"type":"call_service","domain":"homeassistant","service":"reload_all","service_data":{},"return_response":False}))
print("reload_all:", wait_id(21))
ws.close()
