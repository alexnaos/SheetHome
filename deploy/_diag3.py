import subprocess

def run(cmd, sudo=False):
    full = (["sudo", "-n"] + cmd) if sudo else cmd
    try:
        p = subprocess.run(full, capture_output=True, text=True, timeout=25)
        out = (p.stdout or "") + (p.stderr or "")
        return out.strip()
    except Exception as e:
        return f"ERR: {e}"

print("=== ip neigh (device 68:fe:71) ===")
print(run(["bash", "-lc", "ip neigh | grep -i 68:fe:71 || echo NO-ARP"]))

print("\n=== ping 192.168.1.72 ===")
print(run(["bash", "-lc", "ping -c 2 -W 2 192.168.1.72 | tail -4"]))

print("\n=== host TCP 8081 ===")
print(run(["bash", "-lc", "timeout 3 bash -c 'cat < /dev/null > /dev/tcp/192.168.1.72/8081' && echo PORT_OPEN || echo PORT_CLOSED"]))

print("\n=== mDNS: does MINIR4 advertise _ewelink._tcp ? ===")
print(run(["bash", "-lc", "which avahi-browse avahi-resolve getent 2>&1; echo '--- browse ---'; avahi-browse -trp _ewelink._tcp 2>&1 | head -40 || echo NO-AVAHI-BROWSE"]))

print("\n=== SonoffLAN log (last boot, sonoff/ewelink/local/discovery) ===")
print(run(["bash", "-lc", "sudo -n docker logs homeassistant 2>&1 | grep -iE 'sonoff|ewelink|100284|_ewelink|local mode|discover|Can.t login' | tail -50"]))

print("\n=== 'not currently available' recent ===")
print(run(["bash", "-lc", "sudo -n docker logs homeassistant 2>&1 | grep -i 'not currently available' | tail -15"]))
