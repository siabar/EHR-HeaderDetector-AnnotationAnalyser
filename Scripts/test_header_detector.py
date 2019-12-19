import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analysis")
    parser.add_argument('--set', help='Which set is going to compare')
    args = parser.parse_args()
    Set = args.set

    # main_root = os.path.join(parentDir, "documents", "TXT")
    # for text_files in os.listdir(main_root):
    #     if not text_files.startswith("."):
    #         TXT_Directory = os.path.join(main_root, text_files, Set)
    #         XML_Directory = TXT_Directory.replace("TXT", "XML_SECTION")
    #         ANN_Directory = XML_Directory.replace("XML_SECTION", "ANN_SECTION")
    #
    #         xml(TXT_Directory, XML_Directory, Set)
    #         ann(XML_Directory, ANN_Directory)