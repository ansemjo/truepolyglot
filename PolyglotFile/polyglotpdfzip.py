# -*- coding: utf-8 -*-

import logging

'''
    |-------------------------------|    -
    |--------- PDF Header ----------K1   | J1
    |-------------------------------|    -
    |----- PDF OBJ 1 = ZIP Data ----K2   |
    |-------------------------------|    -
    |---- Original PDF Ojbects -----K3   | J2
    |-------------------------------|    -
    |--- Last OBJ = End Zip Data ---K4   |
    |-------------------------------|    |
    |---------- Xref Table ---------|    |
    |-------------------------------K5   |
    |----------- Trailer -----------|    |
    |-------------------------------|    |
'''


class PolyglotPdfZip():
    from PdfFileTransformer import Pdf
    from ZipFileTransformer import Zip

    def __init__(self, Pdf, Zip):
        self.buffer = bytearray()
        self.pdf = Pdf
        self.zip = Zip
        self.buffer = bytearray()

    def generate(self):
        k2_stream = self.zip.buffer[:self.zip.end_of_data]
        size_k2_stream = len(k2_stream)
        self.pdf.insert_new_obj_stream_at_start(k2_stream)
        offset_k2_stream = self.pdf.get_first_stream_offset()

        k4_stream = self.zip.buffer[self.zip.central_dir_file_header:]
        size_k4_stream = len(k4_stream)
        self.pdf.insert_new_obj_stream_at_end(k4_stream)
        offset_k4_stream = self.pdf.get_last_stream_offset()

        pdf_buffer = self.pdf.get_build_buffer()

        j1 = pdf_buffer[0:offset_k2_stream]
        j2 = pdf_buffer[offset_k2_stream + size_k2_stream:offset_k4_stream]
        self.zip.add_data_to_file(j1, j2, True)

        k5 = pdf_buffer[offset_k4_stream + size_k4_stream:]
        self.buffer = self.zip.buffer + k5

    def write(self, filename):
        fd = open(filename, "wb")
        fd.write(self.buffer)
        fd.close()
