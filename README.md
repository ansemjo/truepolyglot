Truepolyglot is polyglot file generator project. This means that the
generated file is composed of several file formats. The same file can be
opened as a ZIP file and as a PDF file for example. The idea of this
project comes from work of [Ange Albertini](https://github.com/corkami),
[International Journal of Proof-of-Concept or Get The Fuck
Out](https://www.alchemistowl.org/pocorgtfo/pocorgtfo07.pdf) and [Julia
Wolf](https://www.troopers.de/wp-content/uploads/2011/04/TR11_Wolf_OMG_PDF.pdf)
that explain how we can build a polyglot file.\
Polyglot file can be fastidious to build, even more if you want to
respect correctly file format. That's why I decided to build a tool to
generate them.\
My main motivation was the technical challenge.

## Features and versions ##

  Description                                                                                               Version
  --------------------------------------------------------------------------------------------------------- -------------
  Build a polyglot file valid as PDF and ZIP format and that can be opened with 7Zip and Windows Explorer   POC
  Add a stream object in PDF part                                                                           POC
  Polyglot file checked without warning with [pdftocairo](https://poppler.freedesktop.org/)                 >= 1.0
  Polyglot file checked without warning with [caradoc](https://github.com/ANSSI-FR/caradoc)                 >= 1.0
  Rebuild PDF Xref Table                                                                                    >= 1.0
  Stream object with correct length header value                                                            >= 1.0
  Format "zippdf", file without offset after Zip data                                                       >= 1.1
  Polyglot file keep original PDF version                                                                   >= 1.1.1
  Add "szippdf" format without offset before and after Zip data                                             >= 1.2
  Fix /Length stream object value and PDF offset for szippdf format                                         >= 1.2.1
  PDF object numbers reorder after insertion                                                                >= 1.3

## Polyglot file compatibility ##

  Software           Formats                   status
  ------------------ ------------------------- -----------------------------
  Acrobat Reader     pdfzip, zippdf            OK
  Acrobat Reader     szippdf                   __KO__
  Sumatra PDF        pdfzip, zippdf, szippdf   OK
  Edge               pdfzip, zippdf, szippdf   OK
  Firefox            pdfzip, zippdf, szippdf   OK
  7zip               pdfzip, zippdf            __OK with warning__
  7zip               szippdf                   OK
  Explorer Windows   pdfzip, zippdf, szippdf   OK
  Info-ZIP (unzip)   pdfzip, zippdf, szippdf   OK
  Evince             pdfzip, zippdf, szippdf   OK
  pdftocairo -pdf    pdfzip, zippdf, szippdf   OK
  caradoc stats      pdfzip                    OK
  java               szippdf                   OK

## Examples ##

  PDF input file                                             Zip input file                                                                                                                                                                      Format    Polyglot                                                                                                                                                                                  Comment
  ---------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- --------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- --------------------------------------------------
  [doc.pdf](/samples/pdfzip/poc1/doc.pdf)                    [archive.zip](/samples/pdfzip/poc1/archive.zip)                                                                                                                                     pdfzip    [polyglot.pdf](/samples/pdfzip/poc1/polyglot.pdf)                                                                                                                                         PDF/ZIP polyglot - 122 Ko
  [orwell\_1984.pdf](/samples/pdfzip/poc2/orwell_1984.pdf)   [file-FILE5\_32.zip](/samples/pdfzip/poc2/file-FILE5_32.zip)                                                                                                                        pdfzip    [polyglot.pdf](/samples/pdfzip/poc2/polyglot.pdf)                                                                                                                                         PDF/ZIP polyglot - 1.3 Mo
  [x86asm.pdf](/samples/pdfzip/poc3/x86asm.pdf)              [fasmw17304.zip](/samples/pdfzip/poc3/fasmw17304.zip)                                                                                                                               pdfzip    [polyglot.pdf](/samples/pdfzip/poc3/polyglot.pdf)                                                                                                                                         PDF/ZIP polyglot - 1.8 Mo
  [doc.pdf](/samples/zippdf/poc4/doc.pdf)                    [archive.zip](/samples/zippdf/poc4/archive.zip)                                                                                                                                     zippdf    [polyglot.pdf](/samples/zippdf/poc4/polyglot.pdf)                                                                                                                                         PDF/ZIP polyglot - 112 Ko
  [electronics.pdf](/samples/szippdf/poc5/electronics.pdf)   [hello\_world.jar](/samples/szippdf/poc5/hello_world.jar)                                                                                                                           szippdf   [polyglot.pdf](/samples/szippdf/poc5/polyglot.pdf)                                                                                                                                        PDF/JAR polyglot - 778 Ko
  [hexinator.pdf](/samples/pdfzip/poc6/hexinator.pdf)        [eicar.zip](/samples/pdfzip/poc6/eicar.zip) ([scan virustotal.com](https://www.virustotal.com/#/file/2174e17e6b03bb398666c128e6ab0a27d4ad6f7d7922127fe828e07aa94ab79d/detection))   pdfzip    [polyglot.pdf](/samples/pdfzip/poc6/polyglot.pdf) ([scan virustotal.com](https://www.virustotal.com/#/file/f6fef31e3b03164bb3bdf35af0521f9fc0c518a9e0f1aa9f8b60ac936201591a/detection))   PDF/ZIP polyglot with Eicar test in Zip - 2.9 Mo

## Usage ##

    usage: truepolyglot format [options] output-file

    Generate a polyglot file.

    Formats availables:
    * pdfzip: Generate a file valid as PDF and ZIP. The format is closest to PDF.
    * zippdf: Generate a file valid as ZIP and PDF. The format is closest to ZIP.
    * szippdf: Generate a file valid as ZIP and PDF. The format is strictly a ZIP. Archive is modified.

    positional arguments:
      {pdfzip,zippdf,szippdf}
                            Output polyglot format
      output_file           Output polyglot file path

    optional arguments:
      -h, --help            show this help message and exit
      --pdffile PDFFILE     PDF input file
      --zipfile ZIPFILE     ZIP input file
      --verbose {none,error,info,debug}
                            Verbosity level  (default: info)

    TruePolyglot v1.3

## Code ##

    git clone https://git.hackade.org/truepolyglot.git/
   Download [truepolyglot-1.3.tar.gz](https://git.hackade.org/truepolyglot.git/snapshot/truepolyglot-1.3.tar.gz)

## Contact ##

[truepolyglot@hackade.org](mailtp:truepolyglot@hackade.org)
