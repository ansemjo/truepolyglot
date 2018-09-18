# -*- coding: utf-8 -*-

from .polyglotpdfzip import PolyglotPdfZip


'''
    |-------------------------------|    -
    |--------- PDF Header ----------K1   | J1
    |-------------------------------|    -
    |----- PDF OBJ 1 = ZIP Data ----K2   |
    |-------------------------------|    -
    |---- Original PDF Ojbects -----K3   |
    |-------------------------------|    |
    |---------- Xref Table ---------|    |
    |-------------------------------K4   | J2
    |----------- Trailer -----------|    |
    |-------------------------------|    -
    |-------- End Zip Data ---------|    |
    |-------------------------------|    |
'''


class PolyglotZipPdf(PolyglotPdfZip):

    def generate(self):
        k2_stream = self.zip.buffer[:self.zip.end_of_data]
        size_k2_stream = len(k2_stream)
        self.pdf.insert_new_obj_stream_at_start(k2_stream)
        offset_k2_stream = self.pdf.get_first_stream_offset()

        pdf_buffer = self.pdf.get_build_buffer()

        j1 = pdf_buffer[0:offset_k2_stream]
        j2 = pdf_buffer[offset_k2_stream + size_k2_stream:]

        self.zip.add_data_to_file(j1, j2, True)
        self.buffer = self.zip.buffer
