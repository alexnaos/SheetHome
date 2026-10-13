import socket
import time
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf

# 1) Proper mDNS/zeroconf browse for _ewelink._tcp.local
found = []
def on_change(zeroconf, service_type, name, state_change):
    if state_change is ServiceStateChange.Added:
        try:
            info = zeroconf.get_service_info(service_type, name, timeout=3000)
            addr = socket.inet_ntoa(info.addresses[0]) if info and info.addresses else "?"
            port = info.port if info else "?"
        except Exception as e:
            addr, port = f"err:{e}", "?"
        found.append((name, addr, port))

print("=== zeroconf browse _ewelink._tcp.local (6s) ===")
zc = Zeroconf()
ServiceBrowser(zc, "_ewelink._tcp.local.", handlers=[on_change])
time.sleep(6)
zc.close()
if found:
    for n, a, p in found:
        print(f"  FOUND {n} @ {a}:{p}")
    print("VERDICT: device advertises mDNS")
else:
    print("  (none)")
    print("VERDICT: NO _ewelink mDNS advertisement")

# 2) Cloud WS reachability (eWeLink endpoints)
print("\n=== eWeLink cloud endpoint reachability (TCP) ===")
for host, port in [("eu-dispa.coolkit.cc", 443), ("eu-dispa.coolkit.cc", 8080),
                   ("eu-ota.coolkit.cc", 443), ("eu-disp.coolkit.cc", 8080)]:
    try:
        ip = socket.gethostbyname(host)
        s = socket.socket(); s.settimeout(4)
        t0 = time.time()
        s.connect((ip, port))
        dt = int((time.time() - t0) * 1000)
        s.close()
        print(f"  {host}:{port} ({ip}) OK in {dt}ms")
    except Exception as e:
        print(f"  {host}:{port} FAIL {type(e).__name__}: {e}")
