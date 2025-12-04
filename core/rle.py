# core/rle.py
from .compressor import Compressor
import numpy as np
import struct

class RLECompressor(Compressor):
    def encode(self, img: np.ndarray):
        flat = img.flatten()
        enc = bytearray()
        i = 0
        while i < len(flat):
            val = flat[i]
            count = 1
            i += 1
            while i < len(flat) and flat[i] == val and count < 255:
                count += 1
                i += 1
            enc.append(val)
            enc.append(count)
        return bytes(enc), None

    def decode(self, data: bytes, metadata, shape):
        out = []
        i = 0
        while i < len(data):
            val, cnt = data[i], data[i+1]
            out.extend([val] * cnt)
            i += 2
        return np.array(out, dtype=np.uint8).reshape(shape)

    def save_file(self, path: str, data: bytes, metadata, shape):
        h, w, c = shape
        with open(path, "wb") as f:
            f.write(b"RLE0")
            f.write(struct.pack("<III", h, w, c))
            f.write(data)

    def load_file(self, path: str):
        with open(path, "rb") as f:
            if f.read(4) != b"RLE0":
                raise ValueError("Invalid .rle file")
            h, w, c = struct.unpack("<III", f.read(12))
            data = f.read()
            return self.decode(data, None, (h, w, c))

    @property
    def name(self):
        return "RLE"