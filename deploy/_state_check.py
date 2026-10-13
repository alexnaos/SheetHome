import sqlite3, os
db = "/home/alex/hass_config/home-assistant_v2.db"
try:
    con = sqlite3.connect(db)
    cur = con.cursor()
    # find metadata id for the entity
    row = cur.execute("SELECT metadata_id, entity_id FROM states_meta WHERE entity_id = ?", ("switch.sonoff_100284cd66_1",)).fetchone()
    if not row:
        print("NO_METADATA for switch.sonoff_100284cd66_1")
    else:
        mid = row[0]
        rows = cur.execute("SELECT state, last_updated_ts FROM states WHERE metadata_id = ? ORDER BY last_updated_ts DESC LIMIT 8", (mid,)).fetchall()
        print("last states (newest first):")
        for r in rows:
            import datetime
            ts = datetime.datetime.utcfromtimestamp(r[1]).strftime("%Y-%m-%d %H:%M:%S")
            print("  ", r[0], "@", ts, "UTC")
    con.close()
except Exception as e:
    print("DB_ERROR:", repr(e))
