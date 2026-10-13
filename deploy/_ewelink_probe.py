import socket, time, json, sys

IP = "192.168.1.72"
PORT = 8081
DEVICEID = "100284cd66"

def try_tcp_hello():
    # eWeLink LAN devices: connect to 8081 and send a discovery/login payload.
    # A brand new (non-DIY) device will respond with encrypted data that needs devicekey.
    s = socket.socket(); s.settimeout(4)
    try:
        s.connect((IP, PORT))
    except Exception as e:
        print("CONNECT_FAIL:", repr(e)); return
    payload = {
        "deviceid": DEVICEID,
        "data": {},
        "sequence": str(int(time.time()*1000)),
    }
    try:
        s.sendall(json.dumps(payload).encode())
        s.settimeout(4)
        data = s.recv(4096)
        print("GOT_RESPONSE len=", len(data))
        print("RAW_HEX(first 80)=", data[:80].hex())
        try:
            print("RAW_TEXT=", data.decode('utf-8', 'replace'))
        except Exception:
            pass
    except Exception as e:
        print("NO_RESPONSE:", repr(e))
    finally:
        s.close()

print("=== Direct eWeLink LAN handshake test to %s:%d ===" % (IP, PORT))
try_tcp_hello()
