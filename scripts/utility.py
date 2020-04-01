import os


def header_path(bunch, parentDir):
    """
    :param bunch: Number of bunch
    :param parentDir: Path of the parent directory
    :return:
        related file of the current bunch that contains the predefined sections
    """
    header_file = os.path.join(parentDir, "data/headers.txt")

    return header_file
