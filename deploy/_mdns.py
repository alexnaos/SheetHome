import socket
import struct

# Minimal raw mDNS query for PTR _ewelink._tcp.local to 224.0.0.251:5353
def mdns_query(name, timeout=5):
    q = bytearray()
    # header: id=0, flags=0, qdcount=1
    q += struct.pack(">HHHHHH", 0, 0, 1, 0, 0, 0)
    for part in name.split("."):
        q.append(len(part))
        q += part.encode()
    q += b"\x00"
    q += struct.pack(">HH", 12, 1)  # PTR, IN
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    s.settimeout(timeout)
    try:
        s.sendto(bytes(q), ("224.0.0.251", 5353))
        data, addr = s.recvfrom(4096)
        # crude: count how many ".local" names appear
        txt = data
        found = []
        i = 0
        while True:
            i = txt.find(b"_ewelink", i)
            if i < 0:
                break
            found.append(i)
            i += 1
        return len(data), addr[0], len(found)
    except socket.timeout:
        return 0, None, 0
    finally:
        s.close()

print("=== mDNS query _ewelink._tcp.local (expect responses if device advertises) ===")
n, src, hits = mdns_query("_ewelink._tcp.local", timeout=5)
print(f"response_bytes={n} from={src} ewelink_hits={hits}")
print("VERDICT:", "DEVICE ADVERTISES mDNS" if hits > 0 else "NO mDNS advertisement seen for _ewelink")
