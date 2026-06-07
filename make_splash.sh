#!/bin/bash
set -e

SPLASH_SIZE=34226176

if [ ! -f "DONTDELETE.img" ]; then
    echo "ERROR: DONTDELETE.img yok"
    exit 1
fi

if [ ! -f "pics/boot.png" ]; then
    echo "ERROR: pics/boot.png yok"
    exit 1
fi

mkdir -p .tmp_bmp

dd if=DONTDELETE.img of=.tmp_bmp/header.img bs=1 count=16384 status=none

python3 bmp_tool.py make pics/boot.png .tmp_bmp/boot.bmp 1080 2160

cat .tmp_bmp/header.img .tmp_bmp/boot.bmp > .tmp_bmp/new_raw.img

RAW_SIZE=$(stat -c%s .tmp_bmp/new_raw.img)

if [ "$RAW_SIZE" -gt "$SPLASH_SIZE" ]; then
    echo "ERROR: new-splash.img fazla buyuk: $RAW_SIZE > $SPLASH_SIZE"
    rm -rf .tmp_bmp
    exit 1
fi

dd if=.tmp_bmp/new_raw.img of=new-splash.img bs=1 count=$RAW_SIZE status=none
truncate -s "$SPLASH_SIZE" new-splash.img

rm -rf .tmp_bmp

echo "Islem tamamlandi : new-splash.img oluşturuldu. | @yigityanik"