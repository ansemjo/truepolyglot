#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
import logging
from PdfFileTransformer.PyPDF2 import PdfFileReader, PdfFileWriter


input_file = "./samples/test1.pdf"
output_file = "./samples/test1_out.pdf"

logging.basicConfig(level=logging.DEBUG)

f_input = open(input_file, "rb")
reader = PdfFileReader(f_input)

f_output = open(output_file, "wb")
writer = PdfFileWriter()

writer.appendPagesFromReader(reader)
writer.setHeader(b"%PDF-1.5")
writer.write(f_output)

f_input.close()
f_output.close()
