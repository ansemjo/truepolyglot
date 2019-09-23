# -*- coding: utf-8 -*-

"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

import logging
import re
import tempfile
from .PyPDF2 import PdfFileWriter, PdfFileReader


class Pdf:

    def __init__(self, filename):
        self.filename = filename
        self.buffer = bytearray()
        self.objects = []  # [(7,0,b"data"), (8,0,b"data2"), ..]
        self.trailer = {}  # {Root: (7, 0), Info: (5, 0)}
        self.translation_table = {}  # {(6,0):7, (5,0): 8}, ..]
        self.original_xref_offset = 0
        self.original_first_obj_offset = 0
        self.file_offset = 0

        self.clean_and_read_pdf()
        self.check_pdf_header()
        self.parse_xref_offset()
        self.parse_xref_table()
        self.parse_objects()
        self.parse_trailer()

    def clean_and_read_pdf(self):
        f_input = open(self.filename, "rb")
        pdf_header = f_input.read(8)
        f_input.seek(0)
        filename_output = tempfile.mktemp()
        logging.info("Use " + filename_output + " for normalisation output")
        f_ouput = open(filename_output, "wb")
        writer = PdfFileWriter()
        reader = PdfFileReader(f_input)
        info = reader.getDocumentInfo()
        logging.info("Document info:", info)
        writer.addMetadata(info)
        if info.producer is None:
            writer.addMetadata({u'/Producer': u'TruePolyglot'})
        elif info.creator is None:
            writer.addMetadata({u'/Creator': u'TruePolyglot'})
        writer.cloneReaderDocumentRoot(reader)
        writer.setHeader(pdf_header)
        writer.write(f_ouput)
        f_input.close()
        f_ouput.close()
        f_norm = open(filename_output, "rb")
        self.buffer = bytearray(f_norm.read())
        self.size = len(self.buffer)
        f_norm.close()

    def check_pdf_header(self):
        if self.buffer[0:5] == b"%PDF-":
            pdf_version = self.buffer[5:8].decode("utf-8")
            logging.info("PDF Header found: " + pdf_version)
        else:
            raise Exception("PDF Header not found")

    def parse_xref_offset(self):
        r = re.compile(b'startxref\n([0-9]+)')
        m = r.search(self.buffer)
        if m is None:
            raise Exception('Unable to find xref offset')
        self.original_xref_offset = int(m.group(1))
        logging.info("Xref offset found at: " + hex(self.original_xref_offset))

    def parse_xref_table(self):
        xref_table = []
        r = re.compile(b'xref\n([0-9]+) ([0-9]+)')
        offset = self.original_xref_offset
        s = r.search(self.buffer[offset:offset + 32])
        nb_xtable_object = int(s.group(2))
        logging.info("Nb objects in Xref table: " + str(nb_xtable_object))
        xref_header_size = s.end()
        r = re.compile(b'([0-9]+) ([0-9]+) ([f|n])')
        x = 0
        for i in range(nb_xtable_object):
            s = r.search(
                self.buffer[self.original_xref_offset + xref_header_size + x:])
            if s is not None:
                x = x + s.end()
                xref_table.append((int(s.group(1)),
                                   int(s.group(2)),
                                   s.group(3)))
        logging.debug("Xref table:")
        for i in xref_table:
            logging.debug(str(i[0]) + " " +
                          str(i[1]) + " " +
                          i[2].decode("utf-8"))

    def parse_objects(self):
        r_begin = re.compile(b'([0-9]+) ([0-9]+) obj\n')
        r_end = re.compile(b'\nendobj\n')

        offset_buffer = 0
        obj = ()
        while offset_buffer < self.size:
            m_begin = r_begin.match(
                self.buffer[offset_buffer:offset_buffer + 32])
            obj_nb_index = 0
            obj_nb_offset = 0
            obj_offset_start = 0
            obj_offset_end = 0
            if m_begin is not None:
                if self.original_first_obj_offset == 0:
                    self.original_first_obj_offset = (offset_buffer +
                                                      m_begin.start())
                obj_nb_index = int(m_begin.group(1))
                obj_nb_offset = int(m_begin.group(2))
                obj_data_start = m_begin.end()
                obj_offset_start = offset_buffer + m_begin.start()
                while offset_buffer < self.size:
                    m_end = r_end.match(
                        self.buffer[offset_buffer:offset_buffer + 8])
                    if m_end is not None:
                        obj_offset_end = offset_buffer + m_end.end() - 2
                        break
                    else:
                        offset_buffer = offset_buffer + 1
            else:
                offset_buffer = offset_buffer + 1

            if (obj_offset_start != 0 and
                    obj_offset_end != 0):
                a = obj_offset_start + obj_data_start
                b = obj_offset_end - 6
                obj = (obj_nb_index, obj_nb_offset,
                       self.buffer[a:b])
                logging.debug("Objects: (" + str(obj_nb_index) +
                              ", " + str(obj_nb_offset) +
                              ", " + hex(obj_offset_start) +
                              ", " + hex(obj_offset_end))
                self.objects.append(obj)

    def parse_trailer(self):
        r_begin = re.compile(b'trailer\n')
        s_begin = r_begin.search(self.buffer[self.original_xref_offset:])
        start = self.original_xref_offset + s_begin.start()
        logging.info("Trailer found at:" + hex(start))

        r_root = re.compile(b'/Root ([0-9]+) ([0-9]+) R')
        s_root = r_root.search(self.buffer[self.original_xref_offset:])
        if s_root is None:
            raise Exception('Root not found')
        else:
            self.trailer["Root"] = (int(s_root.group(1)), int(s_root.group(2)))

        r_info = re.compile(b'/Info ([0-9]+) ([0-9]+) R')
        s_info = r_info.search(self.buffer[self.original_xref_offset:])
        if s_info is not None:
            self.trailer["Info"] = (int(s_info.group(1)), int(s_info.group(2)))

    def get_file_header(self):
        return self.buffer[:self.original_first_obj_offset]

    def get_xref_table(self):
        offset_xref = 0
        buf = (b'xref\n' +
               str(offset_xref).encode('utf-8') + b' ' +
               str(len(self.objects) + 1).encode('utf-8') + b'\n' +
               str(0).zfill(10).encode('utf-8') + b' ' +
               str(65535).zfill(5).encode('utf-8') + b' f \n')

        for i in range(len(self.objects)):
            obj_start = self.get_object_offset(i)
            logging.info("Obj %d at %d" % (self.objects[i][0], obj_start))
            buf = (buf +
                   (str(obj_start).zfill(10)).encode('utf-8') + b' ' +
                   str(0).zfill(5).encode('utf-8') + b' ' +
                   b'n' + b' \n')
        return buf

    def get_trailer(self):
        trailer_data = (b"trailer\n<<\n/Size " +
                        str(len(self.objects) + 1).encode("utf-8") +
                        b"\n/Root " +
                        str(self.trailer["Root"][0]).encode("utf-8") +
                        b" " +
                        str(self.trailer["Root"][1]).encode("utf-8") +
                        b" R\n")
        if "Info" in self.trailer:
            trailer_data = (trailer_data +
                            b"/Info " +
                            str(self.trailer["Info"][0]).encode("utf-8") +
                            b" " +
                            str(self.trailer["Info"][1]).encode("utf-8") +
                            b" R\n")
        trailer_data = trailer_data + b">>"
        return trailer_data

    def get_xref_offset(self):
        return self.get_end_of_last_object() + 1

    def get_eof(self):
        s = (b'startxref\n' +
             str(self.get_xref_offset()).encode("utf-8") +
             b'\n%%EOF\n')
        return s

    def build_object(self, obj):
        buf = (str(obj[0]).encode("utf-8") +
               b' ' +
               str(obj[1]).encode("utf-8") +
               b' obj\n' +
               obj[2] +
               b'\nendobj')
        return buf

    def get_build_buffer(self):
        b_buffer = bytearray()
        b_buffer = b_buffer + self.get_file_header()
        for obj in self.objects:
            b_buffer = b_buffer + self.build_object(obj) + b'\n'
        b_buffer = b_buffer + self.get_xref_table()
        b_buffer = b_buffer + self.get_trailer() + b'\n'
        b_buffer = b_buffer + self.get_eof()
        return b_buffer

    def get_obj(self, nb):
        for obj in self.objects:
            if obj[0] == nb:
                return obj

    def get_end_of_last_object(self):
        offset = self.get_last_object_offset()
        offset = offset + len(self.build_object(self.objects[-1]))
        return offset

    def generate_stream_obj_data(self, data):
        buf = (b'<<\n/Filter /FlateDecode\n/Length ' +
               str(len(data)).encode("utf-8") +
               b'\n>>\nstream\n' +
               data +
               b'\nendstream')
        return buf

    def insert_new_obj_stream_at(self, position, stream_data):
        '''
        Return offset of stream data
        '''
        logging.info("Insert obj at %d" % position)
        obj_nb = position
        obj_off = 0
        data = self.generate_stream_obj_data(stream_data)
        obj = (obj_nb, obj_off, data)

        obj_data = self.build_object(obj)
        full_obj_size = len(obj_data)
        logging.info("New object full size is: " + str(full_obj_size))

        obj = (obj_nb, obj_off, data)
        self.objects.insert(position, obj)

        self.reorder_objects()
        self.fix_trailer_ref()

    def get_first_stream_offset(self):
        offset = self.file_offset + len(self.get_file_header())
        r = re.compile(b'stream\n')
        m = r.search(self.objects[0][2])
        offset = offset + len(b"1 0 obj\n") + m.end()
        return offset

    def get_last_stream_offset(self):
        offset = self.file_offset + self.get_last_object_offset()
        r = re.compile(b'stream\n')
        m = r.search(self.build_object(self.objects[-1]))
        return offset + m.end()

    def get_object_offset(self, index):
        offset = self.file_offset + len(self.get_file_header())
        for obj in self.objects[:index]:
            offset = offset + len(self.build_object(obj)) + 1
        return offset

    def get_last_object_offset(self):
        offset = self.get_object_offset(len(self.objects) - 1)
        return offset

    def insert_new_obj_stream_at_start(self, data):
        return self.insert_new_obj_stream_at(0, data)

    def insert_new_obj_stream_at_end(self, data):
        return self.insert_new_obj_stream_at(len(self.objects) + 1,
                                             data)

    def generate_translation_table(self):
        for i in range(len(self.objects)):
            self.translation_table[(self.objects[i][0],
                                    self.objects[i][1])] = i + 1
        logging.info(self.translation_table)

    def replace_ref(self, ibuffer):
        '''
        Exemple:
        in: AZERTY 6 0 R -- BGT 88 0 R HYT
        out: AZERTY 77 0 R -- BGT 9 0 R HYT
        '''
        index = 0
        obuffer = bytearray()
        while True:
            r = re.compile(b'([0-9]+) ([0-9]+) R')
            s = r.search(ibuffer[index:])
            if s is None:
                obuffer = obuffer + ibuffer[index:]
                break
            o_old = int(s.group(1))
            p_old = int(s.group(2))
            o_new = self.translation_table[(o_old, p_old)]
            p_new = p_old

            newref = (str(o_new).encode("utf-8") +
                      b" " +
                      str(p_new).encode("utf-8") +
                      b" R")

            nbuffer = ibuffer[index:index + s.start()] + newref
            obuffer = obuffer + nbuffer
            index = index + s.end()
        return obuffer

    def reorder_objects(self):
        self.generate_translation_table()
        offset_obj = len(self.get_file_header())
        for i in range(len(self.objects)):
            buf = self.objects[i][2]
            new_buf = self.replace_ref(buf)
            obj_nb = self.objects[i][0]
            new_obj_nb = self.translation_table[(obj_nb, 0)]
            new_obj_start = offset_obj
            size_obj = len(self.build_object((new_obj_nb,
                                              0,
                                              new_buf)))
            new_obj_end = new_obj_start + size_obj

            offset_obj = new_obj_end + 1
            obj = (new_obj_nb,
                   0,
                   new_buf)
            self.objects[i] = obj

    def fix_trailer_ref(self):
        new_obj_nb = self.translation_table[self.trailer["Root"]]
        self.trailer["Root"] = (new_obj_nb, 0)

        if "Info" in self.trailer:
            new_obj_nb = self.translation_table[self.trailer["Info"]]
            self.trailer["Info"] = (new_obj_nb, 0)
