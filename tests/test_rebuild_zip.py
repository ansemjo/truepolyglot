#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import tempfile

from ZipFileTransformer import Zip, ZipFile

input_file = "./samples/test1.zip"
output_file = "./samples/test1_out.zip"

zi = ZipFile(input_file,"r")
zo = ZipFile(output_file,"w")
zo.writestr(' ',b'AAAAAAAAAAAAAAAAAAAAAA',0)
for zipinfo in zi.infolist():
    zo.writestr(zipinfo, zi.read(zipinfo))
zi.close()
zo.close()