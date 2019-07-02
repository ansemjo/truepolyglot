# -*- coding: utf-8 -*-

"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

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
    from Truepolyglot.PdfFileTransformer import Pdf
    from Truepolyglot.ZipFileTransformer import Zip

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
