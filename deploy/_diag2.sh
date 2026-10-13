#!/bin/bash
echo "===ARP by MAC 68:fe:71==="
ip neigh | grep -i 68:fe:71 || echo NO-ARP-ENTRY
echo
echo "===ping 192.168.1.72==="
ping -c 2 -W 2 192.168.1.72 2>&1 | tail -4
echo
echo "===port 8081 from host==="
(timeout 3 bash -c "cat < /dev/null > /dev/tcp/192.168.1.72/8081" && echo PORT_OPEN) || echo PORT_CLOSED
echo
echo "===mDNS tools present==="
which avahi-browse avahi-resolve getent 2>&1
echo "===mDNS resolve eWeLink_100284cd66.local==="
getent hosts eWeLink_100284cd66.local 2>&1 || echo GETENT-NONE
avahi-resolve -n eWeLink_100284cd66.local 2>&1 | head -3 || echo AVAHI-NONE
echo "===avahi-browse ewelink==="
avahi-browse -trp _ewelink._tcp 2>&1 | head -30 || echo NO-AVAHI-BROWSE
echo
echo "===SONOFF LOG last 60==="
sudo -n docker logs homeassistant 2>&1 | grep -iE "sonoff|ewelink|100284|_ewelink|zeroconf|local mode|Can.t login" | tail -60
echo
echo "===not available last 15==="
sudo -n docker logs homeassistant 2>&1 | grep -i "not currently available" | tail -15