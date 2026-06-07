#!/usr/bin/env python3
import sys
import struct
from PIL import Image

WIDTH = 720
HEIGHT = 1440

def u32le(b):
    return struct.unpack("<I", b)[0]

def decode_qsplash(inp, out):
    data = open(inp, "rb").read()

    if data[:8] != b"SPLASH!!":
        raise SystemExit("ERROR: SPLASH!! header yok")

    w = u32le(data[8:12])
    h = u32le(data[12:16])
    typ = u32le(data[16:20])
    blocks = u32le(data[20:24])

    if typ != 1:
        raise SystemExit("ERROR: RLE24 type degil")

    payload = data[512:512 + blocks * 512]
    pixels = []
    i = 0
    need = w * h

    while i < len(payload) and len(pixels) < need:
        c = payload[i]
        i += 1

        if c < 128:
            n = c + 1
            for _ in range(n):
                b = payload[i]
                g = payload[i + 1]
                r = payload[i + 2]
                i += 3
                pixels.append((r, g, b))
        else:
            n = c - 127
            b = payload[i]
            g = payload[i + 1]
            r = payload[i + 2]
            i += 3
            pixels.extend([(r, g, b)] * n)

    img = Image.new("RGB", (w, h))
    img.putdata(pixels[:need])
    img.save(out)

def encode_rle24(img):
    img = img.convert("RGB")
    pixels = list(img.getdata())
    out = bytearray()
    i = 0
    total = len(pixels)

    while i < total:
        run_len = 1

        while (
            i + run_len < total
            and pixels[i + run_len] == pixels[i]
            and run_len < 128
        ):
            run_len += 1

        if run_len >= 2:
            out.append(127 + run_len)
            r, g, b = pixels[i]
            out += bytes([b, g, r])
            i += run_len
        else:
            raw = []

            while i < total:
                raw.append(pixels[i])
                i += 1

                if len(raw) >= 128:
                    break

                if i + 1 < total and pixels[i] == pixels[i + 1]:
                    break

            out.append(len(raw) - 1)

            for r, g, b in raw:
                out += bytes([b, g, r])

    return bytes(out)

def encode_qsplash(inp, out, target_size):
    img = Image.open(inp)

    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)

    body = encode_rle24(img)
    blocks = (len(body) + 511) // 512

    header = bytearray(512)
    header[0:8] = b"SPLASH!!"
    header[8:12] = struct.pack("<I", WIDTH)
    header[12:16] = struct.pack("<I", HEIGHT)
    header[16:20] = struct.pack("<I", 1)
    header[20:24] = struct.pack("<I", blocks)

    blob = bytes(header) + body
    blob += b"\x00" * ((512 - (len(blob) % 512)) % 512)

    if len(blob) > target_size:
        raise SystemExit(
            "ERROR: gorsel fazla buyuk: %d > %d\n"
            "Daha dusuk gorsel boyutu gereklidir."
            % (len(blob), target_size)
        )

    blob += b"\x00" * (target_size - len(blob))

    with open(out, "wb") as f:
        f.write(blob)

def usage():
    print("usage:")
    print("  python3 qsplash_tool.py decode input.qsplash output.png")
    print("  python3 qsplash_tool.py encode input.png output.qsplash target_size")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "decode":
        decode_qsplash(sys.argv[2], sys.argv[3])
    elif mode == "encode":
        if len(sys.argv) != 5:
            usage()
            sys.exit(1)
        encode_qsplash(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    else:
        usage()
        sys.exit(1)
