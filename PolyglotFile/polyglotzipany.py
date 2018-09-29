# -*- coding: utf-8 -*-

import logging

'''
    |-------------------------------|    -
    |---------- Payload 1 ----------K1   | J1
    |-------------------------------|    -
    |---- ZIP Local File Header ----K2   |
    |-------------------------------|    -
    |---------- Payload 2-----------K3   | J2
    |-------------------------------|    -
    |---- ZIP Central Directory ----K4   |
    |-------------------------------|    |
    |--- End of Central Directory --K5   |
    |-------------------------------|    |
'''


class PolyglotZipAny():
    from ZipFileTransformer import Zip

    def __init__(self, Zip, payload1filename, payload2filename):
        self.buffer = bytearray()
        self.zip = Zip
        self.payload1 = bytearray()
        if payload1filename is not None:
            with open(payload1filename, "rb") as f:
                self.payload1 = f.read()
        self.payload2 = bytearray()
        if payload2filename is not None:
            with open(payload2filename, "rb") as f:
                self.payload2 = f.read()

    def generate(self):
        self.zip.add_data_to_file(self.payload1, self.payload2, True)
        self.buffer = self.zip.buffer

    def write(self, filename):
        fd = open(filename, "wb")
        fd.write(self.buffer)
        fd.close()
