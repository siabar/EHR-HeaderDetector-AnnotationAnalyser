import os
import xml.etree.ElementTree as ET
import shutil
import ntpath
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import csv
import unidecode
import collections

fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)


def trim_name(name):
    unaccent_name = unidecode.unidecode(name)
    for i, ch in enumerate(reversed(unaccent_name)):
        if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
            if i == 0:
                return name
            else:
                return name[:-1 * i]


def get_allinfo(xml_files, filter=False, move=True):
    """
    :param xml_files: input files
    :param filter: Select/filter the files that have all needed headers (important_headers.txt in Data directory) [True/False]
    :param move: if move is True, copy the selected files based (based on filter option) to a new directory
    :return:
        dictOfFiles: a dictionary that files are keys and the headers of the files are values
        dictOfHeaders: a dictionary that headers are keys and the files that have that headers are values
        header_cooccurrences: a dictionary that headers are keys and a dictionary of its co-occurance headers and number of occure are values
        dictOfHeaders_childs: a dictionary that headers are keys and a list of variants of the headers are values
    """

    header_list = os.path.join(parentDir, "data/headers.txt")
    dictOfHeaders = dict()
    dictOfHeaders_childs = dict()
    with open(header_list) as f:
        for i in f:
            head = i.strip().split("\t")
            if len(head) >= 2:
                h = head[1].strip()
                if (dictOfHeaders.get(h) == None):
                    dictOfHeaders_childs[h] = []
                    dictOfHeaders[h] = []

    content = []
    if filter:
        content = get_importantheaders()

    dictOfFiles = dict()
    header_cooccurrences = dict()
    count = 0
    for file in xml_files:
        filename = ntpath.basename(file)

        tags = []
        try:
            root = ET.parse(file).getroot()
            pre = ""
            name = ""
            counter = 1
            pre_header = ""
            for type_tag in root.findall('Section'):

                for type_child in type_tag.findall('name'):
                    name = type_child.text

                x = str(type_tag.get('id')).strip()
                # pure_name_eq = name.split("=",2)
                # pure_name = pure_name_eq[0].split("-!-",2)
                #
                # name = pure_name[0]
                if (x != "DEFAULT_HEADER") and (pre_header != x):
                    counter += 1
                    if pre == "":
                        pre = x
                    else:
                        new = x
                        if header_cooccurrences.get(pre) is not None:
                            co_occoure_pre = header_cooccurrences.get(pre)
                            if co_occoure_pre.get(new) is not None:
                                co_occoure_pre[new] = co_occoure_pre.get(new) + 1
                            else:
                                co_occoure_pre[new] = 1
                            header_cooccurrences[pre] = co_occoure_pre
                        else:
                            header_cooccurrences[pre] = {new: 1}
                        pre = new

                    if x not in tags:
                        tags.append(x)

                    if dictOfHeaders_childs.get(x) is not None:
                        listchilds = dictOfHeaders_childs.get(x)
                        trimedname = trim_name(name)
                        if trimedname not in listchilds:
                            listchilds.append(trimedname)
                            updated = {x: listchilds}
                            dictOfHeaders_childs.update(updated)
                pre_header = x
            if filter == True:
                acceptable = True
                for cont in content:
                    if cont not in tags:
                        acceptable = False
                        break
                if acceptable:
                    for val in tags:
                        if dictOfHeaders.get(val) is not None:
                            list_headers = dictOfHeaders.get(val)
                            list_headers.append(filename)
                            updated = {val: list_headers}
                            dictOfHeaders.update(updated)
                        else:
                            print("This tag in XML file is not exist in HEADER list:  " + val)
                    dictOfFiles[filename] = tags
                    if move:
                        pathdir = ntpath.dirname(file).replace("XML_SECTION", "SELECTED_XML")
                        os.makedirs(pathdir,exist_ok=True)
                        shutil.copy(file, pathdir)
            else:
                dictOfFiles[filename] = tags
                for val in tags:
                    if (dictOfHeaders.get(val) != None):
                        list_headers = dictOfHeaders.get(val)
                        list_headers.append(filename)
                        updated = {val: list_headers}
                        dictOfHeaders.update(updated)
                    else:
                        print("This tag in XML file is not exist in HEADER list:  " + val)
            f.close()
        except:
            print("ERROR", filename, sys.exc_info())
    return dictOfFiles, dictOfHeaders, header_cooccurrences, dictOfHeaders_childs


def showbasicinfo(x, y):
    """
    :param x: a list of all files
    :param y: a list of number of headers of each file (in order of x)
    :return:
        PLOT the data
    """
    plt_dir = os.path.join(parentDir, "analysis_headers/PLOT/")
    os.makedirs(plt_dir, exist_ok=True)
    plot_file = os.path.join(plt_dir, "Fiq" + ".png")

    d = {"Headers": x, "Filesnumber": y}
    data = pd.DataFrame(d)
    data.set_index('Headers', inplace=True)


    colors = plt.get_cmap()(
        np.linspace(0.15, 0.85, len(y)))


    ax1 = data.sort_values(by='Filesnumber').plot(kind='barh', figsize=(30, 20), color='#86bf91', fontsize=8,
                                                  legend=False)


    ax1.set_alpha(0.4)
    ax1.set_xlabel("Number of Files", labelpad=20, fontsize=12)
    ax1.set_ylabel("Name of Headers", labelpad=20, fontsize=12)
    totals = []
    for i in ax1.patches:
        totals.append(i.get_width())

    total = sum(totals)

    for i in ax1.patches:

        ax1.text(i.get_width() + .3, i.get_y() + .10,
                 "  " + str(i.get_width()), fontsize=10,
                 color='dimgrey')


    plt.margins(0.1)
    plt.subplots_adjust(left=0.25)
    plt.savefig(str(plot_file), bbox_inches='tight')
    plt.show()




def print_csv(dict_of_files, x, y, yy, header_cooccurrences, dict_of_headers_childs):
    """
    :param dictOfFiles: a dictionary that files are keys and the headers of the files are values
    :param x: a list of all files
    :param y: a list of number of headers of each file (in order of x)
    :param yy: a list of all headers of each file (in order of x)
    :param header_cooccurrences: a dictionary that headers are keys and a dictionary of its co-occurrences headers and number of occure are values
    :param dict_of_headers_childs: a dictionary that headers are keys and a list of variants of the headers are values
    :return:
        Save analysis on csv files
    """
    csv_dir = os.path.join(parentDir, "analysis_headers/CSV/")
    os.makedirs(csv_dir, exist_ok=True)
    csv_files = os.path.join(csv_dir,   "analysis_files.csv")
    csv_headers = os.path.join(csv_dir, "analysis_headers.csv")
    csv_headers_number = os.path.join(csv_dir, "analysis_headers-number.csv")
    csv_header_cooccurrences = os.path.join(csv_dir, "analysis_header_co-occurrences.csv")
    csv_header_children = os.path.join(csv_dir,  "analysis_original_headers_in_report.csv")
    csv_top_10_cooccurrences = os.path.join(csv_dir,  "top_10_header_co-occurrences.csv")

    d = {"Headers": x, "Filesnumber": y}
    data = pd.DataFrame(d)
    data_sorted = data.sort_values(by=["Filesnumber"], ascending=False)
    data_sorted.to_csv(csv_headers_number, index=False, sep='\t')


    with open(csv_headers, mode='w+') as csv_headers_f:
        for key, value in zip(x, yy):
            csv_headers_f.write(key + "\t" + value)
            csv_headers_f.write('\n')

    with open(csv_header_cooccurrences, 'w+') as f:

        csv_writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["\t"] + x)
        temp = {}
        for r in x:
            values = {}
            if header_cooccurrences.get(r) is not None:
                values = header_cooccurrences.get(r)
            output = []
            output.append(r)

            for c in x:
                if values.get(c) is not None:
                    sum_r_c = values.get(c)



                    if header_cooccurrences.get(c) is not None and c != r:
                        if header_cooccurrences.get(c).get(r) is not None:
                            sum_r_c += header_cooccurrences.get(c).get(r)
                    output.append(sum_r_c)

                    temp_rc = r.replace("SECCION_", "") + "\t" + c.replace("SECCION_", "")
                    temp_cr = c.replace("SECCION_", "") + "\t" + r.replace("SECCION_", "")

                    if temp_rc not in temp.keys() and temp_cr not in temp.keys():
                        temp[temp_rc] = sum_r_c
                else:
                    sum_r_c = 0
                    if header_cooccurrences.get(c) is not None and c != r:
                        if header_cooccurrences.get(c).get(r) is not None:
                            sum_r_c += header_cooccurrences.get(c).get(r)
                    output.append(sum_r_c)
            csv_writer.writerow(output)

    sorted_x = sorted(temp.items(), key=lambda kv: kv[1], reverse=True)

    sorted_dict = collections.OrderedDict(sorted_x)
    row = 0
    w = open(csv_top_10_cooccurrences,"w")
    csv_writer = csv.writer(w, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    for key, value in sorted_dict.items():
        if row == 10:
            break
        csv_writer.writerow(key.split("\t") + [str(value)])
        row += 1

    w.close()


    with open(csv_files, mode='w') as csv_f:
        csv_writer = csv.writer(csv_f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["\t"] + x)
        for keys, values in dict_of_files.items():
            output = []
            output.append(keys)
            for val in x:
                if val in values:
                    output.append(1)
                else:
                    output.append(0)

            csv_writer.writerow(output)

    with open(csv_header_children, mode='w') as csv_f:
        csv_writer = csv.writer(csv_f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for keys, values in dict_of_headers_childs.items():
            output = []
            output.append(keys.replace("SECCION_",""))
            output.append(len(values))
            for val in values:
                output.append(val)
            csv_writer.writerow(output)

def get_importantheaders():
    importnat_list = os.path.join(parentDir, "data/important_headers.txt")
    with open(importnat_list) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def analysis(**kwargs):
    """
    :param kwargs: the given arguments by user
    :return:
        save the analysis data on csv file (see the README) and plot the number of headers
    """
    filter = kwargs['filter']
    strict = kwargs['strict']
    xml_files = kwargs['xml_files']
    dictOfFiles, dictOfHeaders, header_cooccurrences, dictOfHeaders_childs = get_allinfo(xml_files, filter)

    if len(dictOfHeaders)== 0:
        if filter:
            print("No file has the requested headers in important_headers.txt file")
        else:
            print("No file has been found")
    importantHeaders = get_importantheaders()
    x = []
    y = []
    yy = []
    for key, value in dictOfHeaders.items():
        if len(value) > 0:
            if strict:
                if key in importantHeaders:
                    x.append(key)
                    y.append(len(value))
                    yy.append(",".join(value))
                    # print("Header: " + key + "\tFiles: " + "\t".join(value))
            else:
                x.append(key)
                y.append(len(value))
                yy.append(",".join(value))
        # else:
            # print("The files do not have any section about: " + key)

    print_csv(dictOfFiles, x, y, yy, header_cooccurrences, dictOfHeaders_childs)

    if len(x) > 0:
        showbasicinfo(x, y)
    # else:
    #     print("No files have been found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analysis")

    parser.add_argument('-f', '--filter',
                        help="filter files that have all headers at important_headers.txt (in data directory), and move the filterred file into 'SELECTED_XML' directory ",
                        action="store_true")

    parser.add_argument('-s', '--strict',
                        help="Analysis headers at important_headers.txt ",
                        action="store_true")

    args = parser.parse_args()

    list_files = []
    list_file_names = []

    main_root = os.path.join(parentDir, "documents", "XML_SECTION")

    for xml_files in os.listdir(main_root):
        if xml_files.endswith(".xml"):
            list_files.append(os.path.join(main_root, xml_files))


    analysis(filter=args.filter, strict=args.strict, xml_files=list_files)
