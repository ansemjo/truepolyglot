Truepolyglot is polyglot file generator project. It means  the generated file is composed of several file formats. The same file can be opened as a ZIP file and as a PDF file for example. The idea of this project comes from the work of [Ange Albertini](https://github.com/corkami), [International Journal of Proof-of-Concept or Get The Fuck Out](https://www.alchemistowl.org/pocorgtfo/pocorgtfo07.pdf) and [Julia Wolf](https://www.troopers.de/wp-content/uploads/2011/04/TR11_Wolf_OMG_PDF.pdf) that explain how we can build a polyglot file.\
Polyglot file can be boring to build, even more if you want to respect the file format correctly.\
That's why I decided to build a tool to generate them.\
My main motivation was the technical challenge.

## Features and versions ##

| Description | Version |
| ----------- | ------- |
| Build a polyglot file valid as PDF and ZIP format and that can be opened with 7Zip and Windows Explorer | POC |
| Add a stream object in the PDF part | POC |
| Polyglot file checked without warning with [pdftocairo](https://poppler.freedesktop.org/) | >= 1.0 |
| Polyglot file checked without warning with [caradoc](https://github.com/ANSSI-FR/caradoc) | >= 1.0 |
| Rebuild the PDF Xref Table | >= 1.0 |
| Stream object with the correct length header value | >= 1.0 |
| Add the format "zippdf", file without offset after the Zip data | >= 1.1 |
| Polyglot file keeps the original PDF version | >= 1.1.1 |
| Add the "szippdf" format without offset before and after the Zip data | >= 1.2 |
| Fix /Length stream object value and the PDF offset for the szippdf format | >= 1.2.1 |
| PDF object numbers reorder after insertion | >= 1.3 |
| Add the format "pdfany" a valid PDF with custom payload content in the first and the last objet | >= 1.5.2 |
| Add "acrobat-compatibility" option to allow szippdf to be read with Acrobat Reader (thanks Ange Albertini)| >= 1.5.3 |
| Add the format "zipany" a valid ZIP with custom payload content at the start and between LHF and CD | >= 1.6 |

## Polyglot file compatibility ##

| Software | Formats | status |
| -------- | ------- | ------ |
| Acrobat Reader | pdfzip, zippdf, szippdf, pdfany | OK |
| Sumatra PDF | pdfzip, zippdf, szippdf, pdfany | OK |
| Foxit PDF Reader | pdfzip, zippdf, szippdf, pdfany | OK |
| Edge | pdfzip, zippdf, szippdf, pdfany | OK |
| Firefox | pdfzip, zippdf, szippdf, pdfany | OK |
| 7zip | pdfzip, zippdf, zipany | OK with warning |
| 7zip | szippdf | OK |
| Explorer Windows | pdfzip, zippdf, szippdf, pdfany, zipany | OK |
| Info-ZIP (unzip) | pdfzip, zippdf, szippdf, pdfany, zipany | OK |
| Evince | pdfzip, zippdf, szippdf, pdfany | OK |
| pdftocairo -pdf | pdfzip, zippdf, szippdf, pdfany | OK |
| caradoc stats | pdfzip, pdfany | OK |
| java -jar | szippdf | OK |

## Examples ##

| First input file | Second input file | Format | Polyglot | Comment |
| ---------------- | ----------------- | ------ | -------- | ------- |
| [doc.pdf](https://truepolyglot.hackade.org/samples/pdfzip/poc1/doc.pdf) | [archive.zip](https://truepolyglot.hackade.org/samples/pdfzip/poc1/archive.zip) | pdfzip | [polyglot.pdf](https://truepolyglot.hackade.org/samples/pdfzip/poc1/polyglot.pdf) | PDF/ZIP polyglot - 122 Ko | 
| [orwell\_1984.pdf](https://truepolyglot.hackade.org/samples/pdfzip/poc2/orwell_1984.pdf) | [file-FILE5\_32.zip](https://truepolyglot.hackade.org/samples/pdfzip/poc2/file-FILE5_32.zip) | pdfzip | [polyglot.pdf](https://truepolyglot.hackade.org/samples/pdfzip/poc2/polyglot.pdf) | PDF/ZIP polyglot - 1.3 Mo |
| [x86asm.pdf](https://truepolyglot.hackade.org/samples/pdfzip/poc3/x86asm.pdf) | [fasmw17304.zip](https://truepolyglot.hackade.org/samples/pdfzip/poc3/fasmw17304.zip) | pdfzip | [polyglot.pdf](https://truepolyglot.hackade.org/samples/pdfzip/poc3/polyglot.pdf) | PDF/ZIP polyglot - 1.8 Mo |
| [doc.pdf](/samples/zippdf/poc4/doc.pdf) | [archive.zip](/samples/zippdf/poc4/archive.zip) | zippdf | [polyglot.pdf](/samples/zippdf/poc4/polyglot.pdf) | PDF/ZIP polyglot - 112 Ko |
| [electronics.pdf](https://truepolyglot.hackade.org/samples/szippdf/poc5/electronics.pdf) | [hello\_world.jar](https://truepolyglot.hackade.org/samples/szippdf/poc5/hello_world.jar) | szippdf | [polyglot.pdf](https://truepolyglot.hackade.org/samples/szippdf/poc5/polyglot.pdf) | PDF/JAR polyglot - 778 Ko |
| [hexinator.pdf](https://truepolyglot.hackade.org/samples/pdfzip/poc6/hexinator.pdf) | [eicar.zip](https://truepolyglot.hackade.org/samples/pdfzip/poc6/eicar.zip) ([scan virustotal.com](https://www.virustotal.com/#/file/2174e17e6b03bb398666c128e6ab0a27d4ad6f7d7922127fe828e07aa94ab79d/detection)) | pdfzip | [polyglot.pdf](https://truepolyglot.hackade.org/samples/pdfzip/poc6/polyglot.pdf) ([scan virustotal.com](https://www.virustotal.com/#/file/f6fef31e3b03164bb3bdf35af0521f9fc0c518a9e0f1aa9f8b60ac936201591a/detection)) | PDF/ZIP polyglot with the Eicar test in Zip - 2.9 Mo |
| [doc.pdf](https://truepolyglot.hackade.org/samples/pdfany/poc7/doc.pdf) | [page.html](https://truepolyglot.hackade.org/samples/pdfany/poc7/page.html) | pdfany | [polyglot.pdf](https://truepolyglot.hackade.org/samples/pdfany/poc7/polyglot.pdf) | PDF/HTML polyglot - 26 Ko |
| [logo.zip](https://truepolyglot.hackade.org/samples/zipany/poc8/logo.zip) | [nc.exe](https://truepolyglot.hackade.org/samples/zipany/poc8/nc.exe) | zipany | [polyglot.zip](https://truepolyglot.hackade.org/samples/zipany/poc8/polyglot.zip) | PDF/PE polyglot - 96 Ko |

## Usage ##

```
usage: truepolyglot format [options] output-file

Generate a polyglot file.

Formats availables:
* pdfzip: Generate a file valid as PDF and ZIP. The format is closest to PDF.
* zippdf: Generate a file valid as ZIP and PDF. The format is closest to ZIP.
* szippdf: Generate a file valid as ZIP and PDF. The format is strictly a ZIP. Archive is modified.
* pdfany: Generate a valid PDF file with payload1 file content as the first object or/and payload2 file content as the last object.
* zipany: Generate a valid ZIP file with payload1 file content at the start of the file or/and payload2 file content between LFH and CD.

positional arguments:       {pdfzip,zippdf,szippdf,pdfany,zipany}
Output polyglot format
output_file           Output polyglot file path

optional arguments:
-h, --help            show this help message and exit
--pdffile PDFFILE     PDF input file
--zipfile ZIPFILE     ZIP input file       
--payload1file PAYLOAD1FILE Payload 1 input file       
--payload2file PAYLOAD2FILE Payload 2 input file 
--acrobat-compatibility Add a byte at the start for Acrobat Reader compatibility with the szippdf format       
--verbose {none,error,info,debug} Verbosity level  (default: info)

TruePolyglot v1.6.2
```

## Code ##

```
git clone https://git.hackade.org/truepolyglot.git/
```

or download [truepolyglot-1.6.2.tar.gz](https://git.hackade.org/truepolyglot.git/snapshot/truepolyglot-1.6.2.tar.gz)

## How to detect a polyglot file ? ##

You can use [binwalk](https://github.com/ReFirmLabs/binwalk) on a file to see if composed of multiple files.

## Contact ##

[truepolyglot@hackade.org](mailto:truepolyglot@hackade.org)

## Credits ##

Copyright © 2018-2019 ben@hackade.org

TruePolyglot is released under [Unlicence](https://unlicense.org/) except for the following libraries:

* [PyPDF2](https://github.com/mstamy2/PyPDF2/blob/master/LICENSE)
* [zipfile.py (cpython)](https://github.com/python/cpython/blob/master/LICENSE)

