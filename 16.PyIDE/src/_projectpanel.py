#!/usr/bin/python

""""""

import wx, os, shutil, base64
from PIL import Image
import img
from myLibs import isThread

ROOT = 'root'
FOLDER = 'folder'
EXEFILE = 'exe file'
PYFILE = 'pyfile'
PNGFILE = 'png file'
ICONFILE = 'icon file'
UNKNOWNFILE = 'unknown file'

I = img.Image


class ProjectPanel(wx.Panel):
    def __init__(self, parent, grandparent):
        wx.Panel.__init__(self, parent)
        self.parent = parent # Tab of left notebook
        self.grandparent = grandparent #mainframe
        self.preferencesdirectory = self.parent.setting.HOMEPATH
        self.newbtn = wx.Button(self, -1, 'New', size=(60, 25))
        self.newbtn.Bind(wx.EVT_BUTTON, self.onNew)
        self.openbtn = wx.Button(self, -1, 'Open', size=(60, 25))
        self.openbtn.Bind(wx.EVT_BUTTON, self.onOpen)
        self.reloadbtn = wx.Button(self, -1, 'Reload', size=(60, 25))
        self.reloadbtn.Bind(wx.EVT_BUTTON, self.onReload)
        self.tree = ProjectTree(self, grandparent, '')
        self.loadTreeFromPref()
        self.OnSize()

    def onNew(self, event):
        path = NewProjectDialog(self.grandparent).path

    def onOpen(self, event):
        path = wx.DirSelector('Choose Folder ...')
        if path != '':
            self.tree.listExpandedItems = []
            self.tree.reloadTree(path)

    def onReload(self, event):
        if self.tree.path is not '' and os.path.exists(self.tree.path):
            self.tree.reloadTree(self.tree.path)

    def loadTreeFromPref(self):
        path = os.path.join(self.preferencesdirectory, '.project.dat')
        if os.path.exists(path):
            with open(path, 'r') as f:
                project = f.readline()
                if os.path.exists(project):
                    # Load expanded items
                    path = os.path.join(self.preferencesdirectory, '.project.expandeditems.dat')
                    if os.path.exists(path):
                        with open(path, 'r') as f:
                            self.tree.listExpandedItems = []
                            for item in f.read().split('\n'):
                                if item not in self.tree.listExpandedItems:
                                    self.tree.listExpandedItems.append(item)
                    #####
                    self.tree.reloadTree(project)

    def OnSize(self):
        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        #bottomsizer.Add((1, 1), 1, wx.EXPAND)
        bottomsizer.Add(self.newbtn, 1, wx.EXPAND)
        bottomsizer.Add(self.openbtn, 1, wx.EXPAND)
        bottomsizer.Add(self.reloadbtn, 1, wx.EXPAND)
        #bottomsizer.Add((1, 1), 1, wx.EXPAND)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 1, wx.EXPAND)
        sizer.Add(bottomsizer, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def memoryExpandedItems(self):
        with open(os.path.join(self.preferencesdirectory, '.project.dat'), 'w') as f:
            f.write(self.tree.path)
        with open(os.path.join(self.preferencesdirectory, '.project.expandeditems.dat'), 'w') as f:
            f.write('\n'.join(self.tree.listExpandedItems))


class ProjectTree(wx.TreeCtrl):
    def __init__(self, parent, grandparent, path):
        wx.TreeCtrl.__init__(self, parent)
        self.parent = parent # Project Panel
        self.grandparent = grandparent #mainframe
        self.path = path
        self.listExpandedItems = []
        self.listItem = {}

        imagelist = wx.ImageList(16, 16)
        imagelist.Add(I['folder'].GetBitmap())
        imagelist.Add(I['folderopen'].GetBitmap())
        imagelist.Add(I['exe'].GetBitmap())
        imagelist.Add(I['py'].GetBitmap())
        imagelist.Add(I['png'].GetBitmap())
        imagelist.Add(I['icon'].GetBitmap())
        imagelist.Add(I['unknown'].GetBitmap())
        imagelist.Add(I['root'].GetBitmap())
        self.AssignImageList(imagelist)

        #self.loadTree()

        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onRightClick)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onExpanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.onCollapsed)
        
        self.SetBackgroundColour(self.parent.GetBackgroundColour())

    def loadTree(self):
        project = self.loadDir(self.path)
        self.root = item = self.AddRoot(os.path.basename(project[0]), 7)
        #self.SetItemImage(item, 1, wx.TreeItemIcon_Expanded)
        self.listItem[item] = [project[0], ROOT]
        project[0] = item
        self.addTreeItem(project)
        for item in self.listItem.keys():
            if self.GetItemText(item) in self.listExpandedItems:
                self.Expand(item)

    def loadDir(self, path):
        #project += os.listdir(project[0])
        folder = [path]
        exefile = []
        pyfile =[]
        pngfile = []
        iconfile = []
        unknownfile = []
        ls = os.listdir(folder[0])
        #print(ls)
        for i in range(len(ls)):
            link = os.path.join(folder[0], ls[i])
            if os.path.isdir(link):
                folder.append(self.loadDir(link))
            else:
                if 'exe.' == ls[i][::-1][:4]:
                    exefile.append(ls[i])
                elif 'yp.' == ls[i][::-1][:3]:
                    pyfile.append(ls[i])
                elif 'gnp.' == ls[i][::-1][:4]:
                    pngfile.append(ls[i])
                elif 'oci.' == ls[i][::-1][:4]:
                    iconfile.append(ls[i])
                else:
                    unknownfile.append(ls[i])
        return folder + exefile + pyfile + pngfile + iconfile + unknownfile

    def addTreeItem(self, project):
        for i in range(1, len(project)):
            if type(project[i]) == str:
                item = self.AppendItem(project[0], project[i])
                if 'exe.' == project[i][::-1][:4]:
                    filetype = EXEFILE
                    self.SetItemImage(item, 2)
                elif 'yp.' == project[i][::-1][:3]:
                    filetype = PYFILE
                    self.SetItemImage(item, 3)
                elif 'gnp.' in project[i][::-1][:4]:
                    filetype = PNGFILE
                    self.SetItemImage(item, 4)
                elif 'oci.' in project[i][::-1][:4]:
                    filetype = ICONFILE
                    self.SetItemImage(item, 5)
                else:
                    filetype = UNKNOWNFILE
                    self.SetItemImage(item, 6)
                self.listItem[item] = [os.path.join(self.listItem[project[0]][0], project[i]), filetype]
            else:
                item = self.AppendItem(project[0], os.path.basename(project[i][0]), 0)
                self.SetItemImage(item, 1, wx.TreeItemIcon_Expanded)
                self.listItem[item] = [project[i][0], FOLDER]
                project[i][0] = item
                self.addTreeItem(project[i])

    def onDoubleClick(self, event):
        item = self.GetSelection()
        if item:
            if self.listItem[item][1] in [FOLDER, ROOT]:
                self.Toggle(item)
            elif self.listItem[item][1] == PYFILE:
                self.grandparent.textpanel.open(self.listItem[item][0])
                try:
                    self.grandparent.menubar.openrecent.update(self.listItem[item][0])
                except: pass
            '''
            elif self.listItem[item][1] == EXEFILE:
                self.onExeFile(item)
            #'''

    def onRightClick(self, event):
        item = event.GetItem()
        if item:
            self.SelectItem(item, True)
            if self.listItem[item][1] == ROOT:
                self.PopupMenu(RootMenu(self, item), event.GetPoint())
            elif self.listItem[item][1] == FOLDER:
                self.PopupMenu(FolderMenu(self, item), event.GetPoint())
            elif self.listItem[item][1] == EXEFILE:
                self.PopupMenu(ExeMenu(self, item), event.GetPoint())
            elif self.listItem[item][1] == PYFILE:
                self.PopupMenu(PyMenu(self, item), event.GetPoint())
            elif self.listItem[item][1] == PNGFILE:
                self.PopupMenu(PngMenu(self, item), event.GetPoint())
            elif self.listItem[item][1] == ICONFILE:
                self.PopupMenu(IconMenu(self, item), event.GetPoint())
            elif self.listItem[item][1] == UNKNOWNFILE:
                self.PopupMenu(UnknownMenu(self, item), event.GetPoint())

    def onExpanded(self, event):
        item = self.GetItemText(event.GetItem())
        if item not in self.listExpandedItems:
            self.listExpandedItems.append(item)

    def onCollapsed(self, event):
        item = self.GetItemText(event.GetItem())
        if item in self.listExpandedItems:
            self.listExpandedItems.remove(item)

    @isThread
    def onExeFile(self, item):
        path = self.listItem[item][0]
        extraCmd = "read -rsp $'Press Enter to continue\n'"
        preCmd = 'cd'
        if self.grandparent.setting.PLATFORM == self.grandparent.setting.IS_WINDOW:
            preCmd += ' /d "%s"' %(os.path.dirname(path))
            extraCmd = "pause"
        else:
            preCmd += ' "%s"' %(os.path.dirname(path))
        command = '(' + preCmd + ' && "%s") || %s' %(os.path.basename(path), extraCmd)
        os.system(command)

    def reloadTree(self, path):
        self.DeleteAllItems()
        self.path = path
        self.listItem = {}
        self.loadTree()
        self.Expand(self.GetRootItem())


class RootMenu(wx.Menu):
    def __init__(self, parent, item):
        wx.Menu.__init__(self)
        self.parent = parent #TreeCtrl
        self.item = item
        parent.Bind(wx.EVT_MENU, self.onNewFolder, self.Append(-1, 'New Folder'))
        self.AppendSeparator()
        parent.Bind(wx.EVT_MENU, self.onNewDjango, self.Append(-1, 'New Django Project'))
        self.AppendSeparator()
        parent.Bind(wx.EVT_MENU, self.onNewPyFile, self.Append(-1, 'New Python File'))
        child, cookie = parent.GetFirstChild(item)
        while child.IsOk():
            if parent.GetItemText(child) == 'img.py':
                break
            child, cookie = parent.GetNextChild(item, cookie)
        else:
            parent.Bind(wx.EVT_MENU, self.onNewImgFile, self.Append(-1, 'New Image File'))
        parent.Bind(wx.EVT_MENU, self.onNewTextFile, self.Append(-1, 'New Text File'))
        self.AppendSeparator()
        parent.Bind(wx.EVT_MENU, self.onToggle, self.Append(-1, 'Toggle'))

    def onNewFolder(self, event):
        name = wx.GetTextFromUser('Your new folder name:', 'New Folder')
        if name != '':
            path = os.path.join(self.parent.listItem[self.item][0], name)
            if os.path.exists(path):
                wx.MessageBox('A folder named "%s" is available.' %(name), 'Attention')
            else:
                os.makedirs(path)
                self.parent.AppendItem(self.item, 'chen vao de expand item')
                self.parent.Expand(self.item)
                self.parent.reloadTree(self.parent.path)
                
    def onNewDjango(self, event):
        name = wx.GetTextFromUser('Your project name:', 'New Django Project')
        if name != '':
            path = self.parent.listItem[self.item][0]
            preCmd = 'cd'
            extraCmd = "read -rsp $'Press Enter to continue\n'"
            admin = os.path.join(self.parent.grandparent.setting.HOMEPATH, 'Lib', 'site-packages', 'django', 'bin', 'django-admin.py')
            python = os.path.join(self.parent.grandparent.setting.HOMEPATH, self.parent.grandparent.setting.PYTHONEXE)
            if self.parent.grandparent.setting.PLATFORM == self.parent.grandparent.setting.IS_WINDOW:
                preCmd += ' /d "%s"' %(path)
                extraCmd = "pause"
            else:
                preCmd += ' "%s"' %(path)
            command = '(%s && "%s" "%s" "%s" "%s") || %s' %(preCmd, python, admin, 'startproject', name, extraCmd)
            os.system(command)
            self.parent.reloadTree(self.parent.path)

    def onNewPyFile(self, event):
        name = wx.GetTextFromUser('Your new python file name:', 'New Python File')
        if name != '':
            name += '.py'
            path = os.path.join(self.parent.listItem[self.item][0], name)
            if os.path.exists(path):
                wx.MessageBox('A python file named "%s" is available.' %(name), 'Attention')
            else:
                with open(path, 'w') as f:
                    f.write(
'''#!/usr/bin/python

""""""

def main():
    return True

if __name__ == '__main__':
    main()
'''
                            )
                self.parent.AppendItem(self.item, 'chen vao de expand item')
                self.parent.Expand(self.item)
                self.parent.reloadTree(self.parent.path)

    def onNewImgFile(self, event):
        path = os.path.join(self.parent.listItem[self.item][0], 'img.py')
        if os.path.exists(path):
                wx.MessageBox('A image python file is available.', 'Attention')
        else:
            with open(path, 'w') as f:
                f.write(
'''#!/usr/bin/python

"""
Use methods: GetImage & GetBitmap & GetIcon
"""

from wx.lib.embeddedimage import PyEmbeddedImage

Image = {

}
'''
                        )
            self.parent.AppendItem(self.item, 'chen vao de expand item')
            self.parent.Expand(self.item)
            self.parent.reloadTree(self.parent.path)

    def onNewTextFile(self, event):
        name = wx.GetTextFromUser('Your new python file name:', 'New Python File')
        if name != '':
            path = os.path.join(self.parent.listItem[self.item][0], name)
            if os.path.exists(path):
                wx.MessageBox('A file named "%s" is available.' %(name), 'Attention')
            else:
                with open(path, 'w') as f:
                    pass
                self.parent.AppendItem(self.item, 'chen vao de expand item')
                self.parent.Expand(self.item)
                self.parent.reloadTree(self.parent.path)

    def onToggle(self, event):
        self.parent.Toggle(self.parent.GetSelection())

class FolderMenu(RootMenu):
    def __init__(self, parent, item):
        RootMenu.__init__(self, parent, item)
        self.AppendSeparator()
        parent.Bind(wx.EVT_MENU, self.onRename, self.Append(-1, 'Rename'))
        parent.Bind(wx.EVT_MENU, self.onDelete, self.Append(-1, 'Delete'))

    def onRename(self, event):
        oldname = self.parent.listItem[self.item][0]
        name = wx.GetTextFromUser('Your new folder name:', 'Rename Folder')
        if name != '':
            newname = os.path.join(os.path.dirname(oldname), name)
            if os.path.exists(newname):
                wx.MessageBox('A folder named "%s" is available.' %(name), 'Attention')
            else:
                old = os.path.basename(oldname)
                if old in self.parent.listExpandedItems:
                    self.parent.listExpandedItems.remove(old)
                    self.parent.listExpandedItems.append(name)
                os.rename(oldname, newname)
                self.parent.reloadTree(self.parent.path)

    def onDelete(self, event):
        if wx.MessageBox('Do you want to delete "%s" folder?'%(self.parent.GetItemText(self.item)), 'Attention', style=wx.YES_NO) == wx.YES:
            path = self.parent.listItem[self.item][0]
            shutil.rmtree(path)
            item = self.parent.GetItemText(self.item)
            if item in self.parent.listExpandedItems:
                self.parent.listExpandedItems.remove(item)
            self.parent.reloadTree(self.parent.path)
    

class FileMenu(wx.Menu):
    def __init__(self, parent, item):
        wx.Menu.__init__(self)
        self.parent = parent
        self.item = item
        parent.Bind(wx.EVT_MENU, self.onRename, self.Append(-1, 'Rename'))
        parent.Bind(wx.EVT_MENU, self.onDelete, self.Append(-1, 'Delete'))

    def onRename(self, event):
        oldname = self.parent.listItem[self.item][0]
        name = wx.GetTextFromUser('Your new file name:', 'Rename File')
        if name != '':
            newname = os.path.join(os.path.dirname(oldname), name) + oldname[::-1][:oldname[::-1].find('.') + 1][::-1]
            if os.path.exists(newname):
                wx.MessageBox('A file named "%s" is available.' %(name), 'Attention')
            else:
                os.rename(oldname, newname)
                self.parent.reloadTree(self.parent.path)

    def onDelete(self, event):
        if wx.MessageBox('Do you want to delete "%s" file?'%(self.parent.GetItemText(self.item)), 'Attention', style=wx.YES_NO) == wx.YES:
            os.remove(self.parent.listItem[self.item][0])
            self.parent.reloadTree(self.parent.path)


class ExeMenu(FileMenu):
    def __init__(self, parent, item):
        FileMenu.__init__(self, parent, item)
        self.InsertSeparator(0)
        parent.Bind(wx.EVT_MENU, self.onRun, self.Insert(0, -1, 'Run'))

    def onRun(self, event):
        self.parent.onExeFile(self.item)


class PyMenu(FileMenu):
    def __init__(self, parent, item):
        FileMenu.__init__(self, parent, item)
        self.InsertSeparator(0)
        parent.Bind(wx.EVT_MENU, self.onCompile, self.Insert(0, -1, 'Compile To Exe'))
        self.InsertSeparator(0)
        parent.Bind(wx.EVT_MENU, self.onRunWithArgs, self.Insert(0, -1, 'Run With Arguments'))
        parent.Bind(wx.EVT_MENU, self.onRun, self.Insert(0, -1, 'Run'))
        parent.Bind(wx.EVT_MENU, self.onOpen, self.Insert(0, -1, 'Open'))

    def onOpen(self, event):
        self.parent.grandparent.textpanel.open(self.parent.listItem[self.item][0])
        try:
            self.parent.grandparent.menubar.openrecent.update(self.parent.listItem[self.item][0])
        except: pass

    def onCompile(self, event):
        CompileDialog(self.parent.grandparent, self.item)

    def onRun(self, event):
        self.parent.grandparent.menubar.runCmd(self.parent.listItem[self.item][0])
        
    def onRunWithArgs(self, event):
        args = wx.GetTextFromUser('Set arguments to run file:', 'Run')
        if args != '':
            self.parent.grandparent.menubar.runCmd(self.parent.listItem[self.item][0], args)


class PngMenu(FileMenu):
    def __init__(self, parent, item):
        FileMenu.__init__(self, parent, item)
        self.InsertSeparator(0)
        parent.Bind(wx.EVT_MENU, self.onConvertToICO, self.Insert(0, -1, 'Convert to ICO'))

    def onConvertToICO(self, event):
        pngfile = self.parent.listItem[self.item][0]
        icofile = pngfile.replace('.png', '.ico')
        if os.path.exists(icofile):
            wx.MessageBox('A named "%s" is available.' %(os.path.basename(icofile)), 'Attention')
        else:
            img = Image.open(pngfile)
            img.save(icofile)
            self.parent.reloadTree(self.parent.path)


class IconMenu(FileMenu):
    def __init__(self, parent, item):
        FileMenu.__init__(self, parent, item)
        self.InsertSeparator(0)
        parent.Bind(wx.EVT_MENU, self.onConvertToString, self.Insert(0, -1, 'Convert to String'))

    def onConvertToString(self, event):
        cb = wx.TheClipboard
        if cb.Open():
            with open(self.parent.listItem[self.item][0], 'rb') as f:
                data = base64.b64encode(f.read()).decode()
            data64 = []
            begin = 0
            end = begin + 80
            length = len(data)
            while end < length:
                data64.append(data[begin:end])
                begin, end = end, end + 80
            data64.append(data[begin:length])
            cb.Clear()
            cb.SetData(wx.TextDataObject('"' + self.parent.GetItemText(self.item).replace('.ico', '') + '" : PyEmbeddedImage("""\n' +
                                         '\n'.join(data64) + '"""),\n'))
            wx.MessageBox('The string has saved on Clipboard.', 'Attention')
        cb.Flush()
        cb.Close()


class UnknownMenu(FileMenu):
    def __init__(self, parent, item):
        FileMenu.__init__(self, parent, item)
        self.InsertSeparator(0)
        parent.Bind(wx.EVT_MENU, self.onEdit, self.Insert(0, -1, 'Edit'))

    def onEdit(self, event):
        self.parent.grandparent.textpanel.open(self.parent.listItem[self.item][0])
        try:
            self.parent.grandparent.menubar.openrecent.update(self.parent.listItem[self.item][0])
        except: pass


class NewProjectDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'New Project', size=(600, 250))
        self.parent = parent #mainframe
        self.path = ''
        self.nametext = wx.TextCtrl(self)
        self.locationtext = wx.TextCtrl(self)
        browsebtn = wx.Button(self, -1, 'Browse', size=(80, 25))
        self.applybtn = wx.Button(self, -1, 'Apply')
        self.applybtn.Disable()

        self.nametext.Bind(wx.EVT_TEXT, self.toggleApplyBtn)
        self.locationtext.Bind(wx.EVT_TEXT, self.toggleApplyBtn)
        browsebtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        self.applybtn.Bind(wx.EVT_BUTTON, self.onApply)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        namesizer_h = wx.BoxSizer(wx.HORIZONTAL)
        namesizer_h.Add(self.nametext, 1)
        namesizer_h.Add((80, 1))
        namesizer = wx.BoxSizer(wx.VERTICAL)
        namesizer.Add(wx.StaticText(self, -1, 'Project Name'))
        namesizer.Add(namesizer_h, 0, wx.EXPAND)
        locationsizer_h = wx.BoxSizer(wx.HORIZONTAL)
        locationsizer_h.Add(self.locationtext, 1)
        locationsizer_h.Add(browsebtn)
        locationsizer_v = wx.BoxSizer(wx.VERTICAL)
        locationsizer_v.Add(wx.StaticText(self, -1, 'Location'))
        locationsizer_v.Add(locationsizer_h, 0, wx.EXPAND)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1, 20))
        sizer.Add(namesizer, 0, wx.EXPAND)
        sizer.Add((1, 20))
        sizer.Add(locationsizer_v, 0, wx.EXPAND)
        sizer.Add((1, 1), 1)
        sizer.Add(self.applybtn, 0, wx.CENTER)
        sizer.Add((1, 20))
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add((20, 1))
        sizer_h.Add(sizer, 1, wx.EXPAND)
        sizer_h.Add((20, 1))
        self.SetSizer(sizer_h)
        self.Center()
        self.ShowModal()

    def toggleApplyBtn(self, event):
        self.applybtn.Enable(self.nametext.GetValue().strip(' ') != '' and self.locationtext.GetValue().strip(' ') != '')

    def onBrowse(self, event):
        path = wx.DirSelector('Choose Folder ...')
        if path != '':
            self.locationtext.Clear()
            self.locationtext.SetValue(path)

    def onApply(self, event):
        try:
            path = os.path.join(self.locationtext.GetValue(), self.nametext.GetValue())
            os.makedirs(path)
            os.mkdir(os.path.join(path, 'src'))
            #os.mkdir(os.path.join(path, 'bin'))
            self.parent.projectpanel.tree.listExpandedItems = []
            self.parent.projectpanel.tree.reloadTree(path)
            self.path = path
        except:
            wx.MessageBox('Appearing some error.', 'Error')
            #NewProjectDialog(self.parent)
        self.Destroy()

    def onClose(self, event):
        self.Destroy()


class CompileDialog(wx.Dialog):
    def __init__(self, parent, item):
        wx.Dialog.__init__(self, parent, -1, 'Compile', size=(500, 500))
        self.parent = parent #mainframe
        self.item = item
        self.path = self.parent.projectpanel.tree.listItem[self.item][0]
        self.name = wx.TextCtrl(self, -1, os.path.basename(self.path)[:-3], style=wx.TE_READONLY)
        self.onefile_checkbox = wx.CheckBox(self, -1, 'Create a one-file bundled executable')
        self.onefile = True
        self.onefile_checkbox.SetValue(self.onefile)
        self.console_checkbox = wx.CheckBox(self, -1, 'Open a console window for standard i/o')
        self.console = False
        self.icon_checkbox = wx.CheckBox(self, -1, 'Icon')
        self.icon = False
        self.icon_panel = wx.Panel(self)
        self.icon_panel.Show(self.icon)
        self.icon_textctrl = wx.TextCtrl(self.icon_panel)
        self.icon_btn = wx.Button(self.icon_panel, -1, 'Browse', size=(80, 25))
        self.material = wx.ListBox(self, style=wx.LB_HSCROLL)
        self.plus_btn = wx.Button(self, -1, '+', size=(25, 25))
        self.minus_btn = wx.Button(self, -1, '-', size=(25, 25))
        self.compile_btn = wx.Button(self, -1, 'Compile', size=(80, 25))

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.name.Bind(wx.EVT_TEXT, self.onName)
        self.onefile_checkbox.Bind(wx.EVT_CHECKBOX, self.onOnefile)
        self.console_checkbox.Bind(wx.EVT_CHECKBOX, self.onConsole)
        self.icon_checkbox.Bind(wx.EVT_CHECKBOX, self.onIcon)
        self.icon_textctrl.Bind(wx.EVT_TEXT, self.onIconTC)
        self.icon_btn.Bind(wx.EVT_BUTTON, self.onIconBtn)
        self.plus_btn.Bind(wx.EVT_BUTTON, self.onPlus)
        self.minus_btn.Bind(wx.EVT_BUTTON, self.onMinus)
        self.compile_btn.Bind(wx.EVT_BUTTON, self.onCompileBtn)

        namesizer_h = wx.BoxSizer(wx.HORIZONTAL)
        namesizer_h.Add(self.name, 1)
        namesizer_h.Add((80, 1))
        namesizer = wx.BoxSizer(wx.VERTICAL)
        namesizer.Add(wx.StaticText(self, -1, 'Name'))
        namesizer.Add(namesizer_h, 0, wx.EXPAND)
        iconsizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        iconsizer_panel.Add(self.icon_textctrl, 1)
        iconsizer_panel.Add(self.icon_btn)
        self.icon_panel.SetSizer(iconsizer_panel)
        checkboxsizer = wx.BoxSizer(wx.VERTICAL)
        checkboxsizer.Add(self.onefile_checkbox)
        checkboxsizer.Add((1, 20))
        checkboxsizer.Add(self.console_checkbox)
        checkboxsizer.Add((1, 20))
        checkboxsizer.Add(self.icon_checkbox)
        checkboxsizer.Add((1, 20))
        checkboxsizer.Add(self.icon_panel, 0, wx.EXPAND)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add(self.plus_btn)
        btnsizer.Add(self.minus_btn)
        materialsizer = wx.BoxSizer(wx.VERTICAL)
        materialsizer.Add(self.material, 1, wx.EXPAND)
        materialsizer.Add(btnsizer, 0, wx.CENTER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1, 20))
        sizer.Add(namesizer, 0, wx.EXPAND)
        sizer.Add((1, 20))
        sizer.Add(checkboxsizer, 0, wx.EXPAND)
        sizer.Add((1, 20))
        sizer.Add(materialsizer, 1, wx.EXPAND)
        sizer.Add((1, 20))
        sizer.Add(self.compile_btn, 0, wx.CENTER)
        sizer.Add((1, 20))
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add((20, 1))
        sizer_h.Add(sizer, 1, wx.EXPAND)
        sizer_h.Add((20, 1))
        self.SetSizer(sizer_h)
        self.Center()
        self.ShowModal()

    def onClose(self, event):
        self.Destroy()

    def onName(self, event):
        self.toggleCompileBtn()

    def onOnefile(self, event):
        self.onefile = not self.onefile

    def onConsole(self, event):
        self.console = not self.console

    def onIcon(self, event):
        self.icon = not self.icon
        self.icon_panel.Show(self.icon)
        self.Layout()
        self.toggleCompileBtn()

    def onIconTC(self, event):
        self.toggleCompileBtn()

    def onIconBtn(self, event):
        path = wx.FileSelector('Select Icon File', wildcard='Icon (.ico)|*.ico')
        if path != '':
            self.icon_textctrl.Clear()
            self.icon_textctrl.SetValue(path)

    def toggleCompileBtn(self):
        self.compile_btn.Enable(self.name.GetValue().strip(' ') != '' and (self.icon == False or (self.icon == True and self.icon_textctrl.GetValue().strip(' ') != '')))

    def onPlus(self, event):
        path = wx.DirSelector('Choose Folder ...')
        if path != '':
            self.material.Append(path)

    def onMinus(self, event):
        item = self.material.GetSelection()
        if item != -1:
            self.material.Delete(item)
            length = self.material.GetCount()
            if length > 0:
                if item == length:
                    self.material.SetSelection(length-1)
                else:
                    self.material.SetSelection(item)

    def onCompileBtn(self, event):
        style = None
        binpath = os.path.join(self.parent.projectpanel.tree.path, 'bin')
        python = os.path.join(self.parent.setting.HOMEPATH, self.parent.setting.PYTHONEXE)
        if self.onefile:
            style = 'file'
            distpath = os.path.join(binpath, self.name.GetValue() + '.exe')
        else:
            style = 'folder'
            distpath = os.path.join(binpath, self.name.GetValue())
        if wx.MessageBox('Do you want to delete the previous version?', 'Attention', wx.YES_NO) == wx.YES:
            try:
                shutil.rmtree(os.path.join(self.parent.projectpanel.tree.path, 'build'))
            except: pass
            try:
                shutil.rmtree(os.path.join(self.parent.projectpanel.tree.path, 'dist'))
            except: pass
            #'''
            if style == 'folder':
                try:
                    shutil.rmtree(distpath)
                except: pass
            else:
                try:
                    os.remove(distpath)
                except: pass
                for item in range(self.material.GetCount()):
                    try:
                        shutil.rmtree(os.path.join(binpath, os.path.basename(self.material.GetString(item))))
                    except: pass
            #'''
            try:
                os.remove(os.path.join(self.parent.projectpanel.tree.path, '%s.spec' %(self.name.GetValue())))
            except: pass
            extraCmd = "read -rsp $'Press Enter to continue\n'"
            preCmd = 'cd'
            if self.parent.setting.PLATFORM == self.parent.setting.IS_WINDOW:
                preCmd += ' /d "%s"' %(self.parent.projectpanel.tree.path)
                extraCmd = "pause"
            else:
                preCmd += ' "%s"' %(self.parent.projectpanel.tree.path)
            command = '(' + preCmd + ' && "%s" -m PyInstaller' %(python)
            if self.onefile:
                command += ' -F'
            if not self.console:
                command += ' -w'
            if self.icon:
                command += ' -i "%s"' %(os.path.abspath(self.icon_textctrl.GetValue()))
            #command += ' -n "%s" "%s") || %s' %(self.name.GetValue(), self.path, extraCmd)
            command += ' "%s") || %s' %(self.path, extraCmd)
            command = command.replace('\\', '/')
            '''
            print(command)
            '''
            os.system(command)
            if not os.path.exists(binpath):
                os.mkdir(binpath)
            if style == 'folder':
                shutil.move(os.path.join(self.parent.projectpanel.tree.path, 'dist', self.name.GetValue()), distpath)
                for item in range(self.material.GetCount()):
                    shutil.copytree(self.material.GetString(item), os.path.join(distpath, os.path.basename(self.material.GetString(item))))
            else:
                shutil.move(os.path.join(self.parent.projectpanel.tree.path, 'dist', self.name.GetValue()) + '.exe', distpath)
                for item in range(self.material.GetCount()):
                    shutil.copytree(self.material.GetString(item), os.path.join(binpath, os.path.basename(self.material.GetString(item))))
            try:
                shutil.rmtree(os.path.join(self.parent.projectpanel.tree.path, 'build'))
            except: pass
            try:
                shutil.rmtree(os.path.join(self.parent.projectpanel.tree.path, 'dist'))
            except: pass
            try:
                os.remove(os.path.join(self.parent.projectpanel.tree.path, '%s.spec' %(self.name.GetValue())))
            except: pass
            #'''
            self.Destroy()
            self.parent.projectpanel.tree.reloadTree(self.parent.projectpanel.tree.path)


def main():
    return True

if __name__ == '__main__':
    main()
