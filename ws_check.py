try:
    import websocket
    print("websocket-client OK", getattr(websocket, "__version__", "?"))
except Exception as e:
    print("NO websocket-client:", e)
