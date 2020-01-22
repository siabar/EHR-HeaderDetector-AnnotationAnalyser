import os


class utility():

    def __init__(self, bunch, parentDir):
        self.bunch = bunch
        self.parentDir = parentDir

    def header_path(self):
        header_file = None
        if int(self.bunch.split("+")[0]) <= 2:
            header_file = os.path.join(self.parentDir, "data/headers_original_bunch_1-2.txt")
        elif int(self.bunch.split("+")[0]) == 3:
            # header_file = os.path.join(self.parentDir, "data/headers_13.11.2019_bunch_3_original.txt")
            header_file = os.path.join(self.parentDir, "data/headers_17.12.2019_bunch_3.txt")
        elif int(self.bunch.split("+")[0]) == 4:
            header_file = os.path.join(self.parentDir, "data/headers_28.11.2019_bunch_4.txt")
        elif int(self.bunch.split("+")[0]) == 5:
            header_file = os.path.join(self.parentDir, "data/headers_17.12.2019_bunch_5.txt")
        elif int(self.bunch.split("+")[0]) == 6:
            header_file = os.path.join(self.parentDir, "data/headers_11.01.2020_bunch_6.txt")

        return header_file
