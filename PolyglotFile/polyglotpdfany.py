# -*- coding: utf-8 -*-

import logging

'''
    |-------------------------------|    -
    |--------- PDF Header ----------K1   | J1
    |-------------------------------|    -
    |---- PDF OBJ 1 = Payload 1 ----K2   |
    |-------------------------------|    -
    |---- Original PDF Ojbects -----K3   | J2
    |-------------------------------|    -
    |-- PDF Last OBJ = Payload 2 ---K4   |
    |-------------------------------|    |
    |---------- Xref Table ---------|    |
    |-------------------------------K5   |
    |----------- Trailer -----------|    |
    |-------------------------------|    |
'''


class PolyglotPdfAny():
    from PdfFileTransformer import Pdf

    def __init__(self, Pdf, payload1filename, payload2filename):
        self.buffer = bytearray()
        self.pdf = Pdf
        self.payload1 = bytearray()
        if payload1filename is not None:
            with open(payload1filename, "rb") as f:
                self.payload1 = f.read()
        self.payload2 = bytearray()
        if payload2filename is not None:
            with open(payload2filename, "rb") as f:
                self.payload2 = f.read()

        self.buffer = bytearray()

    def generate(self):
        k2stream = self.payload1
        if len(k2stream) > 0:
            self.pdf.insert_new_obj_stream_at_start(k2stream)
        k4stream = self.payload2
        if len(k4stream) > 0:
            self.pdf.insert_new_obj_stream_at_end(k4stream)
        self.buffer = self.pdf.get_build_buffer()

    def write(self, filename):
        fd = open(filename, "wb")
        fd.write(self.buffer)
        fd.close()
