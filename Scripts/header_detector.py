import os
from builtins import enumerate
import argparse
import difflib
import Levenshtein as lev
import textdistance
import re
import unidecode

fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
headers_name_dic = dict()
headers_type_dic = dict()
Threshold = 0.85
default_header = "DEFAULT_HEADER"


def Headers_dic(HEADER):
    with open(HEADER, "r") as h:
        for line in h:
            row_header = line.strip().split("\t")
            if not row_header[2] in headers_name_dic.keys():
                headers_name_dic[row_header[2]] = row_header[1]
            else:
                print(line)

            if not row_header[1] in headers_type_dic.keys():
                headers_type_dic[row_header[1]] = row_header[0]

    return headers_name_dic, headers_type_dic


def trim_name(name):
    unaccent_name=unidecode.unidecode(name)
    for i, ch in enumerate(reversed(unaccent_name)):
        if ((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')):
            if i ==0:
                return name
            else:
                return name[:-1*i]

def preprocessing(line):
    pre_line =  line.split(":")[0].split("(")[0].split("/")
    if len(pre_line)>1:
        return trim_name(pre_line[0]), trim_name(pre_line[1])
    else:
        return trim_name(pre_line[0]), ""

def similarity_diff(temp_line):
    list_similarities = difflib.get_close_matches(temp_line, headers_name_dic.keys(),1,0.85)
    if len(list_similarities) >0:
        return headers_name_dic.get(list_similarities[0]), True
    else:
        return "", False


def similarity(temp_line):
    Max_Score = -1
    Final_Header = ""
    for key in headers_name_dic.keys():

        #Levenshtein
        # score = lev.ratio(temp_line,key)
        # score = textdistance.levenshtein(temp_line, key)


        # jaro_winkler
        score = textdistance.jaro_winkler(temp_line, key)

        if score > Max_Score:
            Max_Score = score
            Final_Header = headers_name_dic.get(key)
            Final_key = key

    if Max_Score > Threshold:
        return Final_Header, True
    else:
        return "", False

def header(line):
    if line and ((line[0].isalpha() and line[0].isupper()) or not line[0].isalpha()) and line[0] != '-' and not line.startswith("Nº") and not line.upper().startswith("SIN"):
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


def init(Corpus="Aquas"):

    TXT_Directory = os.path.join(parentDir, "documents", "TXT-" + Corpus)
    # TXT_Directory = os.path.join(parentDir, "documents", "TXT")

    XML_Directory = os.path.join(parentDir, "documents", "XML-Test-" + Corpus)
    HEADER = os.path.join(parentDir, "data/headers.txt")


    headers_name_dic, headers_type_dic = Headers_dic(HEADER)

    for text_files in os.listdir(TXT_Directory):
        file_name = text_files.split(".", 1)
        marked = True
        stri = ""
        if text_files.endswith(".txt"):
            counter = 1
            current_section = ""
            XML_FILE = os.path.join(XML_Directory,text_files + ".xml")
            with open(XML_FILE, "w") as w:
                w.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                w.write("<ehr id=\"" + text_files + "\">\n")
                begin = 0
                with open(os.path.join(TXT_Directory, text_files), "r") as f:
                    for i, line in enumerate(f):
                        line_size = len(line)
                        pre_line, pos_line = preprocessing(line)
                        if pre_line:
                            pre_line = pre_line.strip()

                        header_name, isheader = header(pre_line)
                        if (isheader):
                            isheader_2 = False
                            if pos_line and "/" in line and abs(len(pre_line.split())-len(pos_line.split()) <=1):
                                _, isheader_2 = header(pos_line)
                            marked = False
                            if current_section:
                                if current_section==header_name:
                                    marked = True
                                else:
                                    w.write("\t]]></text>\n</Section>\n")
                                    marked = False
                            if not marked:
                                current_section = header_name

                                if isheader_2 :
                                    x = re.search("^"+ pre_line+"\s*/\s*"+ pos_line, line)
                                    if x:
                                        pre_line = x.group()

                                    span_end = str(begin+len(pre_line))
                                    marked = False
                                else:
                                    span_end = str(begin + len(pre_line))

                                if len(pre_line) < len(line.strip()):
                                    line = line[len(pre_line):]
                                    marked = True

                                w.write("<Section span_begin=\""+str(begin)+"\" span_end=\""  +span_end + "\" id=\""  + header_name+"\" type=\"" + headers_type_dic.get(header_name) + "\">\n\t<name><![CDATA[" + pre_line +"]]></name>\n\t<text><![CDATA[\n")

                        elif(i==0):
                            w.write("<Section id=\"" + default_header + "\" type=\""+ default_header+"\" >\n\t<name>"+default_header+"</name>\n\t<text><![CDATA[\n")
                            current_section = default_header
                            marked = True
                        else:
                            marked = True
                        if (marked and line.strip()):
                            w.write(line)
                        begin += line_size
                w.write("\t]]></text>\n</Section>\n")
                w.write("</ehr>")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analysis")

    parser.add_argument('-c', help='Type of Corpus [Aquas, SonEspases]')

    args = parser.parse_args()

    init(Corpus= args.c)