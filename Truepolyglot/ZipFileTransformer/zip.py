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

import logging as Logging
import re

logging = Logging.getLogger("zip")

class Zip:

    def __init__(self, filename):
        self.filename = filename
        self.buffer = bytearray()
        self.size = 0
        self.end_central_dir = 0
        self.first_local_file_header = 0
        self.offset_local_file = []
        self.offset_central_directory = []
        self.end_of_data = 0
        self.end_of_first_local_file_header = 0

        self.read()
        self.check_header()
        self.call_all_parsers()
        self.check_central_directory()
        self.parse_central_directories()
        self.parse_local_file_headers()

    def call_all_parsers(self):
        self.parse_offset_end_central_dir()
        self.parse_nb_of_disk()
        self.parse_start_disk()
        self.parse_nb_of_central_dir()
        self.parse_nb_total_of_central_dir()
        self.parse_size_central_dir()
        self.parse_central_dir_file_header()
        self.parse_comment_length()

    def read(self):
        with open(self.filename, 'rb') as fd:
            self.buffer = bytearray(fd.read())
        self.size = len(self.buffer)
        logging.info("read " + str(self.size) + " bytes from Zip file")

    def check_header(self):
        if self.buffer[0:4] != b"PK\x03\x04":
            raise Exception("Zip header not found")

    def parse_offset_end_central_dir(self):
        r = re.compile(b'\x06\x05KP')
        s = r.search(self.buffer[::-1])
        if s is None:
            raise Exception("Unable to find end of central directory")
        self.end_central_dir = self.size - s.end()
        logging.info("Offset end of central directory: " +
                     hex(self.end_central_dir))

    def parse_nb_of_disk(self):
        self.nb_of_disk = int.from_bytes(
            self.buffer[self.end_central_dir + 4:self.end_central_dir + 6],
            "little")
        logging.debug("Nb of disk: " + str(self.nb_of_disk))

    def parse_start_disk(self):
        self.start_disk = int.from_bytes(
            self.buffer[self.end_central_dir + 6:self.end_central_dir + 8],
            "little")
        logging.debug("Start disk: " + str(self.start_disk))

    def parse_nb_of_central_dir(self):
        self.nb_of_central_dir = int.from_bytes(
            self.buffer[self.end_central_dir + 8:self.end_central_dir + 10],
            "little")
        logging.info("Nb of central directory record: " +
                     str(self.nb_of_central_dir))

    def parse_nb_total_of_central_dir(self):
        self.nb_total_of_central_dir = int.from_bytes(
            self.buffer[self.end_central_dir + 10:self.end_central_dir + 12],
            "little")
        logging.info("Nb of total central directory record: " +
                     str(self.nb_total_of_central_dir))

    def parse_size_central_dir(self):
        self.size_central_dir = int.from_bytes(
            self.buffer[self.end_central_dir + 12:self.end_central_dir + 14],
            "little")
        logging.info("Size of central directory: " +
                     str(self.size_central_dir))

    def parse_central_dir_file_header(self):
        self.central_dir_file_header = int.from_bytes(
            self.buffer[self.end_central_dir + 16:self.end_central_dir + 20],
            "little")
        logging.info("Central directory file header: " +
                     hex(self.central_dir_file_header))

    def parse_comment_length(self):
        self.comment_length = int.from_bytes(
            self.buffer[self.end_central_dir + 20:self.end_central_dir + 22],
            "little")
        logging.info("Comment length: " +
                     str(self.comment_length))

    def check_central_directory(self):
        offset = self.central_dir_file_header
        if (self.buffer[offset:offset + 4] !=
                b'PK\x01\x02'):
            raise Exception("Unable to find central directory")
        logging.info("Found central directory")

    def parse_central_directories(self):
        if (self.buffer[self.central_dir_file_header:
                        self.central_dir_file_header + 4] !=
                b'PK\x01\x02'):
            raise Exception("Unable to find first central directory")
        logging.info("Found first central directory")

        i = 0
        size = 0
        offset = self.central_dir_file_header

        while (self.buffer[size + offset:
                           size + offset + 4] ==
                b'PK\x01\x02'):

            logging.debug("Parse central directory n°" + str(i))
            logging.debug("Offset: " + hex(offset + size))
            self.offset_central_directory.append(offset + size)
            filename_length = int.from_bytes(
                self.buffer[size + offset + 28:size + offset + 30],
                "little")
            logging.debug("filename length:" + str(filename_length))
            extra_field_length = int.from_bytes(
                self.buffer[size + offset + 30:size + offset + 32],
                "little")
            logging.debug("extra field length:" + str(extra_field_length))
            comment_length = int.from_bytes(
                self.buffer[size + offset + 32:size + offset + 34],
                "little")
            logging.debug("comment length:" + str(comment_length))
            local_file_header = int.from_bytes(
                self.buffer[size + offset + 42:size + offset + 46],
                "little")
            if i == 0:
                self.first_local_file_header = local_file_header
            logging.debug("local file header:" + hex(local_file_header))

            i = i + 1
            size = (size + filename_length +
                    extra_field_length + comment_length + 46)

            logging.debug("parse header at:" + hex(offset + size))

    def parse_local_file_headers(self):
        size = 0
        offset = self.first_local_file_header
        for i in range(self.nb_of_central_dir):
            logging.debug("Parse local file n°" + str(i))
            compressed_data_lenght = int.from_bytes(
                self.buffer[size + offset + 18:size + offset + 22],
                "little")
            logging.debug("compressed data length:" +
                         str(compressed_data_lenght))
            filename_length = int.from_bytes(
                self.buffer[size + offset + 26:size + offset + 28],
                "little")
            logging.debug("filename length:" + str(filename_length))
            extra_field_length = int.from_bytes(
                self.buffer[size + offset + 28:size + offset + 30],
                "little")
            logging.debug("extra field length:" + str(extra_field_length))
            local_file_size = (compressed_data_lenght +
                               filename_length + extra_field_length + 30)
            logging.debug("local file length:" + hex(local_file_size))
            size = size + local_file_size
            logging.debug("parse header at:" + hex(offset + size))
            self.offset_local_file.append(offset + size)
            self.end_of_data = offset + size
            if i == 0:
                self.end_of_first_local_file_header = self.end_of_data

    def add_data_to_file(self, data_before_local, data_after_local,
                         write_buffer=False):
        logging.info("Add data before local lenght:" +
                     str(len(data_before_local)))
        new_buffer = self.buffer
        for i in self.offset_central_directory:
            logging.debug("parse central directory at: " + hex(i))
            local_file_header = int.from_bytes(
                self.buffer[i + 42:i + 46],
                "little")
            logging.debug("old local file header: " + hex(local_file_header))
            local_file_header = local_file_header + len(data_before_local)
            logging.debug("new local file header: " + hex(local_file_header))
            bytes_local_file_header = local_file_header.to_bytes(4, "little")
            logging.debug("change value at:" + hex(i + 42))
            new_buffer[i + 42:i + 46] = bytes_local_file_header

        logging.info("old central directory header: " +
                     hex(self.central_dir_file_header))
        new_central_dir_file_header = (self.central_dir_file_header +
                                       len(data_after_local) +
                                       len(data_before_local))
        logging.info("new central directory header: " +
                     hex(new_central_dir_file_header))
        bytes_offset = new_central_dir_file_header.to_bytes(4, "little")
        new_buffer[self.end_central_dir + 16:
                   self.end_central_dir + 20] = bytes_offset
        self.buffer = new_buffer

        if write_buffer:
            new_buffer = (data_before_local +
                          new_buffer[:self.end_of_data] +
                          data_after_local +
                          new_buffer[self.central_dir_file_header:])
            self.buffer = new_buffer

    def get_local_file_data(self):
        return self.buffer[:self.end_of_data]

    def get_data_after_central_directory(self):
        return self.buffer[self.central_dir_file_header:]

    def get_first_part_length(self):
        return len(self.get_local_file_data())

    def get_second_part_length(self):
        return len(self.get_data_after_central_directory())
