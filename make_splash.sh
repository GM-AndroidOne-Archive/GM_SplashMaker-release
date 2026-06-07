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

if [ ! -f "pics/fastboot.png" ]; then
    echo "ERROR: pics/fastboot.png yok"
    exit 1
fi

mkdir -p .tmp_qsplash

python3 qsplash_tool.py encode pics/boot.png .tmp_qsplash/boot.qsplash 58880
python3 qsplash_tool.py encode pics/fastboot.png .tmp_qsplash/fastboot.qsplash 75264

dd if=DONTDELETE.img of=.tmp_qsplash/logo3.qsplash bs=1 skip=134144 count=48128 status=none
dd if=DONTDELETE.img of=.tmp_qsplash/logo4.qsplash bs=1 skip=182272 status=none

cat .tmp_qsplash/boot.qsplash \
    .tmp_qsplash/fastboot.qsplash \
    .tmp_qsplash/logo3.qsplash \
    .tmp_qsplash/logo4.qsplash > new-splash.img

rm -rf .tmp_qsplash

echo "Islem tamamlandi : new-splash.img oluşturuldu. | @yigityanik"
