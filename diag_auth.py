import json
d = json.load(open("/config/.storage/auth"))
data = d["data"]
print("KEYS:", list(data.keys()))
rts = data.get("refresh_tokens", [])
print("\nREFRESH_TOKENS count:", len(rts))
if rts:
    rt0 = dict(rts[0])
    tok = rt0.get("token","")
    rt0["token"] = tok[:20] + "...(%d)" % len(tok)
    print("sample refresh token fields:", json.dumps(rt0, ensure_ascii=False))
    print("token startswith eyJ(JWT)?", tok.startswith("eyJ"))

# Поиск long-lived access tokens
lla = data.get("auth_module_long_lived_access_tokens") or data.get("long_lived_access_tokens")
print("\nlong_lived_access_tokens:", json.dumps(lla, ensure_ascii=False)[:500] if lla else "NONE")
