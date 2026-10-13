#!/bin/bash
echo "===V4L2 SUPPORTED PIXEL FORMATS==="
sudo -n v4l2-ctl -d /dev/video0 --list-formats 2>/dev/null | grep -i "Pixel Format"
echo
echo "===Full list-formats (first 30 lines)==="
sudo -n v4l2-ctl -d /dev/video0 --list-formats 2>/dev/null | head -30
