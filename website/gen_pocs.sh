#!/bin/bash

find -type f -name 'polyglot.pdf' -delete

mkdir -p ./samples/pdfzip/poc1/
../truepolyglot pdfzip --pdffile ./samples/pdfzip/poc1/doc.pdf --zipfile ./samples/pdfzip/poc1/archive.zip ./samples/pdfzip/poc1/polyglot.pdf

mkdir -p ./samples/pdfzip/poc2/
../truepolyglot pdfzip --pdffile ./samples/pdfzip/poc2/orwell_1984.pdf --zipfile ./samples/pdfzip/poc2/file-FILE5_32.zip ./samples/pdfzip/poc2/polyglot.pdf

mkdir -p ./samples/pdfzip/poc3/
../truepolyglot pdfzip --pdffile ./samples/pdfzip/poc3/x86asm.pdf --zipfile ./samples/pdfzip/poc3/fasmw17304.zip ./samples/pdfzip/poc3/polyglot.pdf

mkdir -p ./samples/zippdf/poc4/
../truepolyglot zippdf --pdffile ./samples/zippdf/poc4/doc.pdf --zipfile ./samples/zippdf/poc4/archive.zip ./samples/zippdf/poc4/polyglot.pdf

mkdir -p ./samples/szippdf/poc5/
../truepolyglot szippdf --pdffile ./samples/szippdf/poc5/electronics.pdf --zipfile ./samples/szippdf/poc5/hello_world.jar ./samples/szippdf/poc5/polyglot.pdf

mkdir -p ./samples/pdfzip/poc6/
../truepolyglot pdfzip --pdffile ./samples/pdfzip/poc6/hexinator.pdf --zipfile ./samples/pdfzip/poc6/eicar.zip ./samples/pdfzip/poc6/polyglot.pdf
