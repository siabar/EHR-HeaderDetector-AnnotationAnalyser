import os


def header_path(bunch, parentDir):
    """
    :param bunch: Number of bunch
    :param parentDir: Path of the parent directory
    :return:
        related file of the current bunch that contains the predefined sections
    """
    header_file = None
    if int(bunch.split("+")[0]) <= 2:
        header_file = os.path.join(parentDir, "data/headers_original_bunch_1-2.txt")
    elif int(bunch.split("+")[0]) == 3:
        header_file = os.path.join(parentDir, "data/headers_17.12.2019_bunch_3.txt")
    elif int(bunch.split("+")[0]) == 4:
        header_file = os.path.join(parentDir, "data/headers_28.11.2019_bunch_4.txt")
    elif int(bunch.split("+")[0]) == 5:
        header_file = os.path.join(parentDir, "data/headers_17.12.2019_bunch_5.txt")
    elif int(bunch.split("+")[0]) == 6:
        header_file = os.path.join(parentDir, "data/headers_11.01.2020_bunch_6.txt")
    elif int(bunch.split("+")[0]) == 7:
        header_file = os.path.join(parentDir, "data/headers_11.01.2020_bunch_7.txt")

    return header_file
