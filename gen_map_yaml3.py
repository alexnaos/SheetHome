ids = [l.strip() for l in open(r"C:\Temp\ids.txt", encoding="utf-8-sig") if l.strip()]
assert len(ids) == 34, len(ids)

HOME_LAT = 55.586173527410885
HOME_LON = 39.4296419620514

id_list = "\n".join(f"          - device_tracker.{i}" for i in ids)
for_each_list = "\n".join(f"          - 'device_tracker.{i}'" for i in ids)


def see_block(entity_expr):
    """Блок if/then/else с device_tracker.see для одного entity_id-выражения."""
    if entity_expr == "trigger":
        suffix_expr = "trigger.entity_id.split('.')[1]"
        name_expr = "state_attr(trigger.entity_id, 'friendly_name') or trigger.entity_id.split('.')[1]"
        state_expr = "trigger.entity_id"
    else:
        suffix_expr = "repeat.item.split('.')[1]"
        name_expr = "state_attr(repeat.item, 'friendly_name') or repeat.item.split('.')[1]"
        state_expr = "repeat.item"
    return f"""            - if:
                - condition: template
                  value_template: "{{{{ is_state('{state_expr}', 'home') }}}}"
              then:
                - action: device_tracker.see
                  data:
                    dev_id: "{{{{ 'karta_' ~ {suffix_expr} }}}}"
                    host_name: "{{{{ {name_expr} }}}}"
                    location_name: home
                    gps: [{HOME_LAT}, {HOME_LON}]
                    gps_accuracy: 100
                    source_type: router
              else:
                - action: device_tracker.see
                  data:
                    dev_id: "{{{{ 'karta_' ~ {suffix_expr} }}}}"
                    host_name: "{{{{ {name_expr} }}}}"
                    location_name: not_home
                    source_type: router
"""


def reconcile_block():
    """Идемпотентная самосинхронизация: вызывает see только при реальном расхождении."""
    karta = "'device_tracker.karta_' ~ repeat.item.split('.')[1]"
    home_need = (
        "{{ is_state(repeat.item, 'home') and "
        f"(states({karta}) != 'home' or state_attr({karta}, 'latitude') is none)"
        " }}"
    )
    away_need = (
        "{{ is_state(repeat.item, 'not_home') and "
        f"states({karta}) == 'home'"
        " }}"
    )
    return f"""            - if:
                - condition: template
                  value_template: "{home_need}"
              then:
                - action: device_tracker.see
                  data:
                    dev_id: "{{{{ 'karta_' ~ repeat.item.split('.')[1] }}}}"
                    host_name: "{{{{ state_attr(repeat.item, 'friendly_name') or repeat.item.split('.')[1] }}}}"
                    location_name: home
                    gps: [{HOME_LAT}, {HOME_LON}]
                    gps_accuracy: 100
                    source_type: router
            - if:
                - condition: template
                  value_template: "{away_need}"
              then:
                - action: device_tracker.see
                  data:
                    dev_id: "{{{{ 'karta_' ~ repeat.item.split('.')[1] }}}}"
                    host_name: "{{{{ state_attr(repeat.item, 'friendly_name') or repeat.item.split('.')[1] }}}}"
                    location_name: not_home
                    source_type: router
"""


yaml = f"""# Автогенерация: map-трекеры keenetic-устройств через device_tracker.see
# home -> устройство получает координаты дома (точка на карте), иначе — координаты снимаются.
# v3: state-automation (мгновенно) + периодическая самореconciliation (лечит гонку старта и дрейф).
# Сгенерировано: 2026-10-11
automation:
  - id: map_keenetic_state
    alias: "Map: Keenetic state -> map point"
    description: >-
      Мгновенно синхронизирует device_tracker.karta_* (legacy see) при смене
      состояния исходного устройства из Keenetic. При home — gps дома, иначе — not_home.
    mode: queued
    max: 10
    triggers:
      - trigger: state
        entity_id:
{id_list}
    actions:
{see_block('trigger')}
  - id: map_keenetic_reconcile
    alias: "Map: reconcile -> map points"
    description: >-
      Самосинхронизация каждые 2 мин (+ сразу после старта, с задержкой, дождаться
      интеграций). Вызывает see только при расхождении источник<->karta. Лечит гонку
      при старте HA и любой дрейф состояний.
    mode: single
    triggers:
      - trigger: homeassistant
        event: start
      - trigger: time_pattern
        minutes: "/2"
    actions:
      - delay: 00:00:30
      - repeat:
          for_each:
{for_each_list}
          sequence:
{reconcile_block()}
"""

with open(r"W:\home\alex\hass_config\packages\map_tracking.yaml", "w", encoding="utf-8", newline="\n") as f:
    f.write(yaml)
print("written v3, ids:", len(ids))

