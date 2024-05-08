import os
import wx
import wx.adv
from Config import Config
from Panel import Panel


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        self.Center()
        self.SetMinSize((400, 400))
        menubar = wx.MenuBar()
        helpMenu = wx.Menu()
        helpMenu.Append(wx.ID_ABOUT, "&About")
        menubar.Append(helpMenu, "&Help")
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        self.SetMenuBar(menubar)

        self.CreateStatusBar(number=2, style=wx.STB_DEFAULT_STYLE)
        self.SetStatusWidths([-1, 100])
        self.SetStatusText("Output view", 0)

        self.wxconfig = wx.Config("LipSync")
        self.config = Config()
        self.panel = Panel(self, wxconfig=self.wxconfig, config=self.config)

    def on_about(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetName('Switching UI')
        info.SetDescription(
            "Python version 3.11.7\n" +
            "Powered by wxPython %s\n" % (wx.version()) +
            "Running on %s\n\n" % (wx.GetOsDescription()) +
            "Process ID = %s\n" % (os.getpid()))
        info.SetWebSite("www.evertz.com", "Evertz")
        info.AddDeveloper("Omkarsinh Sindha")
        wx.adv.AboutBox(info)


def Main():
    app = wx.App()
    frame = MainFrame(None, title="Lip Sync Automation", size=(850, 500))
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    Main()
