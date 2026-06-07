#!/usr/bin/env python3
import sys
from PIL import Image

def extract_bmp(inp, out):
    img = Image.open(inp).convert("RGB")
    img.save(out)

def make_bmp(inp, out, width, height):
    img = Image.open(inp).convert("RGB")

    if img.size != (width, height):
        img = img.resize((width, height), Image.LANCZOS)

    img.save(out, "BMP")

def usage():
    print("usage:")
    print("  python3 bmp_tool.py extract input.bmp output.png")
    print("  python3 bmp_tool.py make input.png output.bmp width height")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "extract":
        extract_bmp(sys.argv[2], sys.argv[3])
    elif mode == "make":
        if len(sys.argv) != 6:
            usage()
            sys.exit(1)
        make_bmp(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    else:
        usage()
        sys.exit(1)
