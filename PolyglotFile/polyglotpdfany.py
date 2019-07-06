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
