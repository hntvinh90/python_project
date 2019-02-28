import wx
import os
FONTSIZE = 10
class TextDocPrintout(wx.Printout):
    def __init__(self, text, title, margins):
        wx.Printout.__init__(self, title)
        self.lines = text.split('\n')
        self.margins = margins
    def HasPage(self, page):
        return page <= self.numPages
    def GetPageInfo(self):
        return (1, self.numPages, 1, self.numPages)
    def CalculateScale(self, dc):
        ppiPrinterX, ppiPrinterY = self.GetPPIPrinter()
        ppiScreenX, ppiScreenY = self.GetPPIScreen()
        logScale = float(ppiPrinterX)/float(ppiScreenX)
        pw, ph = self.GetPageSizePixels()
        dw, dh = dc.GetSize()
        scale = logScale * float(dw)/float(pw)
        dc.SetUserScale(scale, scale)
        self.logUnitsMM = float(ppiPrinterX)/(logScale*25.4)
    def CalculateLayout(self, dc):
        topLeft, bottomRight = self.margins
        dw, dh = dc.GetSize()
        self.x1 = topLeft.x * self.logUnitsMM
        self.y1 = topLeft.y * self.logUnitsMM
        self.x2 = (dc.DeviceToLogicalXRel(dw) - bottomRight.x * self.logUnitsMM)
        self.y2 = (dc.DeviceToLogicalYRel(dh) - bottomRight.y * self.logUnitsMM)
        self.pageHeight = self.y2 - self.y1 - 2*self.logUnitsMM
        font = wx.Font(FONTSIZE, wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        self.lineHeight = dc.GetCharHeight()
        self.linesPerPage = int(self.pageHeight/self.lineHeight)
    def OnPreparePrinting(self):
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)
        self.numPages = len(self.lines) / self.linesPerPage
        if len(self.lines) % self.linesPerPage != 0:
            self.numPages += 1
    def OnPrintPage(self, page):
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)
        dc.SetPen(wx.Pen("black", 0))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        r = wx.Rect(self.x1, self.y1, self.x2, self.y2)
        dc.DrawRectangle(r)
        dc.SetClippingRegion(r)
        line = (page-1) * self.linesPerPage
        x = self.x1 + self.logUnitsMM
        y = self.y1 + self.logUnitsMM
        while line < (page * self.linesPerPage):
            dc.DrawText(self.lines[line], x, y)
            y += self.lineHeight
            line += 1
            if line >= len(self.lines):
                break
        return True
class PrintFrameworkSample(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size=(640, 480),
        title="Print Framework Sample")
        self.CreateStatusBar()
        self.tc = wx.TextCtrl(self, -1, "",
        style=wx.TE_MULTILINE|wx.TE_DONTWRAP)
        self.tc.SetFont(wx.Font(FONTSIZE, wx.TELETYPE, wx.NORMAL, wx.NORMAL))
        filename = os.path.join(os.path.dirname(__file__), "text")
        self.tc.SetValue(open(filename, encoding='utf-8').read())
        self.tc.Bind(wx.EVT_SET_FOCUS, self.OnClearSelection)
        wx.CallAfter(self.tc.SetInsertionPoint, 0)
        menu = wx.Menu()
        item = menu.Append(-1, "Page Setup...\tF5",
        "Set up page margins and etc.")
        self.Bind(wx.EVT_MENU, self.OnPageSetup, item)
        item = menu.Append(-1, "Print Setup...\tF6",
        "Set up the printer options, etc.")
        self.Bind(wx.EVT_MENU, self.OnPrintSetup, item)
        item = menu.Append(-1, "Print Preview...\tF7",
        "View the printout on-screen")
        self.Bind(wx.EVT_MENU, self.OnPrintPreview, item)
        item = menu.Append(-1, "Print...\tF8", "Print the document")
        self.Bind(wx.EVT_MENU, self.OnPrint, item)
        menu.AppendSeparator()
        item = menu.Append(-1, "E&xit", "Close this application")
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")
        self.SetMenuBar(menubar)
        self.pdata = wx.PrintData()
        self.pdata.SetPaperId(wx.PAPER_LETTER)
        self.pdata.SetOrientation(wx.PORTRAIT)
        self.margins = (wx.Point(15,15), wx.Point(15,15))
    def OnExit(self, evt):
        self.Close()
    def OnClearSelection(self, evt):
        evt.Skip()
        wx.CallAfter(self.tc.SetInsertionPoint,
        self.tc.GetInsertionPoint())
    def OnPageSetup(self, evt):
        data = wx.PageSetupDialogData()
        data.SetPrintData(self.pdata)
        data.SetDefaultMinMargins(True)
        data.SetMarginTopLeft(self.margins[0])
        data.SetMarginBottomRight(self.margins[1])
        dlg = wx.PageSetupDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPageSetupData()
            self.pdata = wx.PrintData(data.GetPrintData())
            self.pdata.SetPaperId(data.GetPaperId())
            self.margins = (data.GetMarginTopLeft(),
            data.GetMarginBottomRight())
        dlg.Destroy()
    def OnPrintSetup(self, evt):
        data = wx.PrintDialogData(self.pdata)
        dlg = wx.PrintDialog(self, data)
        dlg.GetPrintDialogData().SetSetupDialog(True)
        dlg.ShowModal();
        data = dlg.GetPrintDialogData()
        self.pdata = wx.PrintData(data.GetPrintData())
        dlg.Destroy()
    def OnPrintPreview(self, evt):
        data = wx.PrintDialogData(self.pdata)
        text = self.tc.GetValue()
        printout1 = TextDocPrintout(text, "title", self.margins)
        printout2 = TextDocPrintout(text, "title", self.margins)
        preview = wx.PrintPreview(printout1, printout2, data)
        if not preview.IsOk():
            wx.MessageBox("Unable to create PrintPreview!", "Error")
        else:
            frame = wx.PreviewFrame(preview, self, "Print Preview",
            pos=self.GetPosition(),
            size=self.GetSize())
            frame.Initialize()
            frame.Show()
    def OnPrint(self, evt):
        data = wx.PrintDialogData(self.pdata)
        printer = wx.Printer(data)
        text = self.tc.GetValue()
        printout = TextDocPrintout(text, "title", self.margins)
        useSetupDialog = True
        if not printer.Print(self, printout, useSetupDialog) \
        and printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox(
            "There was a problem printing.\n"
            "Perhaps your current printer is not set correctly?",
            "Printing Error", wx.OK)
        else:
            data = printer.GetPrintDialogData()
            self.pdata = wx.PrintData(data.GetPrintData()) # force a copy
        printout.Destroy()
app = wx.PySimpleApp()
frm = PrintFrameworkSample()
frm.Show()
app.MainLoop()