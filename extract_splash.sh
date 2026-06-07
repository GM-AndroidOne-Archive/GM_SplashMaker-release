#!/bin/bash
set -e

STOCK="DONTDELETE.img"

if [ ! -f "$STOCK" ]; then
    echo "ERROR: DONTDELETE.img yok"
    exit 1
fi

mkdir -p pics .tmp_bmp

dd if="$STOCK" of=.tmp_bmp/boot.bmp bs=1 skip=16384 count=6998454 status=none

python3 bmp_tool.py extract .tmp_bmp/boot.bmp pics/boot.png

rm -rf .tmp_bmp

echo "Islem tamamlandi : pics/boot.png basariyla cikartildi."
echo "Geri paketlemek icin (bash make_splash.sh) kullan."