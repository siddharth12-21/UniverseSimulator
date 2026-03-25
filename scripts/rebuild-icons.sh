#!/usr/bin/env bash
# Rebuild build/icon.icns from build/icon.png (1024×1024 PNG with alpha).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/build"
sips -z 1024 1024 icon.png --out icon_1024.png
rm -rf icon.iconset
mkdir -p icon.iconset
for sz in 16 32 64 128 256 512; do
  sips -z "$sz" "$sz" icon_1024.png --out "icon.iconset/icon_${sz}x${sz}.png"
done
for sz in 16 32 128 256 512; do
  dsz=$((sz * 2))
  sips -z "$dsz" "$dsz" icon_1024.png --out "icon.iconset/icon_${sz}x${sz}@2x.png"
done
iconutil -c icns icon.iconset -o icon.icns
rm -rf icon.iconset icon_1024.png
echo "Wrote $ROOT/build/icon.icns"
