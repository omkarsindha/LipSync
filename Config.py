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
        self.OUTPUT_AV_SYNC = [0, 1]
        self.VERTICAL_OFFSET = [0, 4]
        self.AES67 = [0, 1]
        self.OUTS = []
        self.DELAY = 0
        self.test_result = []
        self.load_config()

    def load_config(self):
        self.PHABRIX_VALUE = []
        self.OUTS = []
        self.FORMATS = []
        self.DELAY = 0
        record = False
        with open("Config/testconfig", "r") as file:
            for line in file:
                if "DELAY" in line:
                    self.DELAY = int(next(file).strip())

                if "IPGOUTS" in line:
                    self.OUTS = [int(x) for x in next(file).strip().split(',')]  # Converts them to integer

                if "END_RECORD" in line:
                    record = False
                if record:
                    # Checking if it is a valid standard

                    FORMAT = line.strip().split(' ')
                    FORMAT[0] = PHABRIX_VALUES_LINK.get(FORMAT[0], 'INVALID')
                    FORMAT[1] = PHABRIX_VALUES_LINE.get(FORMAT[1], 'INVALID')
                    FORMAT[2] = PHABRIX_VALUES_FRAME_RATE.get(FORMAT[2], 'INVALID')
                    self.PHABRIX_VALUE.append(FORMAT)
                    self.FORMATS.append(line)

                if "STANDARDS" in line:
                    record = True

    def save_config(self):
        HEADINGS = ["#", "IPG Out Tested", "Format on Phabrix", "OutputAv", "Vertical Offset", "AES", "Delay Right", "Delay Left"]
        CENTERED = openpyxl.styles.Alignment(horizontal='center')
        workbook = openpyxl.Workbook(write_only=True)
        get_col_let = utils.get_column_letter
        worksheet = workbook.create_sheet()
        worksheet.title = "IPG Lip Sync test results"
        worksheet.column_dimensions[get_col_let(1)].width = 5
        worksheet.column_dimensions[get_col_let(2)].width = 16
        worksheet.column_dimensions[get_col_let(3)].width = 15
        worksheet.column_dimensions[get_col_let(4)].width = 20
        worksheet.column_dimensions[get_col_let(5)].width = 20
        worksheet.column_dimensions[get_col_let(6)].width = 20
        worksheet.column_dimensions[get_col_let(7)].width = 20
        worksheet.column_dimensions[get_col_let(8)].width = 20

        cells = [openpyxl.cell.WriteOnlyCell(worksheet) for _ in range(len(HEADINGS))]
        for count, heading in enumerate(HEADINGS):
            cells[count].value = HEADINGS[count]
        worksheet.append(cells)
        for result in self.test_result:
            worksheet.append(result)
        workbook.save("testing.xlsx")


if __name__ == "__main__":
    config_instance = Config()
