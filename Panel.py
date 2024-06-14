import os
import socket
import threading
import time
import ahttp
import phabrixlib
import wx


class Panel(wx.Panel):
    def __init__(self, parent, wxconfig, config):

        wx.Panel.__init__(self, parent)
        self.wxconfig = wxconfig
        self.config = config
        self.parent = parent
        self.main_vbox = wx.BoxSizer(wx.VERTICAL)
        main_box = wx.StaticBox(self, label='Test Configuration')
        main_box.SetFont(wx.Font(wx.FontInfo(12).Bold()))
        main_box_sizer = wx.StaticBoxSizer(main_box)

        # Making IPG selection sizer
        ipg_box = wx.StaticBox(self, label='IPG IP Address')
        ipg_box_sizer = wx.StaticBoxSizer(ipg_box)
        self.ipg_ip_input = wx.TextCtrl(self, size=(100, -1), value=wxconfig.Read('/ipgIP', defaultVal=""))
        ipg_box_sizer.Add(self.ipg_ip_input, 0, wx.EXPAND | wx.ALL, 5)

        # Making Magnum and port selection sizer
        magnum_box = wx.StaticBox(self, label="Magnum IP and Interface Port")
        magnum_box_sizer = wx.StaticBoxSizer(magnum_box)
        self.magnum_input = wx.TextCtrl(self, size=(100, -1), value=wxconfig.Read('/magnumIP', defaultVal=""))
        self.port_input = wx.TextCtrl(self, size=(50, -1), value=wxconfig.Read('/port', defaultVal=""))
        magnum_box_sizer.Add(self.magnum_input, 0, wx.ALL, 5)
        magnum_box_sizer.Add(self.port_input, 0, wx.EXPAND | wx.ALL, 5)

        # Making phabrix box sizer
        phabrix_box = wx.StaticBox(self, label="Phabrix IP Address")
        phabrix_box_sizer = wx.StaticBoxSizer(phabrix_box)
        self.phabrixIP_input = wx.TextCtrl(self, size=(90, -1), value=wxconfig.Read('/phabrixIP', defaultVal=""))
        phabrix_box_sizer.Add(self.phabrixIP_input, 0, wx.EXPAND | wx.ALL, 5)

        self.start_button = wx.Button(self, label="Start")
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)

        self.toggle_button = wx.Button(self, label="Toggle View")
        self.toggle_button.Bind(wx.EVT_BUTTON, self.on_toggle_view)

        self.reload_button = wx.Button(self, label="Reload Config")
        self.reload_button.Bind(wx.EVT_BUTTON, self.on_reload)

        self.edit_button = wx.Button(self, label="Edit Config")
        self.edit_button.Bind(wx.EVT_BUTTON, self.on_edit_config)

        grid = wx.GridBagSizer(4, 4)

        grid.Add(ipg_box_sizer, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
                 border=10)
        grid.Add(magnum_box_sizer, pos=(0, 1), flag=wx.TOP, border=10)
        grid.Add(phabrix_box_sizer, pos=(0, 2), flag=wx.TOP, border=10)
        grid.Add(self.start_button, pos=(0, 3), flag=wx.TOP | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL,
                 border=10)
        grid.Add(self.toggle_button, pos=(0, 4), flag=wx.TOP | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL,
                 border=10)
        grid.Add(self.edit_button, pos=(0, 5), flag=wx.TOP | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL,
                 border=10)
        grid.Add(self.reload_button, pos=(0, 6), flag=wx.TOP | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL,
                 border=10)
        main_box_sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 5)

        # List Control
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, 'Result', width=60)
        self.list_ctrl.InsertColumn(1, '#', width=40)
        self.list_ctrl.InsertColumn(2, 'IPG Out Tested', width=100)
        self.list_ctrl.InsertColumn(3, 'Format', width=70)
        self.list_ctrl.InsertColumn(4, 'OutputAV', width=100)
        self.list_ctrl.InsertColumn(5, 'Vertical Offset', width=100)
        self.list_ctrl.InsertColumn(6, 'AES', width=50)
        self.list_ctrl.InsertColumn(7, 'DELAY RIGHT', width=100)
        self.list_ctrl.InsertColumn(8, 'DELAY LEFT', width=100)
        self.list_ctrl.InsertColumn(9, 'Min', width=50)
        self.list_ctrl.InsertColumn(10, 'Max', width=50)

        # Text Control
        self.scrolled_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        self.populate_text_control(self)
        self.scrolled_text.Hide()

        # Image list
        self.image_list = wx.ImageList(16, 16)

        # Load your own img and add them to the ImageList
        self.img_pass = wx.Image('img/pass.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.img_fail = wx.Image('img/fail.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.img_neutral = wx.Image('img/question.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        self.idx_pass = self.image_list.Add(self.img_pass)
        self.idx_fail = self.image_list.Add(self.img_fail)
        self.idx_neutral = self.image_list.Add(self.img_neutral)
        self.list_ctrl.AssignImageList(self.image_list, wx.IMAGE_LIST_SMALL)

        self.main_vbox.Add(main_box_sizer, flag=wx.RIGHT | wx.ALIGN_CENTER)
        self.main_vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        self.main_vbox.Add(self.scrolled_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(self.main_vbox)
        self.test_in_progress = False

    def on_start(self, event):
        # saving to configuration
        self.wxconfig.Write("/magnumIP", self.magnum_input.GetValue())
        self.wxconfig.Write("/port", self.port_input.GetValue())
        self.wxconfig.Write("/phabrixIP", self.phabrixIP_input.GetValue())
        self.wxconfig.Write("/ipgIP", self.ipg_ip_input.GetValue())

        # Setting up UI
        self.list_ctrl.DeleteAllItems()
        self.reload_button.Disable()
        if self.scrolled_text.IsShown():
            self.scrolled_text.Hide()
            self.list_ctrl.Show()
        self.main_vbox.Layout()

        # Starting the thread
        animate_thread = threading.Thread(target=self.animate_test_progress)
        animate_thread.start()

        start_thread = threading.Thread(target=self.on_start_thread)
        start_thread.start()

    def animate_test_progress(self):
        self.test_in_progress = True
        while self.test_in_progress:
            for x in range(6):
                self.parent.SetStatusText("Test in progress" + "." * (x + 1))
                time.sleep(0.5)
        self.parent.SetStatusText("Test Complete :)")
        self.reload_button.Enable()

    def on_start_thread(self):

        # for i in range(5):
        #     index = self.list_ctrl.InsertItem(i, '')
        #     self.list_ctrl.SetItem(index, 1, 'Item %d' % i)
        #     self.list_ctrl.SetItem(index, 2, 'Image %d' % i)  # Set the image in the third column
        #     if i%2 == 0:
        #         self.list_ctrl.SetItemImage(index, self.idx_neutral)
        #     time.sleep(1)

        # Getting the UI configuration
        MAGNUM_IP = self.magnum_input.GetValue()
        INTERFACE_PORT = self.port_input.GetValue()
        PHABRIXIP = self.phabrixIP_input.GetValue()
        IPG_IP = self.ipg_ip_input.GetValue()

        http = ahttp.start()  # Starting http to connect to the webpage
        phabrix = phabrixlib.Phabrix(IP=PHABRIXIP, port=2100, timeout=2.0,
                                     encoding='utf8')  # Connecting to the phabrix

        port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port.connect((MAGNUM_IP, int(INTERFACE_PORT)))  # Connecting to magnum interface for routing
        port.settimeout(3)

        # Setting the phabrix out to AV delay
        phabrix.SetValue(ID="COM_GEN1_PATTERN_SEL", value=3)

        # setting the ipg output
        for out in self.config.OUTS:
            cmd = '.SVABCDEFGHIJKLMNOPQRS%03d,%03d\r' % (1, out)
            port.send(cmd.encode())

            # Setting the standard on phabrix
            for n, format in enumerate(self.config.PHABRIX_VALUE):
                if format[0] == "INVALID" or format[1] == "INVALID" or format[2] == "INVALID":
                    continue

                phabrix.SetValue(ID="COM_GEN1_LINK_TYPE", value=format[0])  # HD eg
                phabrix.SetValue(ID="COM_GEN1_LINES", value=format[1])  # 720p eg
                phabrix.SetValue(ID="COM_GEN1_RATE", value=format[2])  # 59.94 eg

                # Looping the value between 0 and 1 (Bypass and timestamp)
                for sync in self.config.OUTPUT_AV_SYNC:
                    http.set_cfgjson(IPG_IP, {f'816.{out - 1}@i': sync})
                    # Setting vertical offset
                    for v in self.config.VERTICAL_OFFSET:
                        http.set_cfgjson(IPG_IP, {f'159.{out - 1}@i': v})
                        # Setting the AES67 IP Output packet time
                        for aes67 in self.config.AES67:
                            http.set_cfgjson(IPG_IP, {'638@i': aes67})
                            # Sleeping after setting up all the devices
                            time.sleep(self.config.DELAY)

                            # Setting values complete
                            # Checking if all the values are set
                            # Declaring the data to be set
                            aes = ''
                            outputAV = ''
                            outputAV_value = http.get_cfgjson(IPG_IP, [f'816.{out - 1}@i']).result[f'816.{out - 1}@i']
                            if outputAV_value == 0:
                                outputAV = "Bypass"
                            elif outputAV_value == 1:
                                outputAV = "Timestamp"
                            voffset = http.get_cfgjson(IPG_IP, [f'159.{out - 1}@i']).result[f'159.{out - 1}@i']

                            aesValue = http.get_cfgjson(IPG_IP, ['638@i']).result['638@i']
                            if aesValue == 0:
                                aes = "125us"
                            elif aesValue == 1:
                                aes = "1ms"

                            format = phabrix.get_text(560)  # Format on phabrix
                            # Now reading the left and right value
                            left_measurement = phabrix.GetText(2402)
                            right_measurement = phabrix.GetText(2403)

                            # Checking if it passed or failed
                            EXP = self.config.EXPECTED.get(
                                self.config.FORMATS[n][1] + self.config.FORMATS[n][2] + str(outputAV) + str(voffset)
                                + str(aes), ['?', '?'])

                            # Checking if the result was not found in text file
                            if EXP[0] != '?' and EXP[1] != '?':
                                if EXP[0] <= float(left_measurement[:-2]) <= EXP[1] and EXP[0] <= float(
                                        right_measurement[:-2]) <= EXP[1]:
                                    result = "Pass"
                                else:
                                    result = "Fail"
                            else:
                                result = '?'

                            i = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(),
                                                          '')
                            if result == 'Pass':
                                self.list_ctrl.SetItemImage(i, self.idx_pass)
                            elif result == 'Fail':
                                self.list_ctrl.SetItemImage(i, self.idx_fail)
                            elif result == '?':
                                self.list_ctrl.SetItemImage(i, self.idx_neutral)
                            self.list_ctrl.SetItem(i, 1, str(i + 1))
                            self.list_ctrl.SetItem(i, 2, str(out))
                            self.list_ctrl.SetItem(i, 3, format)
                            self.list_ctrl.SetItem(i, 4, outputAV)
                            self.list_ctrl.SetItem(i, 5, str(voffset))
                            self.list_ctrl.SetItem(i, 6, aes)
                            self.list_ctrl.SetItem(i, 7, right_measurement)
                            self.list_ctrl.SetItem(i, 8, left_measurement)
                            self.list_ctrl.SetItem(i, 9, str(EXP[0]))
                            self.list_ctrl.SetItem(i, 10, str(EXP[1]))

                            self.config.test_result.append(
                                [len(self.config.test_result) + 1, out, format, outputAV, voffset, aes,
                                 right_measurement, left_measurement, EXP[0], EXP[1], result])
        phabrix.close()
        self.test_in_progress = False
        print(self.config.test_result)

    def on_reload(self, event):
        self.config.load_config()
        self.config.load_expected()
        self.populate_text_control(self)

    def on_edit_config(self, event):
        file_path = "Config/testconfig.txt"
        text_editor_command = "notepad"

        def run_code():
            os.system(f"{text_editor_command} {file_path}")

        edit_thread = threading.Thread(target=run_code)
        edit_thread.start()

    def on_edit_expected(self, event):
        file_path = "Config/expected.txt"
        text_editor_command = "notepad"

        def run_code():
            os.system(f"{text_editor_command} {file_path}")

        edit_thread = threading.Thread(target=run_code)
        edit_thread.start()

    def on_toggle_view(self, event):
        if self.list_ctrl.IsShown():
            self.list_ctrl.Hide()
            self.scrolled_text.Show()
            self.parent.SetStatusText("Config view")
        else:
            self.scrolled_text.Hide()
            self.list_ctrl.Show()
            self.parent.SetStatusText("Output view")
        self.main_vbox.Layout()

    def populate_text_control(self, event):
        self.scrolled_text.Clear()
        self.scrolled_text.write(f"Time delay between each test: \n {self.config.DELAY}")

        self.scrolled_text.write("\n\n\nFormats being tested:\n")
        for format in self.config.FORMATS:
            self.scrolled_text.write(f"{format[0]} {format[1]} {format[2]}\n")

        self.scrolled_text.write("\n\nIPG outputs being tested:\n")
        for output in self.config.OUTS:
            self.scrolled_text.write(str(output) + "\n")

        self.scrolled_text.write("\n\nOutput AV sync modes selected for testing:\n")
        for mode in self.config.OUTPUT_AV_SYNC:
            if mode == 0:
                self.scrolled_text.write("Bypass \n")
            if mode == 1:
                self.scrolled_text.write("Timestamp \n")

        self.scrolled_text.write("\n\nVertical offset:\n")
        for offset in self.config.VERTICAL_OFFSET:
            self.scrolled_text.write(str(offset) + "\n")

        self.scrolled_text.write("\n\nAES67 IP output Packet time:\n")
        for aes in self.config.AES67:
            if aes == 0:
                self.scrolled_text.write("125us \n")
            if aes == 1:
                self.scrolled_text.write("1ms \n")

    def save_as_excel(self, event):
        open_path = os.getcwd()
        WILDCARDS = "MS Excel files (*.xlsx)|*.xlsx"
        fileDialog = wx.FileDialog(self,
                                   message="Save as Excel",
                                   wildcard=WILDCARDS,
                                   defaultDir=open_path,
                                   style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return
        save_filename = fileDialog.GetPath()
        self.config.save_config(save_filename)
        fileDialog.Destroy()


if __name__ == '__main__':
    import Main

    Main.Main()
