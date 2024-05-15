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

        self.wxconfig = wx.Config("LipSync")
        self.config = Config()
        self.panel = Panel(self, wxconfig=self.wxconfig, config=self.config)

        menubar = wx.MenuBar()
        helpMenu = wx.Menu()
        saveMenu = wx.Menu()
        helpMenu.Append(wx.ID_ABOUT, "&About")
        helpMenu.Append(wx.ID_FILE1, "How to Setup")
        helpMenu.Append(wx.ID_FILE2, "How to Navigate")
        menubar.Append(helpMenu, "&Help")
        saveMenu.Append(wx.ID_FILE3, "Save as excel")
        menubar.Append(saveMenu, "&Save")

        #  Binding the menu options to their methods
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_how_to_setup, id=wx.ID_FILE1)
        self.Bind(wx.EVT_MENU, self.on_how_to_navigate, id=wx.ID_FILE2)
        self.Bind(wx.EVT_MENU, self.panel.save_as_excel, id=wx.ID_FILE3)
        self.SetMenuBar(menubar)

        self.CreateStatusBar(number=2, style=wx.STB_DEFAULT_STYLE)
        self.SetStatusWidths([-1, 100])
        self.SetStatusText("Output view", 0)

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

    def on_how_to_setup(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetName('How to setup this automation?')
        info.SetDescription(
            "Step 1: Make an interface with all the IPG outputs as source and Phabrix SDI input as destination\n\n" +
            "Step 2: Route Phabrix Output to all IPG inputs\n\n" +
            "Step 3: Fill the test config file as per test requirements\n\n" +
            "Step 4: Fill in the interface port number in the UI"
        )
        wx.adv.AboutBox(info)

    def on_how_to_navigate(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetName('How do I navigate through this automation?')
        info.SetDescription(
            "Start: Simply just starts the automation\n\n" +
            "Reload: Goes through the file again to change config\n\n" +
            "Toggle: Lets you can check the config that you wrote in the text file via UI, basically changes between the Output and Config views"
        )
        wx.adv.AboutBox(info)

def Main():
    app = wx.App()
    frame = MainFrame(None, title="Lip Sync Automation", size=(850, 500))
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    Main()
