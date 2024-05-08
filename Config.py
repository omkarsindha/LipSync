
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
        self.OUTS = []
        self.DELAY = 0
        self.load_config()

    def load_config(self):
        self.PHABRIX_VALUE = []
        self.OUTS = []
        self.FORMATS = []
        self.DELAY = 0
        record = False
        with open("Config/testconfig", "r") as file:
            for line in file:
                line.lower()
                if "DELAY" in line:
                    self.DELAY = int(next(file).strip())

                if "IPGOUTS" in line:
                    self.OUTS = [int(x) for x in next(file).strip().split(',')]  # Converts them to integer

                if "END_RECORD" in line:
                    record = False
                if record:
                    self.FORMATS.append(line)
                    FORMAT = line.strip().split(' ')
                    print(FORMAT)
                    FORMAT[0] = PHABRIX_VALUES_LINK.get(FORMAT[0], 'INVALID')
                    FORMAT[1] = PHABRIX_VALUES_LINE.get(FORMAT[1], 'INVALID')
                    FORMAT[2] = PHABRIX_VALUES_FRAME_RATE.get(FORMAT[2], 'INVALID')
                    self.PHABRIX_VALUE.append(FORMAT)

                if "STANDARDS" in line:
                    record = True

if __name__ == "__main__":
    config_instance = Config()





