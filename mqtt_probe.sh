#!/bin/bash
echo "=== mosquitto_sub present? ==="
which mosquitto_sub || echo NO_SUB
echo "=== RETAINED snapshot (delivered instantly on subscribe) ==="
timeout 3 mosquitto_sub -h 127.0.0.1 -v -t 'ym/#' -t 'yoradio/orange/#' 2>/dev/null
echo "=== LIVE 15s window (is .23 publishing right now?) ==="
timeout 15 mosquitto_sub -h 127.0.0.1 -v -t 'ym/#' -t 'yoradio/orange/#' 2>/dev/null | head -40
echo "=== end ==="
