import time
try:
    from zeroconf import Zeroconf, ServiceBrowser
except Exception as e:
    print("NO_ZEROCONF_MODULE:", repr(e)); raise SystemExit

found = []
class L:
    def add_service(self, zc, t, n):
        try:
            info = zc.get_service_info(t, n)
            ips = []
            try:
                ips = [str(x) for x in info.parsed_addresses()]
            except Exception:
                pass
            found.append((n, info.server if info else "?", ips))
        except Exception as e:
            found.append((n, "ERR:" + repr(e), []))
    def update_service(self, *a): pass
    def remove_service(self, *a): pass

z = Zeroconf()
ServiceBrowser(z, "_ewelink._tcp.local.", L())
time.sleep(6)
z.close()
print("MDNS_SCAN_DONE, found", len(found), "services")
for f in found:
    print("  ", f)
