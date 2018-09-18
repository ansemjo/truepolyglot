#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from PdfFileTransformer import Pdf
import logging

input_file = "./samples/test1.pdf"
output_file = "./samples/test1_out.pdf"

logging.basicConfig(level=logging.DEBUG)


p = Pdf(input_file)
f = open(output_file, 'wb')
f.write(p.get_build_buffer())
f.close()
