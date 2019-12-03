import os
from builtins import enumerate
import argparse
import difflib
import textdistance
import re
import unidecode
import xml.etree.ElementTree as ET
import glob
import ntpath
import sys

fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
headers_name_dic = dict()
headers_type_dic = dict()
Threshold = 0.85
default_header = "DEFAULT_HEADER"


def headers_dic(header):
    with open(header, "r") as h:
        for line in h:
            row_header = line.strip().split("\t")
            if not row_header[2] in headers_name_dic.keys():
                headers_name_dic[row_header[2]] = row_header[1]
            if not row_header[1] in headers_type_dic.keys():
                headers_type_dic[row_header[1]] = row_header[0]

    # return headers_name_dic, headers_type_dic


def trim_name(name):
    unaccent_name = unidecode.unidecode(name)
    for i, ch in enumerate(reversed(unaccent_name)):
        if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
            if i == 0:
                return name
            else:
                return name[:-1 * i]


def preprocessing(line):
    pre_line = line.split(":")[0].split("(")[0].split("/")
    if len(pre_line) > 1:
        return trim_name(pre_line[0]), trim_name(pre_line[1])
    else:
        return trim_name(pre_line[0]), ""


def similarity_diff(temp_line):
    list_similarities = difflib.get_close_matches(temp_line, headers_name_dic.keys(), 1, 0.85)
    if len(list_similarities) > 0:
        return headers_name_dic.get(list_similarities[0]), True
    else:
        return "", False


def similarity(temp_line):
    max_score = -1
    final_header = ""
    for key in headers_name_dic.keys():

        # Levenshtein
        # score = lev.ratio(temp_line,key)
        # score = textdistance.levenshtein(temp_line, key)

        # jaro_winkler
        score = textdistance.jaro_winkler(temp_line, key)

        if score > max_score:
            max_score = score
            final_header = headers_name_dic.get(key)
            Final_key = key

    if max_score > Threshold:
        return final_header, True
    else:
        return "", False


def header_finder(line):
    # and line[0] != '-' \
    if line and ((line[0].isalpha() and line[0].isupper()) or not line[0].isalpha()) \
            and not line.startswith("Nº") and not line.upper().startswith("SIN"):
        temp_line = " ".join(line.split()).upper()
        if temp_line in headers_name_dic.keys():
            return headers_name_dic.get(temp_line), True
        else:
            header_name, isheader = similarity_diff(temp_line)
            if isheader:
                return header_name, isheader
            else:
                return "", False
    else:
        return "", False


def xml(txt_directory, xml_directory, sett):
    if int(sett.split("_")[0]) <= 2:
        header_file = os.path.join(parentDir, "/data/headers_original_bunch_1-2.txt")
    elif int(sett.split("_")[0]) == 3:
        header_file = os.path.join(parentDir, "/data/headers_13.11.2019_bunch_3.txt")
    else:
        header_file = os.path.join(parentDir, "data/headers.txt")

    headers_dic(header_file)
    for text_files in os.listdir(txt_directory):
        print(text_files)
        if text_files.endswith(".txt"):
            current_section = ""
            xml_files = text_files[0:-4]
            xml_file = os.path.join(xml_directory, xml_files + ".xml")
            os.makedirs(xml_directory, exist_ok=True)
            with open(xml_file, "w") as w:
                w.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                w.write("<ehr id=\"" + text_files + "\">\n")
                begin = 0
                with open(os.path.join(txt_directory, text_files), "r") as f:
                    for i, line in enumerate(f):
                        line_size = len(line)
                        pre_line, pos_line = preprocessing(line)
                        if pre_line:
                            pre_line = pre_line.rstrip()


                        header_name, isheader = header_finder(pre_line)
                        if isheader:
                            isheader_2 = False
                            if pos_line and "/" in line and abs(len(pre_line.split()) - len(pos_line.split()) <= 1):
                                _, isheader_2 = header_finder(pos_line)
                            marked = False
                            if current_section:
                                if current_section == header_name:
                                    marked = True
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

                                if begin == 546:
                                    print("TEST")
                                before_lstrip = len(pre_line)
                                pre_line = pre_line.lstrip()
                                afteR_lstrip = len(pre_line)
                                begin += (before_lstrip - afteR_lstrip)
                                line_size -= (before_lstrip - afteR_lstrip)

                                w.write("<Section span_begin=\"" + str(
                                    begin) + "\" span_end=\"" + span_end + "\" id=\"" + header_name + "\" type=\"" +
                                        headers_type_dic.get(
                                    header_name) + "\">\n\t<name><![CDATA[" +
                                        pre_line + "]]></name>\n\t<text><![CDATA[\n")

                        elif i == 0:
                            w.write(
                                "<Section id=\"" + default_header + "\" type=\"" + default_header + "\" >\n\t<name>"
                                + default_header + "</name>\n\t<text><![CDATA[\n")
                            current_section = default_header
                            marked = True
                        else:
                            marked = True
                        if marked and line.strip():
                            w.write(line)
                        begin += line_size
                w.write("\t]]></text>\n</Section>\n")
                w.write("</ehr>")


def ann(xml_dir, ann_dir):
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
            pre_header = ""
            for type_tag in root.findall('Section'):

                for type_child in type_tag.findall('name'):
                    name = type_child.text

                x = str(type_tag.get('id')).strip()
                span_begin = str(type_tag.get('span_begin')).strip()
                span_end = str(type_tag.get('span_end')).strip()
                pure_name_eq = name.split("=", 2)
                pure_name = pure_name_eq[0].split("-!-", 2)

                # if pure_name.startswith(" Ana lít ica d 'urgè ncies"):
                #     print("Checkpoint")

                name = pure_name[0]
                if (x != "DEFAULT_HEADER") and (pre_header != x):
                    f.write("T" + str(counter) + "\t" + x + " " + span_begin + " " + span_end + "\t" + pure_name[
                        0].rstrip() + "\n")
                    counter += 1
                pre_header = x
            f.close()
        except:
            print("ERROR", filename, sys.exc_info())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analysis")
    parser.add_argument('--set', help='Which set is going to compare')
    args = parser.parse_args()
    Set = args.set

    main_root = os.path.join(parentDir, "documents", "TXT")
    for text_files in os.listdir(main_root):
        if not text_files.startswith("."):
            TXT_Directory = os.path.join(main_root, text_files, Set)
            XML_Directory = TXT_Directory.replace("TXT", "XML_SECTION")
            ANN_Directory = XML_Directory.replace("XML_SECTION", "ANN_SECTION")

            xml(TXT_Directory, XML_Directory, Set)
            ann(XML_Directory, ANN_Directory)
