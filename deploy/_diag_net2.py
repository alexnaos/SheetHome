import subprocess, sys

def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        return "ERR:" + repr(e)

print("=== NetworkMode ===")
print(sh("sudo -n docker inspect -f '{{.HostConfig.NetworkMode}}' homeassistant"))

print("\n=== TCP 192.168.1.72:8081 from INSIDE container ===")
py = (
    "import socket;s=socket.socket();s.settimeout(3)\n"
    "try:\n s.connect(('192.168.1.72',8081));print('TCP_OPEN')\n"
    "except Exception as e:\n print('TCP_FAIL',repr(e))\n"
    "s.close()"
)
print(sh("sudo -n docker exec homeassistant python3 -c " + repr(py).replace("'", "'\\''")))

print("\n=== mDNS _ewelink._tcp.local. discovery INSIDE container (5s) ===")
mdns = (
    "from zeroconf import Zeroconf, ServiceBrowser\n"
    "import time\n"
    "found=[]\n"
    "class L:\n"
    " def add_service(self,zc,t,n): found.append(n)\n"
    " def update_service(self,*a): pass\n"
    " def remove_service(self,*a): pass\n"
    "z=Zeroconf(); ServiceBrowser(z,'_ewelink._tcp.local.',L()); time.sleep(5)\n"
    "print('MDNS_FOUND=',found); z.close()"
)
print(sh("sudo -n docker exec homeassistant python3 -c " + repr(mdns).replace("'", "'\\''")))

print("\n=== HOST ARP for 192.168.1.72 ===")
print(sh("ip neigh | grep -i '192.168.1.72' || echo NO_ARP"))
