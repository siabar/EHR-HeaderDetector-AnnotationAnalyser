import os
import xml.etree.ElementTree as ET
import glob
import shutil
import ntpath
import sys
# Import `pyplot` from `matplotlib`
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import lxml.etree as ET
import argparse
import csv
import unidecode


fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)


def trim_name(name):
    unaccent_name=unidecode.unidecode(name)
    for i, ch in enumerate(reversed(unaccent_name)):
        if ((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')):
            if i == 0:
                return name
            else:
                return name[:-1*i]

def get_allinfo(xml_files, filter=False, move=True, corpus='Aquas'):

    header_list = os.path.join(parentDir, "data/headers.txt")
    header = []
    dictOfHeaders = dict()
    dictOfHeaders_childs = dict()
    with open(header_list) as f:
        for i in f:
            head = i.strip().split("\t")
            if len(head)>=2:
                h = head[1].strip()
                if (dictOfHeaders.get(h) == None):
                    dictOfHeaders_childs[h] = []
                    dictOfHeaders[h] = []

    content = []
    if filter ==True:
        content= get_importantheaders()

    # parser = ET.XMLParser(encoding="UTF-8")

    # home =  os.path.join(parentDir, "documents/")
    # files = glob.glob("/home/siabar/30yamak/git/EHR-normalizer/documents/XML-" + corpus + "/*.xml")

    # files = glob.glob(xml_dir + "/*.xml")
    # Brat_dir = home + "BRAT-" + corpus

    dictOfFiles = dict()
    header_cooccurrences = dict()
    count = 0
    for file in xml_files:
        filename = ntpath.basename(file)

        # print(filename)

        tags = []
        try:
            root = ET.parse(file).getroot()
            pre = ""
            new  = ""
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
                if (x != "DEFAULT_HEADER") and (pre_header!=x):
                    counter += 1
                    if pre == "":
                        pre = x
                    else:
                        new=x
                        if (header_cooccurrences.get(pre) != None):
                             co_occoure_pre= header_cooccurrences.get(pre)
                             if (co_occoure_pre.get(new) != None):
                                 co_occoure_pre[new] = co_occoure_pre.get(new) + 1
                             else:
                                 co_occoure_pre[new] = 1
                             header_cooccurrences[pre] = co_occoure_pre
                        else:
                            header_cooccurrences[pre] = {new:1}
                        pre=new

                    if x not in tags:
                        tags.append(x)

                    if (dictOfHeaders_childs.get(x) != None):
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
                    if ((cont not in tags)):
                        acceptable = False
                        break
                if (acceptable):
                    for val in tags:
                        if (dictOfHeaders.get(val) != None):
                            listHeaders = dictOfHeaders.get(val)
                            listHeaders.append(filename)
                            updated = {val: listHeaders}
                            dictOfHeaders.update(updated)
                        else:
                            print("This tag in XML file is not exist in HEADER list:  " + val)
                    dictOfFiles[filename] = tags
                    if move:
                        shutil.copy(file, os.path.join(parentDir, "documents/Fined_XML"))
            else:
                dictOfFiles[filename] = tags
                for val in tags:
                    if (dictOfHeaders.get(val) != None):
                        listHeaders = dictOfHeaders.get(val)
                        listHeaders.append(filename)
                        updated = {val: listHeaders}
                        dictOfHeaders.update(updated)
                    else:
                        print("This tag in XML file is not exist in HEADER list:  " + val)
            f.close()
        except:
            print("ERROR", filename, sys.exc_info())
    return  dictOfFiles, dictOfHeaders, header_cooccurrences, dictOfHeaders_childs



def showbasicinfo(x,y,corpus):
    plt_dir = os.path.join(parentDir, "analysis_headers/PLOT/")
    os.makedirs(plt_dir,exist_ok=True)
    plot_file = os.path.join(plt_dir,"Fiq_" + corpus + ".png")
    # x = []
    # y = []
    # for key, value in dictOfHeaders.items():
    #     if (len(value) > 0):
    #         x.append(key)
    #         y.append(len(value))

    # print(x, y)

    d = {"Headers": x, "Filesnumber": y}
    data = pd.DataFrame(d)
    data.set_index('Headers', inplace=True)

    # Initialize the plot
    # fig = plt.figure(figsize=(20,10))
    #
    # ax1 = fig.add_subplot(121)
    # ax2 = fig.add_subplot(122)
    # Prepare the data

    colors = plt.get_cmap()(
        np.linspace(0.15, 0.85, len(y)))

    # PLOT the data

    # ax1.barh(x, y, color=colors, align='center')
    # ax1.set_xlabel('Number of Files')
    # ax1.set_ylabel('Name of Headers')
    # ax1.set_title('How many files have each given headers')
    # sorted_list = sorted(y)
    # ax1.set_xticks(sorted_list)

    ax1 = data.sort_values(by='Filesnumber').plot(kind='barh', figsize=(30, 20), color='#86bf91', fontsize=8,
                                                 legend=False)

    from matplotlib.ticker import StrMethodFormatter

    ax1.set_alpha(0.4)
    # ax1.set_title("How many files have each given header", fontsize=12)
    ax1.set_xlabel("Number of Files", labelpad=20, fontsize=12)
    ax1.set_ylabel("Name of Headers", labelpad=20, fontsize=12)
    totals = []
    for i in ax1.patches:
        totals.append(i.get_width())

    # set individual bar lables using above list
    total = sum(totals)

    # set individual bar lables using above list
    for i in ax1.patches:
        # get_width pulls left or right; get_y pushes up or down
        # ax1.text(i.get_width() + .3, i.get_y() + .18,
        #          str(round((i.get_width() / total) * 100, 2)) + '%' + " (" + str(i.get_width()) + ")", fontsize=10,
        #          color='dimgrey')
        ax1.text(i.get_width() + .3, i.get_y() + .10,
                 "  " + str(i.get_width()), fontsize=10,
                 color='dimgrey')

    # invert for largest on top
    # ax1.invert_yaxis()
    #
    plt.margins(0.1)
    plt.subplots_adjust(left=0.25)
    plt.savefig(str(plot_file),bbox_inches='tight')
    plt.show()

    # def func(pct, allvals):
    #     absolute = float(pct/100.*np.sum(allvals))
    #     return "{:1.1f}%\n({:1.0f})".format(pct, absolute)
    # #
    # fig = plt.figure(figsize=(20,10))
    # ax2 = fig.add_subplot(111)
    #
    # ax2.pie(y, labels =x, explode = ((0.05),)*len(x),autopct = lambda pct: func(pct, y))
    # # Add a legend
    # # plt.legend()
    #
    # # Show the plot
    # plt.show()

def print_csv(dictOfFiles, x, y, yy, header_cooccurrences,dictOfHeaders_childs,corpus):


    csv_dir = os.path.join(parentDir, "analysis_headers/CSV/")
    os.makedirs(csv_dir, exist_ok=True)
    csv_files = os.path.join(csv_dir, corpus + "_analysis_files.csv")
    csv_headers = os.path.join(csv_dir, corpus + "_analysis_headers.csv")
    csv_headers_number = os.path.join(csv_dir, corpus + "_analysis_headers-number.csv")
    csv_header_cooccurrences= os.path.join(csv_dir, corpus + "_analysis_header_co-occurrences.csv")
    csv_header_children = os.path.join(csv_dir, corpus + "_analysis_original_headers_in_report.csv")


    d = {"Headers": x, "Filesnumber": y}
    data = pd.DataFrame(d)
    data_sorted = data.sort_values(by=["Filesnumber"], ascending=False)
    data_sorted.to_csv(csv_headers_number,  index=False, sep='\t')

    # d = {"Headers": x, "Files": yy}
    # data = pd.DataFrame(d)
    # print(data.head())
    # data.to_csv(csv_headers, index = False, sep='\t' )
    with open(csv_headers, mode='w+') as csv_headers_f:
        for key, value in zip(x,yy):
            csv_headers_f.write(key + "\t" + value)
            csv_headers_f.write('\n')



    with open(csv_header_cooccurrences, 'w+') as f:
        # for key, values in sorted(header_cooccurrences.items(), key = lambda kv:(kv[1], kv[0]), reverse=True):
        #     f.write("%s\t%s\n" % (key, values))
        csv_writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["\t"]+x)
        # for key, values in header_cooccurrences.items():
        #     output  = []
        #     output.append(key)
        #     for keys in x:
        #         if values.get(keys) !=  None:
        #             output.append(values.get(keys))
        #         else:
        #             output.append(0)
        #     csv_writer.writerow(output)


        # for r in x:
        #     if (header_cooccurrences.get(r)!= None):
        #         values = header_cooccurrences.get(r)
        #         output  = []
        #         output.append(r)
        #         for c in x:
        #             if values.get(c) !=  None:
        #                 sum_r_c = values.get(c)
        #                 if header_cooccurrences.get(c)!= None and c!=r:
        #                     if header_cooccurrences.get(c).get(r)!= None:
        #                         sum_r_c += header_cooccurrences.get(c).get(r)
        #                 output.append(sum_r_c)
        #             else:
        #                 sum_r_c = 0
        #                 if header_cooccurrences.get(c)!= None and c!=r:
        #                     if header_cooccurrences.get(c).get(r)!= None:
        #                         sum_r_c += header_cooccurrences.get(c).get(r)
        #                 output.append(sum_r_c)
        #         csv_writer.writerow(output)
        for r in x:
            values = {}
            if (header_cooccurrences.get(r)!= None):
                values = header_cooccurrences.get(r)
            output  = []
            output.append(r)
            for c in x:
                if values.get(c) !=  None:
                    sum_r_c = values.get(c)
                    if header_cooccurrences.get(c)!= None and c!=r:
                        if header_cooccurrences.get(c).get(r)!= None:
                            sum_r_c += header_cooccurrences.get(c).get(r)
                    output.append(sum_r_c)
                else:
                    sum_r_c = 0
                    if header_cooccurrences.get(c)!= None and c!=r:
                        if header_cooccurrences.get(c).get(r)!= None:
                            sum_r_c += header_cooccurrences.get(c).get(r)
                    output.append(sum_r_c)
            csv_writer.writerow(output)


    # header_list = os.path.join(parentDir, "data/headers.txt")
    # header = []
    # with open(header_list) as f:
    #     for i in f:
    #         head = i.strip().split("\t")
    #         if len(head)>=2:
    #             h = head[1].strip()
    #             if (h not in header):
    #                 header.append(h)
    #
    with open(csv_files, mode='w') as csv_f:
        csv_writer = csv.writer(csv_f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["\t"]+x)
        for keys, values in dictOfFiles.items():
            output  = []
            output.append(keys)
            for val in x:
                if val in values:
                    output.append(1)
                else:
                    output.append(0)
                # if val != "DEFAULT_HEADER":
                #     output.append(val)
            csv_writer.writerow(output)

    with open(csv_header_children, mode='w') as csv_f:
        csv_writer = csv.writer(csv_f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        # csv_writer.writerow(["\t"]+x)
        for keys, values in dictOfHeaders_childs.items():
            output  = []
            output.append(keys)
            for val in values:
                output.append(val)
            csv_writer.writerow(output)
            # csv_f.write(keys + "," + ",".join(values) + "\n")



def get_importantheaders():
    importnat_list = os.path.join(parentDir, "data/important_headers.txt")
    with open(importnat_list) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

def analysis(**kwargs):
    filter = kwargs['filter']
    strict = kwargs['strict']
    corpus = kwargs['corpus']
    XML_files = kwargs['XML_files']
    dictOfFiles, dictOfHeaders, header_cooccurrences, dictOfHeaders_childs = get_allinfo(XML_files, filter, corpus=corpus)

    # dictOfHeaders = filtering(dictOfFiles, combination)


    importantHeaders = get_importantheaders()
    x = []
    y = []
    yy = []
    for key, value in dictOfHeaders.items():
        if (len(value) > 0):
            if (strict == True):
                if (key in importantHeaders):
                    x.append(key)
                    y.append(len(value))
                    yy.append(",".join(value))
                    print("Header: " + key + "\tFiles: " +  "\t".join(value))
            else:
                x.append(key)
                y.append(len(value))
                yy.append(",".join(value))
                # print("Header: " + key + "\tFiles: " + "\t".join(value))
        else:
            print("The files do not have any section about: " + key)

    print_csv(dictOfFiles, x, y, yy, header_cooccurrences, dictOfHeaders_childs, corpus)
    #Show Basic Info
    # print(x,y)
    if len(x)>0:
        showbasicinfo(x,y,corpus)
    else:
        print("No files have been found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analysis")

    parser.add_argument('-f', '--filter',
                        help="Filter files based on needed headers",
                        action = "store_true")

    parser.add_argument('-s', '--strict',
                        help="Show just analysis of filtered headers",
                        action = "store_true")

    parser.add_argument('-c', help='Type of Corpus [Aquas, SonEspases]')

    parser.add_argument('--set', help='Which set is going to compare')

    args = parser.parse_args()
    Set =   args.set





    list_files = []
    list_file_names = []

    main_root = os.path.join(parentDir, "documents", "XML_SECTION")

    for dirpath, dirnames, filenames in os.walk(main_root):
        if Set!=None:
            if not dirpath.endswith(Set):
                continue
        for filename in [f for f in filenames if f.endswith(".xml") and not f.startswith(".DS_Store")]:
            if filename not in list_file_names:
                list_files.append(os.path.join(dirpath, filename))
                list_file_names.append(filename)

    # for text_files in os.listdir(main_root):
    #     if not text_files.startswith(".DS_Store"):
    #         XML_Directory = os.path.join(main_root,text_files, Set)


    analysis(filter=args.filter, strict=args.strict, corpus= args.set, XML_files=list_files)




