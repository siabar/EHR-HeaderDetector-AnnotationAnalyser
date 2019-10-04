import argparse
import csv
import os
from collections import OrderedDict

fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)

Set = None
original_dir = ""
pre_processing_dir = ""
post_processing_ann_dir = ""
post_processing_csv_dir = ""

def init(Set):
    global original_dir, pre_processing_dir, post_processing_ann_dir, post_processing_csv_dir

    main_dir = os.path.join(parentDir, "Annotated", "set" + Set)
    original_dir = os.path.join(main_dir, "original")
    pre_processing_dir = os.path.join(main_dir, "pre_processing")
    post_processing_ann_dir = os.path.join(main_dir, "post_processing_ann")
    post_processing_csv_dir = os.path.join(main_dir, "post_processing_csv")

def annators():
    list_annotators = []
    for sub_dir in os.listdir(original_dir):
        list_annotators.append(sub_dir)

    return list_annotators


def pre_processing(annotators):
    list_files = set()
    for dir in annotators:
        os.makedirs(os.path.join(pre_processing_dir, dir), exist_ok=True)
        for original_files in os.listdir(os.path.join(original_dir, dir)):
            if original_files.endswith(".ann"):
                list_files.add(original_files)
                with open(os.path.join(original_dir, dir,original_files), "r") as r:
                    with open(os.path.join(pre_processing_dir, dir,original_files),"w+") as w:
                        for full_line in r:
                            line = full_line.split("\t",1)[1]
                            # if not (line.startswith("HORA") or full_line.startswith("#") or line.startswith("FECHA") or line.startswith("_SUG_")):
                            if not (line.startswith("HORA") or full_line.startswith("#") or line.startswith("FECHA")):

                                w.write(full_line)
                        w.close()
                    r.close()

    return list_files


def post_processing(annotators, list_files):

    for files in list_files:
        with open(os.path.join(post_processing_ann_dir, files),"w+") as w_ann, open(os.path.join(post_processing_csv_dir,files+ ".csv"), "w+") as w_csv:
            all_ann_dict = OrderedDict()
            counter = 0
            csv_writer = csv.writer(w_csv, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([" "]+ annotators)
            for dir in annotators:
                with open(os.path.join(pre_processing_dir,dir,files),"r") as r:
                    for line in r:
                        if line.strip():
                            row = line.strip().split("\t",1)
                            w_ann.write("T"+ str(counter) + "\t" + row[1] + "\n")
                            w_ann.write("#"+str(counter) + "\tAnnotatorNotes " + "T"+ str(counter) +"\t" + dir + "\n")
                            if row[1] in all_ann_dict.keys():
                                temp = all_ann_dict.get(row[1])
                                temp.append(dir)
                                update = {row[1]: temp}
                                all_ann_dict.update(update)
                            else:
                                all_ann_dict[row[1]] = [dir]
                            counter+=1
                    r.close()
            w_ann.close()
            for rows in all_ann_dict.keys():
                anns_list = all_ann_dict.get(rows)
                temp_list = []

                for dir in annotators:
                    if dir in anns_list:
                        temp_list.append("X")
                    else:
                        temp_list.append("")
                csv_writer.writerow([rows] + temp_list)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="comparing")

    parser.add_argument('--set', help='Which set is going to compare')

    args = parser.parse_args()
    Set =   args.set

    init(Set)
    list_annotators = annators()
    list_files = pre_processing(list_annotators)
    post_processing(list_annotators, list_files)

