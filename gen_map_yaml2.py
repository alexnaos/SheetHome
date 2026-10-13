ids = [l.strip() for l in open(r"C:\Temp\ids.txt", encoding="utf-8-sig") if l.strip()]
assert len(ids) == 34, len(ids)

HOME_LAT = 55.586173527410885
HOME_LON = 39.4296419620514

id_list = "\n".join(f"          - device_tracker.{i}" for i in ids)

yaml = f"""# Автогенерация: map-трекеры keenetic-устройств через device_tracker.see
# home -> устройство получает координаты дома (точка на карте), иначе — координаты снимаются.
# Сгенерировано: 2026-10-11
automation:
  - id: map_keenetic_sync
    alias: "Map: Keenetic trackers -> map points"
    description: >-
      Синхронизирует device_tracker.karta_* (legacy see) с состояниями
      device_tracker.* из Keenetic. При home — gps дома, иначе — not_home без gps.
    mode: queued
    max: 10
    triggers:
      - trigger: homeassistant
        event: start
      - trigger: state
        entity_id:
{id_list}
    actions:
      - variables:
          targets: >-
            {{ [trigger.entity_id] if trigger.platform == 'state' else [{','.join("'device_tracker."+i+"'" for i in ids)}] }}
      - repeat:
          for_each: "{{ targets }}"
          sequence:
            - choose:
                - conditions: "{{ is_state(repeat.item, 'home') }}"
                  sequence:
                    - action: device_tracker.see
                      data:
                        dev_id: "karta_{{{{ repeat.item.split('.')[1] }}}}"
                        host_name: "{{{{ state_attr(repeat.item, 'friendly_name') or repeat.item.split('.')[1] }}}}"
                        location_name: home
                        gps: [{HOME_LAT}, {HOME_LON}]
                        gps_accuracy: 100
                        source_type: router
              default:
                - action: device_tracker.see
                  data:
                    dev_id: "karta_{{{{ repeat.item.split('.')[1] }}}}"
                    host_name: "{{{{ state_attr(repeat.item, 'friendly_name') or repeat.item.split('.')[1] }}}}"
                    location_name: not_home
                    source_type: router
"""

with open(r"W:\home\alex\hass_config\packages\map_tracking.yaml", "w", encoding="utf-8", newline="\n") as f:
    f.write(yaml)
print("written, ids:", len(ids))
