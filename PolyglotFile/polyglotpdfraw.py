# -*- coding: utf-8 -*-

import logging

'''
    |-------------------------------|    -
    |--------- PDF Header ----------K1   | J1
    |-------------------------------|    -
    |----- PDF OBJ 1 = RAW Data ----K2   |
    |-------------------------------|    -
    |---- Original PDF Ojbects -----K3   | J2
    |-------------------------------|    -
    |---------- Xref Table ---------|    |
    |-------------------------------K5   |
    |----------- Trailer -----------|    |
    |-------------------------------|    |
'''


class PolyglotPdfRaw():
    from PdfFileTransformer import Pdf

    def __init__(self, Pdf, Raw_filename):
        self.buffer = bytearray()
        self.pdf = Pdf
        self.raw_filename = Raw_filename
        self.buffer = bytearray()

    def generate(self):
        raw_buffer = bytearray()
        with open(self.raw_filename, "rb") as f:
            raw_buffer = f.read()
        k2_stream = raw_buffer
        self.pdf.insert_new_obj_stream_at_start(k2_stream)
        self.buffer = self.pdf.get_build_buffer()

    def write(self, filename):
        fd = open(filename, "wb")
        fd.write(self.buffer)
        fd.close()
