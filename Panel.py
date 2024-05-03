import socket
import threading
import time

import ahttp
import phabrixlib
import wx
import Config
import WebpageMethods

class Panel(wx.Panel):
    def __init__(self, parent, config):

        wx.Panel.__init__(self, parent)
        self.config = config
        self.config_data = Config

        self.main_vbox = wx.BoxSizer(wx.VERTICAL)

        main_box = wx.StaticBox(self, label='Test Configuration')
        main_box.SetFont(wx.Font(wx.FontInfo(12).Bold()))
        main_box_sizer = wx.StaticBoxSizer(main_box)

        # Making IPG selection sizer
        ipg_box = wx.StaticBox(self, label='IPG and IP Address')
        ipg_box_sizer = wx.StaticBoxSizer(ipg_box)
        ipgs = ['570 A9', '570 X-19', 'evIPG-12G', 'evIPG-3G']
        self.select_ipg = wx.Choice(self, choices=ipgs)
        self.select_ipg.SetStringSelection(config.Read("/device", defaultVal="570 A9"))
        self.ipg_ip_input = wx.TextCtrl(self, size=(100, -1), value=config.Read('/magnumIP', defaultVal=""))
        ipg_box_sizer.Add(self.select_ipg, 0, wx.ALL, 5)
        ipg_box_sizer.Add(self.ipg_ip_input, 0, wx.EXPAND | wx.ALL, 5)

        # Making Magnum and port selection sizer
        magnum_box = wx.StaticBox(self, label="Magnum IP and Interface Port")
        magnum_box_sizer = wx.StaticBoxSizer(magnum_box)
        self.magnum_input = wx.TextCtrl(self, size=(100, -1), value=config.Read('/magnumIP', defaultVal=""))
        self.port_input = wx.TextCtrl(self, size=(50, -1), value=config.Read('/port', defaultVal=""))
        magnum_box_sizer.Add(self.magnum_input, 0, wx.ALL, 5)
        magnum_box_sizer.Add(self.port_input, 0, wx.EXPAND | wx.ALL, 5)

        # Making phabrix box sizer
        phabrix_box = wx.StaticBox(self, label="Phabrix IP Address")
        phabrix_box_sizer = wx.StaticBoxSizer(phabrix_box)
        self.phabrixIP_input = wx.TextCtrl(self, size=(90, -1), value=config.Read('/phabrixIP', defaultVal=""))
        phabrix_box_sizer.Add(self.phabrixIP_input, 0, wx.EXPAND | wx.ALL, 5)

        self.start_button = wx.Button(self, label="Start")
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)
        self.grid = wx.GridBagSizer(4, 4)

        self.grid.Add(ipg_box_sizer, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
                      border=10)
        self.grid.Add(magnum_box_sizer, pos=(0, 1), flag=wx.TOP, border=10)
        self.grid.Add(phabrix_box_sizer, pos=(0, 2), flag=wx.TOP, border=10)
        self.grid.Add(self.start_button, pos=(0, 3), flag=wx.TOP | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL,
                      border=10)
        main_box_sizer.Add(self.grid, 0, wx.EXPAND | wx.ALL, 5)

        # List Control
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, 'Type', width=40)
        self.list_ctrl.InsertColumn(1, 'Format', width=100)
        self.list_ctrl.InsertColumn(2, 'Frame Rate', width=100)
        self.list_ctrl.InsertColumn(3, 'OutputAV', width=100)
        self.list_ctrl.InsertColumn(4, 'Vertical Offset', width=100)
        self.list_ctrl.InsertColumn(5, 'AES', width=100)
        self.list_ctrl.InsertColumn(6, 'DELAY RIGHT', width=100)
        self.list_ctrl.InsertColumn(7, 'DELAY LEFT', width=100)

        self.main_vbox.Add(main_box_sizer, flag=wx.RIGHT | wx.ALIGN_CENTER)
        self.main_vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(self.main_vbox)


    def on_start(self, event):
        # saving to configuration
        self.config.Write("/device", self.select_ipg.GetStringSelection())
        self.config.Write("/port", self.port_input.GetValue())
        self.config.Write("/phabrixIP", self.phabrixIP_input.GetValue())
        start_thread = threading.Thread(target=self.on_start_thread)
        start_thread.start()

    def on_start_thread(self):
        # Getting the UI configuration
        INTERFACE_PORT = self.port_input.GetValue()
        PHABRIXIP = self.phabrixIP_input.GetValue()
        DEVICE = self.select_ipg.GetStringSelection()
        http = ahttp.start()  # Starting http to connect to the webpage
        phabrix = phabrixlib.Phabrix(IP='172.17.223.162', port=2100, timeout=2.0,
                                     encoding='utf8')  # Connecting to the phabrix

        port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port.connect(('172.17.223.175', 4012))  # Connecting to magnum interface for routing
        port.settimeout(3)
        print('CONNECTED TO MAGNUM INTERFACE')

        # Setting the phabrix out to AV delay
        phabrix.SetValue(ID="COM_GEN1_PATTERN_SEL", value=3)

        # Setting the standard on phabrix
        for x in range(3):
            if x == 0:
                phabrix.SetValue(ID="COM_GEN1_LINK_TYPE", value=1)  # HD 720p59.94
                time.sleep(0.5)
                phabrix.SetValue(ID="COM_GEN1_LINES", value=2)  # 720p
                time.sleep(0.5)
                phabrix.SetValue(ID="COM_GEN1_RATE", value=6)  # 59.94
                cmd = '.SVABCDEFGHIJKLMNOPQRS%03d,%03d\r' % (1, 3)
                port.send(cmd.encode())
            elif x == 1:
                phabrix.SetValue(ID="COM_GEN1_LINK_TYPE", value=1)  # HD 1080i59.94
                time.sleep(0.5)
                phabrix.SetValue(ID="COM_GEN1_LINES", value=4)  # 1080i
                time.sleep(0.5)
                phabrix.SetValue(ID="COM_GEN1_RATE", value=6)  # 59.94
                cmd = '.SVABCDEFGHIJKLMNOPQRS%03d,%03d\r' % (1, 7)
                port.send(cmd.encode())
            elif x == 2:
                phabrix.SetValue(ID="COM_GEN1_LINK_TYPE", value=3)  # 3G 1080p59.94
                time.sleep(0.5)
                phabrix.SetValue(ID="COM_GEN1_LINES", value=6)
                time.sleep(0.5)
                phabrix.SetValue(ID="COM_GEN1_RATE", value=6)
                cmd = '.SVABCDEFGHIJKLMNOPQRS%03d,%03d\r' % (1, 13)
                port.send(cmd.encode())
            # Looping the value between 0 and 1 (Bypass and timestamp)
            for m in range(2):
                WebpageMethods.set_device_setting(http, {'816.0@i': m})
                # Setting vertical offset
                for n in range(2):
                    if n == 0:
                        WebpageMethods.set_device_setting(http, {'159.0@i': 0})
                    if n == 1:
                        WebpageMethods.set_device_setting(http, {'159.0@i': 4})
                    # Setting the AES67IP
                    for o in range(2):
                        WebpageMethods.set_device_setting(http, {'638@i': o})
                        # Checking if all the values are set
                        outputAV = WebpageMethods.get_device_setting(http, ['816.0@i'])['816.0@i']
                        voffset = WebpageMethods.get_device_setting(http, ['159.0@i'])['159.0@i']
                        aes = WebpageMethods.get_device_setting(http, ['638@i'])['638@i']
                        format = f"{phabrix.get_text(560)} "
                        # Setting complete now reading the left and right value
                        time.sleep(3)
                        left_measurement = phabrix.GetText(2402)
                        right_measurement = phabrix.GetText(2403)

                        print(f"Values are OutputAV: {outputAV} Vertical Offset: {voffset} AES: {aes}")
                        print(f"Format on phabrix: {format}")
                        print(f"Phabrix Delay Right {right_measurement} Left {left_measurement}\n\n")

        phabrix.close()
