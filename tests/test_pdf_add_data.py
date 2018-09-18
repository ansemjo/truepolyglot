#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import logging
from PdfFileTransformer import Pdf


input_file = "./samples/test1.pdf"
output_file = "./samples/test1_out.pdf"

logging.basicConfig(level=logging.DEBUG)

p = Pdf(input_file)
p.insert_new_obj_stream_at_start(b'A' * 140)
p.insert_new_obj_stream_at_end(b'B' * 120)
f = open(output_file, 'wb')
f.write(p.get_build_buffer())
f.close()
