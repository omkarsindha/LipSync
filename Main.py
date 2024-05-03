import os
import wx
import wx.adv
import threading
from Panel import Panel

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        self.config = wx.Config("LipSync")
        self.panel = Panel(self, config=self.config)

        self.Center()
        self.SetMinSize((400, 400))

        menubar = wx.MenuBar()
        helpMenu = wx.Menu()
        helpMenu.Append(wx.ID_ABOUT, "&About")
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        self.SetMenuBar(menubar)

        self.CreateStatusBar(number=2, style=wx.STB_DEFAULT_STYLE)
        self.SetStatusWidths([-1, 100])
        self.SetStatusText("This is the status bar", 0)

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


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title="Lip Sync Automation", size=(800, 500))
    frame.Show()
    app.MainLoop()
