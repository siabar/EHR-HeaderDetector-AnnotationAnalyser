import os
import shutil
import string
from builtins import enumerate
import argparse
import difflib
import re
import unidecode
import xml.etree.ElementTree as ET
import glob
import ntpath
import sys

from utility import *


class header_detector():

    def __init__(self):
        self.abbreviation_headers = []
        self.threshold = 0.85
        self.default_header = "DEFAULT_HEADER"
        self.headers_name_dic = dict()
        self.headers_type_dic = dict()
        self.fileDir = os.path.dirname(os.path.abspath(__file__))
        self.parentDir = os.path.dirname(self.fileDir)

    def headers_dic(self, header):
        """
        :param header: path of header's file
        :return:
            headers_type_dic: A dictionary that contains sections as keys and their categories as values
            header_name_dic : A dictionary that contains categories as keys and their types as values
        """

        with open(header, "r") as h:
            for line in h:
                row_header = line.strip().split("\t")
                if row_header[2].endswith('.'):
                    self.abbreviation_headers.append(unidecode.unidecode(row_header[2]))
                if not row_header[2] in self.headers_name_dic.keys():
                    self.headers_name_dic[row_header[2]] = row_header[1]
                if not row_header[1] in self.headers_type_dic.keys():
                    self.headers_type_dic[row_header[1]] = row_header[0]

    def trim(self, name):
        """
            It is not used
        """
        for i, ch in enumerate(reversed(name)):
            if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
                if i == 0:
                    return name
                else:
                    return name[:-1 * i]

    def trim_name(self, name):
        """
        :param name: input string
        :return:
            remove unalpha chars at the end of the input
        """
        unaccent_name = unidecode.unidecode(name)
        if unaccent_name.upper() in self.abbreviation_headers:
            return name
        for i, ch in enumerate(reversed(unaccent_name)):
            if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
                if i == 0:
                    return name
                else:
                    return name[:-1 * i]

    def preprocessing(self, line):
        """
        Split the given line by following punctuations: ":", "(", "/"

        :param line:
        :return:
            return left part and right part of the splitted line
        """
        pre_line = line.split(":")[0].split("(")[0].split("/")
        if len(pre_line) > 1:
            return self.trim_name(pre_line[0]), self.trim_name(pre_line[1])
        else:
            return self.trim_name(pre_line[0]), ""



    def similarity_diff(self, line):
        """
        :param line: input line
        :return:
            The most similarity defined section with the given line
        """

        list_similarities = difflib.get_close_matches(line, self.headers_name_dic.keys(), 1, 0.85)
        if len(list_similarities) > 0:
            return self.headers_name_dic.get(list_similarities[0]), True
        else:
            return "", False



    def header_finder(self, line):
        '''
        :param line:
        :return Fasle, or True if the given line is a header:
        '''
        # and line[0] != '-' \
        if line and ((line[0].isalpha() and line[0].isupper()) or not line[0].isalpha()) \
                and not line.startswith("Nº") and not line.upper().startswith("SIN"):
            temp_line = " ".join(line.split()).upper()
            if temp_line in self.headers_name_dic.keys():
                return self.headers_name_dic.get(temp_line), True
            else:
                header_name, isheader = self.similarity_diff(temp_line)
                if isheader:
                    return header_name, isheader
                else:
                    return "", False
        else:
            return "", False

    def xml(self, txt_directory, xml_directory, sett):
        """
        :param txt_directory: Directory of text files as input
        :param xml_directory: Directory of xml files as output
        :param sett: Number of bunch
        :return: detect headers of the given text files and save them as a xml files in output directory (xml_directory)
        '''
        """
        shutil.rmtree(xml_directory, ignore_errors=True)
        os.makedirs(xml_directory, exist_ok=True)


        header_file = header_path(sett, self.parentDir)

        self.headers_dic(header_file)
        print("Processing these files:")
        for text_files in os.listdir(txt_directory):
            print('\t', text_files)
            if text_files.endswith(".txt"):
                current_section = ""
                xml_files = text_files[0:-4]
                xml_file = os.path.join(xml_directory, xml_files + ".xml")

                with open(xml_file, "w") as w:
                    w.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                    w.write("<ehr id=\"" + text_files + "\">\n")
                    begin = 0
                    with open(os.path.join(txt_directory, text_files), "r") as f:
                        for i, line in enumerate(f):
                            line_size = len(line)
                            if line.lower().startswith("diag."):
                                check = 0
                            pre_line, pos_line = self.preprocessing(line)
                            if pre_line:
                                pre_line = pre_line.rstrip()

                            header_name, isheader = self.header_finder(pre_line)
                            if isheader:
                                isheader_2 = False
                                if pos_line and "/" in line and abs(len(pre_line.split()) - len(pos_line.split()) <= 1):
                                    _, isheader_2 = self.header_finder(pos_line)
                                marked = False
                                if current_section:
                                    if current_section == header_name:
                                        # marked = True
                                        w.write("\t]]></text>\n</Section>\n")
                                        marked = False

                                    else:
                                        w.write("\t]]></text>\n</Section>\n")
                                        marked = False
                                if not marked:
                                    current_section = header_name

                                    if isheader_2:
                                        x = re.search("^" + pre_line + "\s*/\s*" + pos_line, line)
                                        if x:
                                            pre_line = x.group()

                                        span_end = str(begin + len(pre_line))
                                        marked = False
                                    else:
                                        span_end = str(begin + len(pre_line))

                                    if len(pre_line) < len(line.strip()):
                                        line = line[len(pre_line):]
                                        marked = True

                                    begin_original = begin
                                    pre_line, begin, span_end = self.span_fixer(pre_line, begin, int(span_end))
                                    line_size -= begin - begin_original

                                    w.write("<Section span_begin=\"" + str(
                                        begin) + "\" span_end=\"" + str(
                                        span_end) + "\" id=\"" + header_name + "\" type=\"" +
                                            self.headers_type_dic.get(
                                                header_name) + "\">\n\t<name><![CDATA[" +
                                            pre_line + "]]></name>\n\t<text><![CDATA[\n")

                            elif i == 0:
                                w.write(
                                    "<Section id=\"" + self.default_header + "\" type=\"" + self.default_header + "\" >\n\t<name>"
                                    + self.default_header + "</name>\n\t<text><![CDATA[\n")
                                current_section = self.default_header
                                marked = True
                            else:
                                marked = True
                            if marked and line.strip():
                                w.write(line)
                            begin += line_size
                    w.write("\t]]></text>\n</Section>\n")
                    w.write("</ehr>")

    def span_fixer(self, text, start_span, end_span):
        """
        :param text:  input
        :param start_span: start span of text
        :param end_span:  end span of text
        :return: fix the spans of the given text. for example if strip white space at begin or end of the given input.
        """

        punctuation = string.punctuation.replace(".", "")

        before_rstrip = len(text)
        text = text.rstrip()
        after_rstrip = len(text)
        end_span -= before_rstrip - after_rstrip
        while text[len(text) - 1] in punctuation:
            text = text[:-1]
            removed_space = len(text) - len(text.rstrip())
            text = text.rstrip()
            end_span -= 1 + removed_space
        before_lstrip = len(text)
        text = text.lstrip()
        after_lstrip = len(text)
        start_span += before_lstrip - after_lstrip
        while text[0] in string.punctuation:
            text = text[1:]
            removed_space = len(text) - len(text.lstrip())
            text = text.lstrip()
            start_span += 1 + removed_space

        return text, start_span, end_span

    def ann(self, xml_dir, ann_dir):
        """
        :param xml_dir: Directory of xml files as input
        :param ann_dir: Directory of ann files as output
        :return: read xml files and save headers in the ann file
        """
        shutil.rmtree(ann_dir, ignore_errors=True)
        os.makedirs(os.path.join(ann_dir), exist_ok=True)
        files = glob.glob(xml_dir + "/*.xml")
        brat_dir = ann_dir
        for file in files:
            filename = ntpath.basename(file)

            try:
                root = ET.parse(file).getroot()
                name = ""
                filename_ann = filename.replace("xml", "ann")
                xx = os.path.join(brat_dir, filename_ann)
                f = open(xx, "w")
                counter = 1
                for type_tag in root.findall('Section'):

                    for type_child in type_tag.findall('name'):
                        name = type_child.text

                    x = str(type_tag.get('id')).strip()
                    span_begin = str(type_tag.get('span_begin')).strip()
                    span_end = str(type_tag.get('span_end')).strip()
                    pure_name_eq = name.split("=", 2)
                    pure_name = pure_name_eq[0].split("-!-", 2)


                    name = pure_name[0]
                    if (x != "DEFAULT_HEADER"):
                        f.write("T" + str(counter) + "\t" + x + " " + span_begin + " " + span_end + "\t" + pure_name[
                            0].rstrip() + "\n")
                        counter += 1
                f.close()
            except:
                print("ERROR", filename, sys.exc_info())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="analysis")
    parser.add_argument('--set', help='Which bunch is going to process')
    args = parser.parse_args()
    Set = args.set

    detect = header_detector()
    main_root = os.path.join(detect.parentDir, "documents", "TXT")
    for text_files in os.listdir(main_root):
        if not text_files.startswith("."):
            TXT_Directory = os.path.join(main_root, text_files, Set)
            XML_Directory = TXT_Directory.replace("TXT", "XML_SECTION")
            ANN_Directory = XML_Directory.replace("XML_SECTION", "ANN_SECTION")

            detect.xml(TXT_Directory, XML_Directory, Set)
            detect.ann(XML_Directory, ANN_Directory)
