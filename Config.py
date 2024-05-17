import openpyxl
from openpyxl import utils
from openpyxl import styles

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


class Config:

    def __init__(self):
        self.IPGS = ['570 A9', '570 X-19', 'evIPG-12G', 'evIPG-3G']
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
        with open("Config/expected", "r") as file:
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
        with open("Config/testconfig", "r") as file:
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
                    # Checking if it is a valid standard
                    FORMAT = line.strip().split(' ')
                    LINK = PHABRIX_VALUES_LINK.get(FORMAT[0], 'INVALID')
                    LINE = PHABRIX_VALUES_LINE.get(FORMAT[1], 'INVALID')
                    RATE = PHABRIX_VALUES_FRAME_RATE.get(FORMAT[2], 'INVALID')
                    self.PHABRIX_VALUE.append([LINK, LINE, RATE])
                    if LINK != "INVALID" and LINE != "INVALID" and RATE != "INVALID":
                        self.FORMATS.append(FORMAT)
                    else:
                        self.FORMATS.append(["INVALID", "", "(Check test config)"])

                if "STANDARDS" in line:
                    record = True

    def save_config(self, filename):
        HEADINGS = ["#", "IPG Out Tested", "Format on Phabrix", "OutputAv", "Vertical Offset", "AES", "Delay Right", "Delay Left","Min", "Max", "Result"]
        CENTERED = openpyxl.styles.Alignment(horizontal='center')
        workbook = openpyxl.Workbook(write_only=True)
        get_col_let = utils.get_column_letter
        worksheet = workbook.create_sheet()
        worksheet.title = "IPG Lip Sync test results"
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

        cells = [openpyxl.cell.WriteOnlyCell(worksheet) for _ in range(len(HEADINGS))]
        for count, heading in enumerate(HEADINGS):
            cells[count].value = HEADINGS[count]
        worksheet.append(cells)
        for result in self.test_result:
            worksheet.append(result)
        workbook.save(filename)


if __name__ == "__main__":
    config_instance = Config()
