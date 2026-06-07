#!/usr/bin/env python3
import sys
from PIL import Image

def main():
    if len(sys.argv) != 6:
        print("usage: python3 bmp_fit.py input output width height target_size")
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2]
    width = int(sys.argv[3])
    height = int(sys.argv[4])
    target_size = int(sys.argv[5])

    img = Image.open(inp).convert("RGB")

    if img.size != (width, height):
        img = img.resize((width, height), Image.LANCZOS)

    img.save(out, "BMP")

    data = open(out, "rb").read()

    if target_size > 0:
        if len(data) > target_size:
            raise SystemExit(
                "ERROR: BMP fazla buyuk: %d > %d" % (len(data), target_size)
            )

        data += b"\x00" * (target_size - len(data))

        with open(out, "wb") as f:
            f.write(data)

if __name__ == "__main__":
    main()