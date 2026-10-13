#!/bin/bash
echo "=== Full ARP/neigh table ==="
ip neigh | grep -iE "192.168.1." | sort
echo
echo "=== Devices with TCP 8081 open (eWeLink LAN port) in 192.168.1.0/24 ==="
for i in $(seq 2 254); do
  ip="192.168.1.$i"
  (timeout 1 bash -c "cat < /dev/null > /dev/tcp/$ip/8081" 2>/dev/null && echo "8081 OPEN on $ip") &
done
wait
echo "=== scan done ==="
