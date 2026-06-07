#!/bin/bash
set -e

STOCK="DONTDELETE.img"

if [ ! -f "$STOCK" ]; then
    echo "ERROR: DONTDELETE.img yok"
    exit 1
fi

mkdir -p pics .tmp_qsplash

dd if="$STOCK" of=.tmp_qsplash/boot.qsplash     bs=1 skip=0      count=58880  status=none
dd if="$STOCK" of=.tmp_qsplash/fastboot.qsplash bs=1 skip=58880  count=75264  status=none

python3 qsplash_tool.py decode .tmp_qsplash/boot.qsplash pics/boot.png
python3 qsplash_tool.py decode .tmp_qsplash/fastboot.qsplash pics/fastboot.png

rm -rf .tmp_qsplash

echo "Islem tamamlandi : pics/boot.png ve pics/fastboot.png basariyla cikartildi."
echo "Geri paketlemek icin (bash make_splash.sh) kullan."
