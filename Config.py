import openpyxl
from openpyxl import utils
from openpyxl.styles import Alignment

LINK_TYPES = ['SD', 'HD', '3GA']
LINK_LINE_SUPPORTED = {
    'SD': ['525i', '625i'],
    'HD': ['720p', '1080i', '1080sF', '1080p'],
    '3GA': ['720p', '1080i', '1080sF', '1080p']
}
FRAME_RATES_SUPPORTED = {
    '525i': ['59.94'],
    '625i': ['50'],
    '720p': ['23.98', '24', '25', '29.97', '30', '50', '59.94', '60'],
    '1080i': ['50', '59.94', '60'],
    '1080sF': ['23.98', '24', '25', '29.97', '30'],
    '1080p': ['23.98', '24', '25', '29.97', '30']
}
PHABRIX_VALUES_LINK = {
    'SD': 0,
    'HD': 1,
    '3GA': 3
}
PHABRIX_VALUES_LINE = {
    '525i': 0,
    '625i': 1,
    '720p': 2,
    '1080i': 4,
    '1080sF': 5,
    '1080p': 6
}
PHABRIX_VALUES_FRAME_RATE = {
    '23.98': 0,
    '24': 1,
    '25': 2,
    '29.97': 3,
    '30': 4,
    '50': 5,
    '59.94': 6,
    '60': 7
}
IPGS = ['570 A9', '570 X-19', 'evIPG-12G', 'evIPG-3G']


class Config:

    def __init__(self):
        self.PHABRIX_VALUE = []
        self.FORMATS = []
        self.OUTPUT_AV_SYNC = []
        self.VERTICAL_OFFSET = []
        self.AES67 = []
        self.OUTS = []
        self.DELAY = 0
        self.test_result = []
        self.EXPECTED = {}
        self.load_config()
        self.load_expected()

    def load_expected(self):
        self.EXPECTED = {}
        with open("Config/expected.txt", "r") as file:
            for line in file:
                if "//" in line:
                    continue
                if "END" in line:
                    break
                row = line.strip().split(" ")
                key = f"{row[0]}{row[1]}{row[2]}{row[3]}{row[4]}"
                value1 = float(row[5])
                value2 = float(row[6])
                self.EXPECTED[key] = [value1, value2]

    def load_config(self):
        self.PHABRIX_VALUE = []
        self.OUTS = []
        self.OUTPUT_AV_SYNC = []
        self.VERTICAL_OFFSET = []
        self.AES67 = []
        self.FORMATS = []
        self.DELAY = 0
        record = False
        with open("Config/testconfig.txt", "r") as file:
            for line in file:
                # Checking if the line is a comment or not
                if "//" in line:
                    continue

                if "DELAY" in line:
                    self.DELAY = int(next(file).strip())

                if "IPGOUTS" in line:
                    self.OUTS = [int(x) for x in next(file).strip().split(' ')]  # Converts them to integer

                if "OUTPUT_AV_SYNC" in line:
                    self.OUTPUT_AV_SYNC = [int(x) for x in next(file).strip().split(' ')]  # Converts them to integer

                if "VERTICAL_OFFSET" in line:
                    self.VERTICAL_OFFSET = [int(x) for x in next(file).strip().split(' ')]  # Converts them to integer

                if "AES" in line:
                    self.AES67 = [int(x) for x in next(file).strip().split(' ')]  # Converts them to integer

                if "END_RECORD" in line:
                    record = False
                if record:
                    # Checking if user made a mistake
                    FORMAT = line.strip().split(' ')
                    LINK = PHABRIX_VALUES_LINK.get(FORMAT[0], 'INVALID')
                    LINE = PHABRIX_VALUES_LINE.get(FORMAT[1], 'INVALID')
                    RATE = PHABRIX_VALUES_FRAME_RATE.get(FORMAT[2], 'INVALID')
                    if LINK != "INVALID" and LINE != "INVALID" and RATE != "INVALID":
                        # Checking if format exists or not
                        if FORMAT[1] in LINK_LINE_SUPPORTED[FORMAT[0]] and FORMAT[2] in \
                                FRAME_RATES_SUPPORTED[FORMAT[1]]:
                            self.PHABRIX_VALUE.append([LINK, LINE, RATE])  # Appending them as is as it is valid
                            self.FORMATS.append(FORMAT)
                        else:
                            self.PHABRIX_VALUE.append(['INVALID', 'INVALID', 'INVALID'])
                            self.FORMATS.append(["Not a valid format", "", "(Check testcongif file)"])
                    else:
                        self.FORMATS.append(["INVALID", "", "(Check testconfig file)"])

                if "STANDARDS" in line:
                    record = True

    def save_config(self, filename):
        HEADINGS = ["#", "IPG Out Tested", "Format on Phabrix", "OutputAv", "Vertical Offset", "AES", "Delay Right",
                    "Delay Left", "Min", "Max", "Result"]
        workbook = openpyxl.Workbook()

        get_col_let = utils.get_column_letter
        default_sheet = workbook.active
        workbook.remove(default_sheet)

        worksheet = workbook.create_sheet(title="IPG Lip Sync test results")

        worksheet.column_dimensions[get_col_let(1)].width = 3
        worksheet.column_dimensions[get_col_let(2)].width = 16
        worksheet.column_dimensions[get_col_let(3)].width = 18
        worksheet.column_dimensions[get_col_let(4)].width = 12
        worksheet.column_dimensions[get_col_let(5)].width = 13
        worksheet.column_dimensions[get_col_let(6)].width = 5.5
        worksheet.column_dimensions[get_col_let(7)].width = 12
        worksheet.column_dimensions[get_col_let(8)].width = 12
        worksheet.column_dimensions[get_col_let(9)].width = 12
        worksheet.column_dimensions[get_col_let(10)].width = 12

        worksheet.append(HEADINGS)

        for result in self.test_result:
            worksheet.append(result)

        for row in worksheet.iter_rows():
            for cell in row:
                cell.alignment = Alignment(horizontal='left')

        workbook.save(filename)


if __name__ == "__main__":
    config_instance = Config()
