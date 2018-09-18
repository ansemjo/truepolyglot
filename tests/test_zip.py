#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import tempfile

from ZipFileTransformer import Zip

input_file = "./samples/test1.zip"
output_file = tempfile.mktemp()
print("Output: " + output_file)

z = Zip(input_file)
a = bytearray(b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
b = bytearray(b'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
z.add_data_to_file(a, b, False)
g = open(output_file, "wb")
g.write(a + z.get_local_file_data() + b + z.get_data_after_central_directory())
g.close()
