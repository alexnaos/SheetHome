#!/bin/bash
echo "===DOCKER NETWORK MODE of homeassistant==="
sudo -n docker inspect -f 'NetworkMode={{.HostConfig.NetworkMode}}' homeassistant
echo
echo "===Can container reach MINIR4 192.168.1.72:8081 (TCP)?==="
sudo -n docker exec homeassistant sh -c 'python3 - <<PY
import socket
s=socket.socket(); s.settimeout(3)
try:
    s.connect(("192.168.1.72",8081)); print("TCP_8081_FROM_CONTAINER=OPEN")
except Exception as e:
    print("TCP_8081_FROM_CONTAINER=FAIL", repr(e))
s.close()
PY'
echo
echo "===Does container see eWeLink mDNS via zeroconf? (scan 3s)==="
sudo -n docker exec homeassistant sh -c 'python3 - <<PY
try:
    from zeroconf import Zeroconf
    from zeroconf._services.info import ServiceInfo
    import time
    z=Zeroconf()
    found=[]
    from zeroconf import ServiceBrowser
    class L:
        def add_service(self,zc,t,n): found.append(n)
        def update_service(self,*a): pass
        def remove_service(self,*a): pass
    ServiceBrowser(z,"_ewelink._tcp.local.",L())
    time.sleep(3)
    print("mDNS_found=",found)
    z.close()
except Exception as e:
    print("MDNS_ERROR",repr(e))
PY'
echo
echo "===ARP from HOST for the device MAC==="
ip neigh | grep -iE "68:fe:71|192.168.1.72" || echo "no arp entry"
