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
