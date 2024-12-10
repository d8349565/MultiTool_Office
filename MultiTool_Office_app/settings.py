# -*- coding: utf-8 -*-
import wx
import json
import os
import sys
import wx.xrc
from MultiTool_Office_app import root_dirs

class Settings(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"请在此界面设置文件管理目录", pos=wx.DefaultPosition,
                           size=wx.Size(438, 298), style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer15 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"以下为已添加的目录", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText7.Wrap(-1)

        bSizer15.Add(self.m_staticText7, 0, wx.ALL | wx.EXPAND, 5)

        m_listBox6Choices = root_dirs
        self.m_listBox6 = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox6Choices, 0)
        bSizer15.Add(self.m_listBox6, 1, wx.ALL | wx.EXPAND, 5)

        bSizer17 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button_delete = wx.Button(self, wx.ID_ANY, u"删除上方选择目录", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17.Add(self.m_button_delete, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_dirPicker1 = wx.DirPickerCtrl(self, wx.ID_ANY, u"F:\\Python_files\\程序UI设计\\案例1",
                                             u"Select a folder", wx.DefaultPosition, wx.Size(300, -1),
                                             wx.DIRP_DEFAULT_STYLE)
        bSizer17.Add(self.m_dirPicker1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button_add_dir = wx.Button(self, wx.ID_ANY, u"添加左侧目录", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17.Add(self.m_button_add_dir, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer15.Add(bSizer17, 0, 0, 5)

        self.SetSizer(bSizer15)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_button_delete.Bind(wx.EVT_BUTTON, self.m_button_deleteOnButtonClick)
        self.m_button_add_dir.Bind(wx.EVT_BUTTON, self.m_button_add_dirOnButtonClick)

    def __del__(self):
        pass

    def m_button_deleteOnButtonClick(self, event):
        selected = self.m_listBox6.GetStringSelection()
        new_dirs = root_dirs
        del new_dirs[new_dirs.index(selected)]
        self.m_listBox6.Clear()
        self.m_listBox6.Append(new_dirs)
        with open('MultiTool_Office_app\\settings.json', 'r') as file:
            data = json.load(file)
        data['root_dirs'] = new_dirs
        with open('MultiTool_Office_app\\settings.json', 'w') as file:
            json.dump(data, file)
        os.execl(sys.executable, sys.executable, *sys.argv)

    def m_button_add_dirOnButtonClick(self, event):
        new_dir = self.m_dirPicker1.GetPath()
        new_dirs = root_dirs
        new_dirs.append(new_dir)
        self.m_listBox6.Clear()
        self.m_listBox6.Append(new_dirs)
        with open('MultiTool_Office_app\\settings.json', 'r') as file:
            data = json.load(file)
        data['root_dirs'] = new_dirs
        with open('MultiTool_Office_app\\settings.json', 'w') as file:
            json.dump(data, file)
        os.execl(sys.executable, sys.executable, *sys.argv)



if __name__ == '__main__':
    app = wx.App()
    frame = Settings(None)
    frame.Show(True)
    app.MainLoop()
