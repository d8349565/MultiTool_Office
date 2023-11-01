# -*- coding: utf-8 -*-
import wx,os
import wx.xrc
from MultiTool_Office_app import root_dirs_dict
from MultiTool_Office_app.get_files import list_files, list_dirs
from MultiTool_Office_app.translate import translate
from MultiTool_Office_app.settings import Settings
import threading
import pyperclip as cb

class MyFrame(wx.Frame):
    def __init__(self, parent):

        self.present_dir = ''

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"MultiTool Office", pos=wx.DefaultPosition,
                          size=wx.Size(800, 800), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        icon = wx.Icon(r'MultiTool_Office_app\favicon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.SetSizeHints( wx.Size( 600,600 ), wx.DefaultSize )
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.m_menubar4 = wx.MenuBar(0)
        self.m_menu5 = wx.Menu()
        self.m_menuItem3 = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"设置", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.m_menuItem3)

        self.m_menu5.AppendSeparator()

        # self.m_menuItem4 = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"文件", wx.EmptyString, wx.ITEM_NORMAL)
        # self.m_menu5.Append(self.m_menuItem4)

        # self.m_menuItem5 = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"退出", wx.EmptyString, wx.ITEM_NORMAL)
        # self.m_menu5.Append(self.m_menuItem5)

        self.m_menubar4.Append(self.m_menu5, u"菜单")

        self.SetMenuBar(self.m_menubar4)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.m_notebook8 = wx.Notebook(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       wx.NB_FIXEDWIDTH | wx.NB_NOPAGETHEME)
        self.m_panel3 = wx.Panel(self.m_notebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL,
                                 u"文件管理")
        bSizer26 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel30 = wx.Panel(self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel30.SetMaxSize(wx.Size(-1, 5))

        bSizer26.Add(self.m_panel30, 0, wx.ALL | wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticline6 = wx.StaticLine(self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.LI_HORIZONTAL)
        bSizer8.Add(self.m_staticline6, 0, wx.EXPAND | wx.ALL, 5)

        self.m_panel16 = wx.Panel(self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        m_choice1Choices = list(root_dirs_dict.keys())
        self.m_choice1 = wx.Choice(self.m_panel16, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        bSizer15.Add(self.m_choice1, 0, wx.ALL, 5)

        self.m_textCtrl42 = wx.TextCtrl(self.m_panel16, wx.ID_ANY, u"全局搜索，请在此处输入关键字", wx.DefaultPosition,
                                        wx.DefaultSize, wx.TE_PROCESS_ENTER)
        bSizer15.Add(self.m_textCtrl42, 1, wx.ALL, 5)

        bSizer14.Add(bSizer15, 0, wx.EXPAND, 5)

        bSizer22 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText5 = wx.StaticText(self.m_panel16, wx.ID_ANY, u"一级目录", wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText5.Wrap(-1)

        bSizer22.Add(self.m_staticText5, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText6 = wx.StaticText(self.m_panel16, wx.ID_ANY, u"二级目录", wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText6.Wrap(-1)

        bSizer22.Add(self.m_staticText6, 1, wx.ALL, 5)

        bSizer14.Add(bSizer22, 0, wx.EXPAND, 5)

        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)
        dir_name = self.m_choice1.GetStringSelection()
        self.present_dir = root_dirs_dict[dir_name]
        m_listBox13Choices = [i for i in list_dirs(self.present_dir)]
        self.m_listBox13 = wx.ListBox(self.m_panel16, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox13Choices,
                                      wx.LB_SORT)
        self.m_listBox13.SetMaxSize( wx.Size( 120,-1 ) )
        bSizer16.Add(self.m_listBox13, 0, wx.ALL | wx.EXPAND, 5)

        m_listBox12Choices = []
        self.m_listBox12 = wx.ListBox(self.m_panel16, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox12Choices,
                                      wx.LB_SORT)
        self.m_listBox12.SetMinSize( wx.Size(200,-1 ) )
        bSizer16.Add(self.m_listBox12, 1, wx.ALL | wx.EXPAND, 5)

        bSizer14.Add(bSizer16, 1, wx.EXPAND, 5)

        self.m_staticText51 = wx.StaticText(self.m_panel16, wx.ID_ANY, u"三级目录", wx.DefaultPosition, wx.DefaultSize,
                                            wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText51.Wrap(-1)

        bSizer14.Add(self.m_staticText51, 0, wx.ALL | wx.EXPAND, 5)

        m_listBox14Choices = []
        self.m_listBox14 = wx.ListBox(self.m_panel16, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox14Choices,
                                      wx.LB_SORT)
        bSizer14.Add(self.m_listBox14, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel16.SetSizer(bSizer14)
        self.m_panel16.Layout()
        bSizer14.Fit(self.m_panel16)
        bSizer8.Add(self.m_panel16, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel17 = wx.Panel(self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer20 = wx.BoxSizer(wx.VERTICAL)

        bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText53 = wx.StaticText(self.m_panel17, wx.ID_ANY, u"筛选文本/后缀", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText53.Wrap(-1)

        bSizer21.Add(self.m_staticText53, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl4 = wx.TextCtrl(self.m_panel17, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_PROCESS_ENTER)
        bSizer21.Add(self.m_textCtrl4, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer20.Add(bSizer21, 0, wx.EXPAND, 5)

        bSizer131 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText611 = wx.StaticText(self.m_panel17, wx.ID_ANY, u"四级目录", wx.DefaultPosition, wx.DefaultSize,
                                             wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText611.Wrap(-1)

        bSizer131.Add(self.m_staticText611, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer20.Add(bSizer131, 0, wx.EXPAND, 5)

        m_listBox17Choices = []
        self.m_listBox17 = wx.ListBox(self.m_panel17, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox17Choices,
                                      wx.LB_SORT)
        bSizer20.Add(self.m_listBox17, 1, wx.ALL | wx.EXPAND, 5)

        bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText61 = wx.StaticText(self.m_panel17, wx.ID_ANY, u"文件搜索结果", wx.DefaultPosition,
                                            wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText61.Wrap(-1)

        bSizer13.Add(self.m_staticText61, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer20.Add(bSizer13, 0, wx.EXPAND, 5)

        m_listBox5Choices = []
        self.m_listBox5 = wx.ListBox(self.m_panel17, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox5Choices,
                                     wx.LB_SORT | wx.HSCROLL)
        bSizer20.Add(self.m_listBox5, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel17.SetSizer(bSizer20)
        self.m_panel17.Layout()
        bSizer20.Fit(self.m_panel17)
        bSizer8.Add(self.m_panel17, 1, wx.EXPAND | wx.ALL, 5)

        bSizer26.Add(bSizer8, 1, wx.EXPAND, 5)

        self.m_panel3.SetSizer(bSizer26)
        self.m_panel3.Layout()
        bSizer26.Fit(self.m_panel3)
        self.m_notebook8.AddPage(self.m_panel3, u"文件管理", True)
        self.m_panel4 = wx.Panel(self.m_notebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        m_radioBox1Choices = [u"中文", u"英文", u"日文"]
        self.m_radioBox1 = wx.RadioBox(self.m_panel4, wx.ID_ANY, u"目标语言", wx.DefaultPosition, wx.DefaultSize,
                                       m_radioBox1Choices, 1, wx.RA_SPECIFY_ROWS)
        self.m_radioBox1.SetSelection(0)
        bSizer12.Add(self.m_radioBox1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl3 = wx.TextCtrl(self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)
        bSizer12.Add(self.m_textCtrl3, 1, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl41 = wx.TextCtrl(self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        bSizer12.Add(self.m_textCtrl41, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel4.SetSizer(bSizer12)
        self.m_panel4.Layout()
        bSizer12.Fit(self.m_panel4)
        self.m_notebook8.AddPage(self.m_panel4, u"文本翻译", False)
        self.m_panel5 = wx.Panel(self.m_notebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_notebook8.AddPage(self.m_panel5, u"ChatBot", False)

        bSizer5.Add(self.m_notebook8, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticline4 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.LI_HORIZONTAL)
        bSizer5.Add(self.m_staticline4, 0, wx.EXPAND | wx.ALL, 5)

        # self.m_panel9 = wx.Panel(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 20), wx.TAB_TRAVERSAL)
        # self.m_panel9.SetMaxSize(wx.Size(-1, 20))
        #
        # bSizer7 = wx.BoxSizer(wx.VERTICAL)
        #
        # self.m_gauge2 = wx.Gauge(self.m_panel9, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        # self.m_gauge2.SetValue(0)
        # bSizer7.Add(self.m_gauge2, 1, wx.ALL | wx.EXPAND, 5)
        #
        # self.m_panel9.SetSizer(bSizer7)
        # self.m_panel9.Layout()
        # bSizer5.Add(self.m_panel9, 0, wx.ALL | wx.EXPAND, 5)

        self.m_panel1.SetSizer(bSizer5)
        self.m_panel1.Layout()
        bSizer5.Fit(self.m_panel1)
        bSizer3.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.m_menuItem3OnMenuSelection, id=self.m_menuItem3.GetId())
        # self.Bind(wx.EVT_MENU, self.m_menuItem4OnMenuSelection, id=self.m_menuItem4.GetId())
        # self.Bind(wx.EVT_MENU, self.m_menuItem5OnMenuSelection, id=self.m_menuItem5.GetId())
        self.m_choice1.Bind(wx.EVT_CHOICE, self.m_choice1OnChoice)
        self.m_choice1.Bind(wx.EVT_LEFT_DCLICK, self.m_choice1OnLeftDClick)
        self.m_textCtrl42.Bind(wx.EVT_LEFT_DCLICK, self.m_textCtrl42OnLeftDClick)
        self.m_textCtrl42.Bind(wx.EVT_TEXT_ENTER, self.m_textCtrl42OnTextEnter)
        self.m_listBox13.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox13OnLeftDClick)
        self.m_listBox13.Bind(wx.EVT_LISTBOX, self.m_listBox13OnListBox)
        self.m_listBox13.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox13OnRightDown)
        self.m_listBox12.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox12OnLeftDClick)
        self.m_listBox12.Bind(wx.EVT_LISTBOX, self.m_listBox12OnListBox)
        self.m_listBox12.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox12OnRightDown)
        self.m_listBox14.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox14OnLeftDClick)
        self.m_listBox14.Bind(wx.EVT_LISTBOX, self.m_listBox14OnListBox)
        self.m_listBox14.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox14OnRightDown)
        self.m_textCtrl4.Bind(wx.EVT_LEFT_DCLICK, self.m_textCtrl4OnLeftDClick)
        self.m_textCtrl4.Bind(wx.EVT_TEXT_ENTER, self.m_textCtrl4OnTextEnter)
        self.m_listBox17.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox17OnLeftDClick)
        self.m_listBox17.Bind(wx.EVT_LISTBOX, self.m_listBox17OnListBox)
        self.m_listBox17.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox17OnRightDown)
        self.m_listBox5.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox5OnLeftDClick)
        self.m_listBox5.Bind(wx.EVT_LISTBOX, self.m_listBox5OnListBox)
        self.m_listBox5.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox5OnRightDown)
        self.m_radioBox1.Bind(wx.EVT_RADIOBOX, self.m_radioBox1OnRadioBox)
        self.m_textCtrl3.Bind(wx.EVT_TEXT_ENTER, self.m_textCtrl3OnTextEnter)
        self.m_textCtrl41.Bind(wx.EVT_RIGHT_DOWN, self.m_textCtrl41OnRightDown)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def m_menuItem3OnMenuSelection(self, event):
        settings_frame = Settings(None)
        settings_frame.Show(True)
        event.Skip()

    def m_menuItem4OnMenuSelection(self, event):
        event.Skip()

    def m_menuItem5OnMenuSelection(self, event):
        event.Skip()

    def m_choice1OnChoice(self, event):
        self.m_listBox13.Clear()
        self.m_listBox12.Clear()
        self.m_listBox14.Clear()
        self.m_listBox17.Clear()
        self.m_listBox5.Clear()

        dir_name = self.m_choice1.GetStringSelection()
        self.present_dir = root_dirs_dict[dir_name]
        dirs = [i for i in list_dirs(self.present_dir)]
        self.m_listBox13.Clear()
        self.m_listBox13.Append(dirs)

    def m_choice1OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())
        event.Skip()

    def m_textCtrl4OnLeftDClick(self, event):
        obj = event.GetEventObject()
        obj.Clear()

    def m_textCtrl4OnTextEnter(self, event):
        event.Skip()

    def m_textCtrl42OnLeftDClick(self, event):
        obj = event.GetEventObject()
        obj.Clear()

    def run_task_m_textCtrl42OnTextEnter(self):
        self.m_listBox12.Clear()
        self.m_listBox13.Clear()
        self.m_listBox14.Clear()
        self.m_listBox17.Clear()
        self.m_listBox5.Clear()
        target_dir_name = self.present_dir
        flag = self.m_textCtrl42.GetValue()
        files = [os.path.relpath(i, target_dir_name) for i in list_files(target_dir_name) if flag in i]
        self.m_listBox5.Clear()
        self.m_listBox5.Append(files)

    def m_textCtrl42OnTextEnter(self, event):
        thread = threading.Thread(target=self.run_task_m_textCtrl42OnTextEnter)
        thread.start()

    def m_listBox13OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())
        event.Skip()

    def m_listBox13OnListBox(self, event):
        self.m_listBox12.Clear()
        self.m_listBox14.Clear()
        self.m_listBox17.Clear()
        self.m_listBox5.Clear()
        dir_name = self.m_listBox13.GetStringSelection()
        target_dir_name = os.path.join(self.present_dir, dir_name)
        dirs = [i for i in list_dirs(target_dir_name)]
        self.m_listBox12.Clear()
        self.m_listBox12.Append(dirs)

    def m_listBox13OnRightDown(self, event):
        dir_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection())
        os.startfile(dir_path)

    def m_listBox12OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())

    def run_task_m_listBox12OnListBox(self):
        self.m_listBox14.Clear()
        self.m_listBox17.Clear()
        self.m_listBox5.Clear()
        target_dir_name = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                       self.m_listBox12.GetStringSelection())
        dirs = [i for i in list_dirs(target_dir_name)]
        self.m_listBox14.Append(dirs)
        flag = self.m_textCtrl4.GetValue()
        files = [os.path.relpath(i, target_dir_name) for i in list_files(target_dir_name) if flag in i]
        self.m_listBox5.Clear()
        self.m_listBox5.Append(files)

    def m_listBox12OnListBox(self, event):
        thread = threading.Thread(target=self.run_task_m_listBox12OnListBox)
        thread.start()

    def m_listBox12OnRightDown(self, event):
        dir_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                 self.m_listBox12.GetStringSelection())
        os.startfile(dir_path)

    def m_listBox14OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())
        event.Skip()

    def run_task_m_listBox14OnListBox(self):
        self.m_listBox17.Clear()
        self.m_listBox5.Clear()
        target_dir_name = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                       self.m_listBox12.GetStringSelection(), self.m_listBox14.GetStringSelection())
        dirs = [i for i in list_dirs(target_dir_name)]
        self.m_listBox17.Clear()
        self.m_listBox17.Append(dirs)
        flag = self.m_textCtrl4.GetValue()
        files = [os.path.relpath(i, target_dir_name) for i in list_files(target_dir_name) if flag in i]
        self.m_listBox5.Clear()
        self.m_listBox5.Append(files)

    def m_listBox14OnListBox(self, event):
        thread = threading.Thread(target=self.run_task_m_listBox14OnListBox)
        thread.start()

    def m_listBox14OnRightDown(self, event):
        dir_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                 self.m_listBox12.GetStringSelection(), self.m_listBox14.GetStringSelection())
        os.startfile(dir_path)

    def m_listBox17OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())
        event.Skip()

    def run_task_m_listBox17OnListBox(self):
        self.m_listBox5.Clear()
        target_dir_name = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                       self.m_listBox12.GetStringSelection(), self.m_listBox14.GetStringSelection(),
                                       self.m_listBox17.GetStringSelection())
        flag = self.m_textCtrl4.GetValue()
        files = [os.path.relpath(i, target_dir_name) for i in list_files(target_dir_name) if flag in i]
        self.m_listBox5.Clear()
        self.m_listBox5.Append(files)

    def m_listBox17OnListBox(self, event):
        thread = threading.Thread(target=self.run_task_m_listBox17OnListBox)
        thread.start()

    def m_listBox17OnRightDown(self, event):
        dir_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                 self.m_listBox12.GetStringSelection(), self.m_listBox14.GetStringSelection(),
                                 self.m_listBox17.GetStringSelection())
        os.startfile(dir_path)

    def m_listBox5OnLeftDClick(self, event):
        file_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                 self.m_listBox12.GetStringSelection(), self.m_listBox14.GetStringSelection(),
                                 self.m_listBox17.GetStringSelection(), self.m_listBox5.GetStringSelection())
        os.startfile(file_path)

    def m_listBox5OnListBox(self, event):
        pass

    def m_listBox5OnRightDown(self, event):
        file_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                 self.m_listBox12.GetStringSelection(), self.m_listBox14.GetStringSelection(),
                                 self.m_listBox17.GetStringSelection(), self.m_listBox5.GetStringSelection())
        dir_path = os.path.dirname(file_path)
        os.startfile(dir_path)

    def m_radioBox1OnRadioBox(self, event):
        event.Skip()



    def run_task_m_textCtrl3OnTextEnter(self):
        d = {'中文': 'zh', '日文': 'ja', '英文': 'en', }
        text = self.m_textCtrl3.GetValue()
        lang = d[self.m_radioBox1.GetStringSelection()]
        result = translate(text, lang)
        self.m_textCtrl41.SetValue(result)

    def m_textCtrl3OnTextEnter(self, event):
        thread = threading.Thread(target=self.run_task_m_textCtrl3OnTextEnter)
        thread.start()



    def m_textCtrl41OnRightDown(self, event):
        event.Skip()
