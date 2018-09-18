#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from PdfFileTransformer import Pdf
from ZipFileTransformer import Zip
from PolyglotFile import PolyglotPdfZip
import logging

input_file_pdf = "./samples/test1.pdf"
input_file_zip = "./samples/test1.zip"
output_file = "./samples/test1_out.pdf"

logging.basicConfig(level=logging.DEBUG)


p = Pdf(input_file_pdf)
z = Zip(input_file_zip)
a = PolyglotPdfZip(p, z)
a.generate()
a.write(output_file)
