import subprocess

def sh(c, t=8):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)
    return (r.stdout or "") + (r.stderr or "")

print("=== who is pid 1314 (parent of both go2rtc)? ===")
print(sh("sudo -n ps -eo pid,ppid,comm,args -p 1314 | cat"))
print()
print("=== what starts /config/go2rtc-1.9.9? search shell_command/automation/yaml ===")
print(sh("sudo -n grep -rIl 'go2rtc-1.9.9\\|go2rtc-1\\|go2rtc ' /home/alex/hass_config/*.yaml /home/alex/hass_config/packages/ /home/alex/hass_config/automations.yaml 2>/dev/null | head"))
print("--- shell_command in config ---")
print(sh("sudo -n grep -rn -A6 'shell_command:' /home/alex/hass_config/configuration.yaml /home/alex/hass_config/packages/*.yaml 2>/dev/null | head -40"))
print()
print("=== built-in go2rtc temp yaml content ===")
print(sh("sudo -n cat /tmp/go2rtc-*/go2rtc_*.yaml 2>/dev/null | head -40 || echo 'no temp yaml readable from host (it is inside HA container ns)'"))
print()
print("=== is /config/go2rtc.yaml the one built-in reads? check go2rtc integration default ===")
print("NOTE: HA go2rtc integration reads <config>/go2rtc.yaml and creates camera.<name> entities (platform=go2rtc)")
