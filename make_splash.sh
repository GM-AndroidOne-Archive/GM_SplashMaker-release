#!/bin/bash
set -e

if [ ! -f "DONTDELETE.img" ]; then
    echo "ERROR: DONTDELETE.img yok"
    exit 1
fi

if [ ! -f "pics/boot.png" ]; then
    echo "ERROR: pics/boot.png yok"
    exit 1
fi

mkdir -p .tmp_qsplash

python3 qsplash_tool.py encode pics/boot.png .tmp_qsplash/boot.qsplash 11534336

cat .tmp_qsplash/boot.qsplash > new-splash.img

rm -rf .tmp_qsplash

echo "Islem tamamlandi : new-splash.img oluşturuldu. | @yigityanik"