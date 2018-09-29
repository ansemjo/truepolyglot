# -*- coding: utf-8 -*-

from .polyglotpdfzip import PolyglotPdfZip
import logging
import tempfile
from ZipFileTransformer import ZipFile
from ZipFileTransformer import Zip
from PdfFileTransformer import Pdf

'''
    |-----------------------------------|  -
    |--------- ZIP Data[0] = -----------|  |
    |- PDF Header + PDF Obj[0] Header --|  |
    |-----------------------------------|  | K2
    |------- PDF Obj[0] stream =  ------|  |
    |--------- ZIP Data LF [1:] --------|  |
    |-----------------------------------|  -
    |------ Original PDF Ojbects -------|  |
    |-----------------------------------|  |
    |------------ Xref Table -----------|  |
    |-----------------------------------|  | J2
    |------------- Trailer -------------|  |
    |-----------------------------------|  -
    |---------- End Zip Data -----------|
    |-----------------------------------|
'''


class PolyglotSZipPdf(PolyglotPdfZip):

    def __init__(self, Pdf, Zip, acrobat_compatibility):
        super().__init__(Pdf, Zip)
        self.acrobat_compatibility = acrobat_compatibility

    def get_rebuild_zip_first_part_size(self):

        zo_path = tempfile.mkstemp()[1]
        logging.info("use tmp file zip: " + zo_path)
        zo = ZipFile(zo_path, 'a')
        zi = ZipFile(self.zip.filename, 'r')
        for zipinfo in zi.infolist():
            zo.writestr(zipinfo, zi.read(zipinfo))
        zi.close()
        zo.close()

        rebuild_zip = Zip(zo_path)

        p = rebuild_zip.end_of_data
        k2_stream = rebuild_zip.buffer[:p]

        size_k2_stream = len(k2_stream)

        return size_k2_stream

    def get_pdf_header(self):
        return self.pdf.get_file_header()

    def generate_zip_with_pdf_part(self, filename, pdf_data):

        zo = ZipFile(filename, 'a')
        zi = ZipFile(self.zip.filename, 'r')
        zo.writestr(' ', pdf_data, 0)
        for zipinfo in zi.infolist():
            zo.writestr(zipinfo, zi.read(zipinfo))
        zi.close()
        zo.close()

    def get_rebuild_pdf(self, zo_path, offset):
        '''
            Generate polyglot with final zip.
        '''
        new_zip = Zip(zo_path)
        new_pdf = Pdf(self.pdf.filename)

        p1 = new_zip.end_of_first_local_file_header
        p2 = new_zip.end_of_data
        k2_stream = new_zip.buffer[p1:p2]

        size_k2_stream = len(k2_stream)
        new_pdf.insert_new_obj_stream_at_start(k2_stream)
        k2_stream_offset = new_pdf.get_first_stream_offset()

        new_pdf.file_offset = offset
        if self.acrobat_compatibility:
            new_pdf.file_offset = new_pdf.file_offset + 1
        pdf_buffer = new_pdf.get_build_buffer()
        j2 = pdf_buffer[k2_stream_offset + size_k2_stream:]

        if self.acrobat_compatibility:
            new_zip.add_data_to_file(b'\x00', j2, True)
        else:
            new_zip.add_data_to_file(b'', j2, True)

        return new_zip.buffer

    def get_pdf_offset(self, zipfile):

        f = open(zipfile, "rb")
        data = f.read()
        return data.find(b"%PDF")

    def generate(self):

        zip_stream_size = self.get_rebuild_zip_first_part_size()
        pdf_header = self.get_pdf_header()
        pdf_header = (pdf_header +
                      b'1 0 obj\n<<\n/Filter /FlateDecode\n/Length ' +
                      str(zip_stream_size).encode("utf-8") +
                      b'\n>>\nstream\n')

        filename = tempfile.mkstemp()[1]
        logging.info("use tmp file for new zip: " + filename)
        self.generate_zip_with_pdf_part(filename, pdf_header)

        pdf_offset = self.get_pdf_offset(filename)

        self.buffer = self.get_rebuild_pdf(filename, pdf_offset)
