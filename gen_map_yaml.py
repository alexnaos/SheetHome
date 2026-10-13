#!/usr/bin/env python3
# Генерирует packages/map_tracking.yaml:
#  - template device_tracker для каждогоkeenetic-трекера (координаты = зона home, когда устройство home)
#  - telegram/... не нужен. Только карта.
import json, datetime

REG="/config/.storage/core.entity_registry"
reg=json.load(open(REG))
keens=[e["entity_id"] for e in reg["data"]["entities"]
       if e.get("entity_id","").startswith("device_tracker.")
       and e.get("platform")=="keenetic_ndms2"]
keens=sorted(set(keens))
print("keenetic trackers:", len(keens))

HOME_LAT="55.586173527410885"
HOME_LON="39.4296419620514"

lines=[]
lines.append("# Автогенерация: template device_tracker'ыkeenetic-устройств для отображения на карте")
lines.append("# Когда устройство 'home' -> координаты зоны home (точка на карте), иначе -> не показывается.")
lines.append(f"# Сгенерировано: {datetime.datetime.now().isoformat(timespec='seconds')}")
lines.append("template:")
lines.append("  - device_tracker:")
for eid in keens:
    short=eid.replace("device_tracker.","")
    lines.append(f"      - name: \"Карта {short}\"")
    lines.append(f"        unique_id: map_track_{short}")
    lines.append(f"        state: >-")
    lines.append(f"          {{{{ 'home' if is_state('{eid}', 'home') else 'not_home' }}}}")
    lines.append(f"        attributes:")
    lines.append(f"          source_type: >-")
    lines.append(f"            {{{{ 'router' if is_state('{eid}', 'home') else 'none' }}}}")
    lines.append(f"          latitude: >-")
    lines.append(f"            {{{{ {HOME_LAT} if is_state('{eid}', 'home') else none }}}}")
    lines.append(f"          longitude: >-")
    lines.append(f"            {{{{ {HOME_LON} if is_state('{eid}', 'home') else none }}}}")

out="/config/packages/map_tracking.yaml"
import os
os.makedirs("/config/packages", exist_ok=True)
with open(out,"w",encoding="utf-8") as f:
    f.write("\n".join(lines)+"\n")
print("WRITTEN:", out, "lines:", len(lines))
