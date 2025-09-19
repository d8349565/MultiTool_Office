# -*- coding: utf-8 -*-
import wx, os
import wx.xrc
from MultiTool_Office_app import root_dirs_dict
from MultiTool_Office_app.get_files import list_files, list_dirs, list_files_debounced, list_dirs_async
from MultiTool_Office_app.translate import translate
from MultiTool_Office_app.settings import Settings
from MultiTool_Office_app.theme import ModernTheme, AnimationHelper, IconHelper
from MultiTool_Office_app.performance import performance_optimizer, debounce, throttle, LazyLoader
import threading, json
import pyperclip as cb
from functools import lru_cache
import time


class MyFrame(wx.Frame):

    def __init__(self, parent):
        self.present_dir = ''
        with open('MultiTool_Office_app\\settings.json', 'r') as file:
            data = json.load(file)
        x = data['size_x']
        y = data['size_y']
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"🏢 MultiTool Office", pos=wx.DefaultPosition,
                          size=wx.Size(x, y), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        
        # 应用现代化主题
        self.SetBackgroundColour(ModernTheme.COLORS['background'])
        icon = wx.Icon(r'MultiTool_Office_app\favicon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.SetSizeHints(wx.Size(700, 600), wx.DefaultSize)
        
        # 初始化性能组件
        self.lazy_loaders = {}
        self.search_timer = None
        self.current_page = 0
        self.page_size = 100

        self.m_menubar4 = wx.MenuBar(0)
        self.m_menu5 = wx.Menu()
        self.m_menuItem3 = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"⚙️ 设置", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.m_menuItem3)

        self.m_menu5.AppendSeparator()

        self.m_menubar4.Append(self.m_menu5, u"📋 菜单")

        self.SetMenuBar(self.m_menubar4)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        # 创建主面板并应用主题
        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        ModernTheme.apply_panel_style(self.m_panel1)
        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        # 创建现代化标签控件
        self.m_notebook8 = wx.Notebook(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       wx.NB_FIXEDWIDTH | wx.NB_TOP)
        self.m_notebook8.SetBackgroundColour(ModernTheme.COLORS['surface'])
        self.m_notebook8.SetFont(ModernTheme.FONTS['default'])
        
        # 文件管理标签页
        self.m_panel3 = wx.Panel(self.m_notebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        ModernTheme.apply_panel_style(self.m_panel3)
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

        # 创建搜索和选择区域
        search_panel, search_sizer = ModernTheme.create_titled_panel(self.m_panel16, "🔍 搜索和选择")
        
        m_choice1Choices = list(root_dirs_dict.keys())
        self.m_choice1 = wx.Choice(search_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(150, -1), m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        ModernTheme.apply_button_style(self.m_choice1, 'secondary')
        
        self.m_textCtrl42 = wx.TextCtrl(search_panel, wx.ID_ANY, u"🔍 全局搜索，请在此处输入关键字", 
                                        wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        ModernTheme.apply_text_style(self.m_textCtrl42, 'search')
        
        search_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_box_sizer.Add(self.m_choice1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        search_box_sizer.Add(self.m_textCtrl42, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        search_sizer.Add(search_box_sizer, 0, wx.EXPAND, 5)
        
        bSizer14.Add(search_panel, 0, wx.EXPAND | wx.ALL, 5)

        # 创建目录导航区域
        nav_panel, nav_sizer = ModernTheme.create_titled_panel(self.m_panel16, "📁 目录导航")
        
        dir_labels_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # 创建带图标的目录标签
        label_configs = [
            ("📂 一级目录", "text_secondary"),
            ("📁 二级目录", "text_secondary")
        ]
        
        for label_text, color_key in label_configs:
            label = wx.StaticText(nav_panel, wx.ID_ANY, label_text, wx.DefaultPosition, wx.DefaultSize,
                                 wx.ALIGN_CENTER_HORIZONTAL)
            label.SetFont(ModernTheme.FONTS['subtitle'])
            label.SetForegroundColour(ModernTheme.COLORS[color_key])
            dir_labels_sizer.Add(label, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        nav_sizer.Add(dir_labels_sizer, 0, wx.EXPAND, 5)
        
        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)
        dir_name = self.m_choice1.GetStringSelection()
        self.present_dir = root_dirs_dict[dir_name]
        
        # 异步加载目录列表
        self.m_listBox13 = wx.ListBox(nav_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(150, -1), [],
                                      wx.LB_SORT)
        ModernTheme.apply_listbox_style(self.m_listBox13)
        
        self.m_listBox12 = wx.ListBox(nav_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), [],
                                      wx.LB_SORT)
        ModernTheme.apply_listbox_style(self.m_listBox12)
        
        bSizer16.Add(self.m_listBox13, 0, wx.ALL | wx.EXPAND, 5)
        bSizer16.Add(self.m_listBox12, 1, wx.ALL | wx.EXPAND, 5)
        nav_sizer.Add(bSizer16, 1, wx.EXPAND, 5)
        
        bSizer14.Add(nav_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # 异步加载初始目录
        def load_initial_dirs(dirs):
            if dirs:
                self.m_listBox13.Clear()
                self.m_listBox13.Append(dirs)
        
        list_dirs_async(self.present_dir, load_initial_dirs)

        # 创建三级目录区域
        level3_panel, level3_sizer = ModernTheme.create_titled_panel(self.m_panel16, "📁 三级目录")
        
        self.m_listBox14 = wx.ListBox(level3_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [],
                                      wx.LB_SORT)
        ModernTheme.apply_listbox_style(self.m_listBox14)
        level3_sizer.Add(self.m_listBox14, 1, wx.ALL | wx.EXPAND, 5)
        
        bSizer14.Add(level3_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel16.SetSizer(bSizer14)
        self.m_panel16.Layout()
        bSizer14.Fit(self.m_panel16)
        bSizer8.Add(self.m_panel16, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel17 = wx.Panel(self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer20 = wx.BoxSizer(wx.VERTICAL)

        # 创建搜索和筛选区域
        filter_panel, filter_sizer = ModernTheme.create_titled_panel(self.m_panel17, "🔍 文件筛选")
        
        filter_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        filter_label = wx.StaticText(filter_panel, wx.ID_ANY, u"📝 筛选文本/后缀:", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        filter_label.SetFont(ModernTheme.FONTS['default'])
        filter_label.SetForegroundColour(ModernTheme.COLORS['text_secondary'])
        filter_input_sizer.Add(filter_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl4 = wx.TextCtrl(filter_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_PROCESS_ENTER)
        ModernTheme.apply_text_style(self.m_textCtrl4)
        filter_input_sizer.Add(self.m_textCtrl4, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        filter_sizer.Add(filter_input_sizer, 0, wx.EXPAND, 5)

        # 四级目录和文件列表区域
        files_panel, files_sizer = ModernTheme.create_titled_panel(self.m_panel17, "📂 四级目录")
        
        self.m_listBox17 = wx.ListBox(files_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [],
                                      wx.LB_SORT)
        ModernTheme.apply_listbox_style(self.m_listBox17)
        files_sizer.Add(self.m_listBox17, 1, wx.ALL | wx.EXPAND, 5)
        
        bSizer20.Add(files_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # 文件列表区域
        file_list_panel, file_list_sizer = ModernTheme.create_titled_panel(self.m_panel17, "📄 文件搜索结果")
        
        self.m_listBox5 = wx.ListBox(file_list_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 
                                     wx.LB_SORT | wx.HSCROLL)
        ModernTheme.apply_listbox_style(self.m_listBox5)
        file_list_sizer.Add(self.m_listBox5, 1, wx.ALL | wx.EXPAND, 5)
        
        # 创建加载更多按钮
        self.m_loadMoreBtn = ModernTheme.apply_button_style(
            wx.Button(file_list_panel, label="📥 加载更多文件"), 'secondary'
        )
        self.m_loadMoreBtn.Bind(wx.EVT_BUTTON, self.on_load_more_files)
        file_list_sizer.Add(self.m_loadMoreBtn, 0, wx.ALL | wx.EXPAND, 5)
        
        bSizer20.Add(file_list_panel, 2, wx.EXPAND | wx.ALL, 5)

        self.m_panel17.SetSizer(bSizer20)
        self.m_panel17.Layout()
        bSizer20.Fit(self.m_panel17)
        bSizer8.Add(self.m_panel17, 1, wx.EXPAND | wx.ALL, 5)

        bSizer26.Add(bSizer8, 1, wx.EXPAND, 5)

        self.m_panel3.SetSizer(bSizer26)
        self.m_panel3.Layout()
        bSizer26.Fit(self.m_panel3)
        self.m_notebook8.AddPage(self.m_panel3, u"📁 文件管理", True)
        
        # 翻译标签页
        self.m_panel4 = wx.Panel(self.m_notebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        ModernTheme.apply_panel_style(self.m_panel4)
        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        # 创建翻译语言选择区域
        lang_panel, lang_sizer = ModernTheme.create_titled_panel(self.m_panel4, "🌐 目标语言选择")
        
        m_radioBox1Choices = [u"🇨🇳 中文", u"🇺🇸 英文", u"🇯🇵 日文"]
        self.m_radioBox1 = wx.RadioBox(lang_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize,
                                       m_radioBox1Choices, 3, wx.RA_SPECIFY_COLS)
        self.m_radioBox1.SetSelection(0)
        self.m_radioBox1.SetFont(ModernTheme.FONTS['default'])
        lang_sizer.Add(self.m_radioBox1, 0, wx.ALL | wx.EXPAND, 5)
        
        bSizer12.Add(lang_panel, 0, wx.ALL | wx.EXPAND, 5)

        # 创建输入文本区域
        input_panel, input_sizer = ModernTheme.create_titled_panel(self.m_panel4, "📝 输入文本")
        
        self.m_textCtrl3 = wx.TextCtrl(input_panel, wx.ID_ANY, u"请在此输入需要翻译的文本...", wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_PROCESS_ENTER | wx.TE_MULTILINE)
        ModernTheme.apply_text_style(self.m_textCtrl3)
        input_sizer.Add(self.m_textCtrl3, 1, wx.ALL | wx.EXPAND, 5)
        
        bSizer12.Add(input_panel, 1, wx.ALL | wx.EXPAND, 5)

        # 创建翻译结果区域
        result_panel, result_sizer = ModernTheme.create_titled_panel(self.m_panel4, "✨ 翻译结果")
        
        self.m_textCtrl41 = wx.TextCtrl(result_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_MULTILINE | wx.TE_READONLY)
        ModernTheme.apply_text_style(self.m_textCtrl41)
        self.m_textCtrl41.SetBackgroundColour(ModernTheme.COLORS['card'])
        result_sizer.Add(self.m_textCtrl41, 1, wx.ALL | wx.EXPAND, 5)
        
        # 添加复制按钮
        copy_btn = ModernTheme.apply_button_style(
            wx.Button(result_panel, label="📋 复制结果"), 'primary'
        )
        copy_btn.Bind(wx.EVT_BUTTON, self.on_copy_translation)
        result_sizer.Add(copy_btn, 0, wx.ALL | wx.EXPAND, 5)
        
        bSizer12.Add(result_panel, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel4.SetSizer(bSizer12)
        self.m_panel4.Layout()
        bSizer12.Fit(self.m_panel4)
        self.m_notebook8.AddPage(self.m_panel4, u"🌐 文本翻译", False)
        self.m_panel5 = wx.Panel(self.m_notebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        ModernTheme.apply_panel_style(self.m_panel5)

        bSizer5.Add(self.m_notebook8, 1, wx.ALL | wx.EXPAND, 5)

        # 添加状态栏样式的分隔线
        self.m_staticline4 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.LI_HORIZONTAL)
        self.m_staticline4.SetBackgroundColour(ModernTheme.COLORS['divider'])
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
        self.m_listBox13.Bind(wx.EVT_LISTBOX, self.m_listBox13OnListBox)
        self.m_listBox13.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox13OnLeftDClick)
        self.m_listBox13.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox13OnRightDown)
        self.m_listBox12.Bind(wx.EVT_LISTBOX, self.m_listBox12OnListBox)
        self.m_listBox12.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox12OnLeftDClick)
        self.m_listBox12.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox12OnRightDown)
        self.m_listBox14.Bind(wx.EVT_LISTBOX, self.m_listBox14OnListBox)
        self.m_listBox14.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox14OnLeftDClick)
        self.m_listBox14.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox14OnRightDown)
        self.m_textCtrl4.Bind(wx.EVT_LEFT_DCLICK, self.m_textCtrl4OnLeftDClick)
        self.m_textCtrl4.Bind(wx.EVT_TEXT_ENTER, self.m_textCtrl4OnTextEnter)
        self.m_listBox17.Bind(wx.EVT_LISTBOX, self.m_listBox17OnListBox)
        self.m_listBox17.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox17OnLeftDClick)
        self.m_listBox17.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox17OnRightDown)
        self.m_listBox5.Bind(wx.EVT_LEFT_DCLICK, self.m_listBox5OnLeftDClick)
        self.m_listBox5.Bind(wx.EVT_LISTBOX, self.m_listBox5OnListBox)
        self.m_listBox5.Bind(wx.EVT_RIGHT_DOWN, self.m_listBox5OnRightDown)
        self.m_radioBox1.Bind(wx.EVT_RADIOBOX, self.m_radioBox1OnRadioBox)
        self.m_textCtrl3.Bind(wx.EVT_TEXT_ENTER, self.m_textCtrl3OnTextEnter)
        self.m_textCtrl41.Bind(wx.EVT_RIGHT_DOWN, self.m_textCtrl41OnRightDown)

        self._cache = {}  # 添加缓存字典

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
        """目录选择变更事件 - 使用异步优化"""
        try:
            # 清空所有列表
            self.m_listBox13.Clear()
            self.m_listBox12.Clear()
            self.m_listBox14.Clear()
            self.m_listBox17.Clear()
            self.m_listBox5.Clear()

            dir_name = self.m_choice1.GetStringSelection()
            self.present_dir = root_dirs_dict.get(dir_name, ".")
            
            if not os.path.exists(self.present_dir):
                wx.MessageBox(f"目录不存在: {self.present_dir}", "错误", wx.OK | wx.ICON_ERROR)
                return
            
            # 异步加载目录列表
            def load_dirs_callback(dirs):
                if dirs:
                    self.m_listBox13.Clear()
                    self.m_listBox13.Append(dirs)
                    
            list_dirs_async(self.present_dir, load_dirs_callback)
            
            # 清理缓存
            self.clear_cache_if_needed()
            
        except Exception as e:
            wx.MessageBox(f"发生错误: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def m_choice1OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())
        event.Skip()

    def m_textCtrl4OnLeftDClick(self, event):
        obj = event.GetEventObject()
        obj.Clear()

    def m_textCtrl4OnTextEnter(self, event):
        """筛选文本输入事件 - 使用优化搜索"""
        search_text = self.m_textCtrl4.GetValue()
        self.optimized_search(search_text)
        event.Skip()

    def m_textCtrl42OnLeftDClick(self, event):
        """全局搜索框清空事件 - 优化版本"""
        obj = event.GetEventObject()
        obj.Clear()
        # 重新加载一级目录内容 - 使用异步
        try:
            self.m_listBox13.Clear()
            self.m_listBox12.Clear()
            self.m_listBox14.Clear()
            self.m_listBox17.Clear()
            self.m_listBox5.Clear()

            dir_name = self.m_choice1.GetStringSelection()
            self.present_dir = root_dirs_dict.get(dir_name, ".")
            
            if not os.path.exists(self.present_dir):
                wx.MessageBox(f"目录不存在: {self.present_dir}", "错误", wx.OK | wx.ICON_ERROR)
                return
            
            # 异步加载
            def load_dirs_callback(dirs):
                if dirs:
                    self.m_listBox13.Clear()
                    self.m_listBox13.Append(dirs)
                    
            list_dirs_async(self.present_dir, load_dirs_callback)
            
        except Exception as e:
            wx.MessageBox(f"发生错误: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

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
        """一级目录点击事件"""
        thread = threading.Thread(target=self.run_task_m_listBox13OnListBox)
        thread.start()

    def run_task_m_listBox13OnListBox(self):
        """一级目录点击事件的线程任务"""
        self.m_listBox12.Clear()
        self.m_listBox14.Clear()
        self.m_listBox17.Clear()
        self.m_listBox5.Clear()
        
        dir_name = self.m_listBox13.GetStringSelection()
        if not dir_name:
            return
        
        target_dir_name = os.path.join(self.present_dir, dir_name)
        dirs = list(list_dirs(target_dir_name))
        self.m_listBox12.Append(dirs)

    def m_listBox13OnRightDown(self, event):
        dir_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection())
        os.startfile(dir_path)

    def m_listBox12OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())

    def m_listBox12OnListBox(self, event):
        """二级目录点击事件"""
        thread = threading.Thread(target=self.run_task_m_listBox12OnListBox)
        thread.start()

    def run_task_m_listBox12OnListBox(self):
        """二级目录点击事件的线程任务"""
        self.m_listBox14.Clear()
        self.m_listBox17.Clear()
        self.m_listBox5.Clear()
        
        dir_name = self.m_listBox12.GetStringSelection()
        if not dir_name:
            return
        
        target_dir_name = os.path.join(self.present_dir,
                                      self.m_listBox13.GetStringSelection(),
                                      dir_name)
        dirs = list(list_dirs(target_dir_name))
        self.m_listBox14.Append(dirs)
        
        flag = self.m_textCtrl4.GetValue()
        files = [os.path.relpath(i, target_dir_name) for i in list_files(target_dir_name) if flag in i]
        self.m_listBox5.Append(files)

    def m_listBox12OnRightDown(self, event):
        dir_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                self.m_listBox12.GetStringSelection())
        os.startfile(dir_path)

    def m_listBox14OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())
        event.Skip()

    def m_listBox14OnListBox(self, event):
        """三级目录点击事件"""
        thread = threading.Thread(target=self.run_task_m_listBox14OnListBox)
        thread.start()

    def run_task_m_listBox14OnListBox(self):
        """三级目录点击事件的线程任务"""
        self.m_listBox17.Clear()
        self.m_listBox5.Clear()
        
        dir_name = self.m_listBox14.GetStringSelection()
        if not dir_name:
            return
        
        target_dir_name = os.path.join(self.present_dir,
                                      self.m_listBox13.GetStringSelection(),
                                      self.m_listBox12.GetStringSelection(),
                                      dir_name)
        dirs = list(list_dirs(target_dir_name))
        self.m_listBox17.Append(dirs)
        
        flag = self.m_textCtrl4.GetValue()
        files = [os.path.relpath(i, target_dir_name) for i in list_files(target_dir_name) if flag in i]
        self.m_listBox5.Append(files)

    def m_listBox14OnRightDown(self, event):
        dir_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                self.m_listBox12.GetStringSelection(), self.m_listBox14.GetStringSelection())
        os.startfile(dir_path)

    def m_listBox17OnLeftDClick(self, event):
        obj = event.GetEventObject()
        cb.copy(obj.GetStringSelection())
        event.Skip()

    def m_listBox17OnListBox(self, event):
        """四级目录点击事件"""
        thread = threading.Thread(target=self.run_task_m_listBox17OnListBox)
        thread.start()

    def run_task_m_listBox17OnListBox(self):
        """四级目录点击事件的线程任务"""
        self.m_listBox5.Clear()
        
        dir_name = self.m_listBox17.GetStringSelection()
        if not dir_name:
            return
        
        target_dir_name = os.path.join(self.present_dir,
                                      self.m_listBox13.GetStringSelection(),
                                      self.m_listBox12.GetStringSelection(),
                                      self.m_listBox14.GetStringSelection(),
                                      dir_name)
        
        flag = self.m_textCtrl4.GetValue()
        files = [os.path.relpath(i, target_dir_name) for i in list_files(target_dir_name) if flag in i]
        self.m_listBox5.Append(files)

    def m_listBox17OnRightDown(self, event):
        dir_path = os.path.join(self.present_dir, self.m_listBox13.GetStringSelection(),
                                self.m_listBox12.GetStringSelection(), self.m_listBox14.GetStringSelection(),
                                self.m_listBox17.GetStringSelection())
        os.startfile(dir_path)

    def m_listBox5OnLeftDClick(self, event):
        try:
            file_path = os.path.join(self.present_dir, 
                                    self.m_listBox13.GetStringSelection(),
                                    self.m_listBox12.GetStringSelection(), 
                                    self.m_listBox14.GetStringSelection(),
                                    self.m_listBox17.GetStringSelection(), 
                                    self.m_listBox5.GetStringSelection())
            if os.path.exists(file_path):
                os.startfile(file_path)                
            else:
                wx.MessageBox("文件不存在", "错误", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"打开文件失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

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
        """优化的翻译任务"""
        try:
            # 语言映射
            lang_map = {
                '🇨🇳 中文': 'zh', 
                '🇯🇵 日文': 'ja', 
                '🇺🇸 英文': 'en',
                # 兼容旧版本
                '中文': 'zh', 
                '日文': 'ja', 
                '英文': 'en'
            }
            
            text = self.m_textCtrl3.GetValue().strip()
            if not text:
                wx.CallAfter(self.m_textCtrl41.SetValue, "请输入要翻译的文本")
                return
            
            # 清除提示文本
            if text == "请在此输入需要翻译的文本...":
                wx.CallAfter(self.m_textCtrl41.SetValue, "请输入要翻译的文本")
                return
            
            selected_lang = self.m_radioBox1.GetStringSelection()
            target_lang = lang_map.get(selected_lang, 'zh')
            
            # 显示翻译中状态
            wx.CallAfter(self.m_textCtrl41.SetValue, "🔄 正在翻译，请稍候...")
            
            # 执行翻译
            from .translate import translate
            result = translate(text, target_lang)
            
            # 更新结果
            wx.CallAfter(self.m_textCtrl41.SetValue, result)
            
        except Exception as e:
            error_msg = f"翻译失败: {str(e)}"
            wx.CallAfter(self.m_textCtrl41.SetValue, error_msg)

    def m_textCtrl3OnTextEnter(self, event):
        """翻译文本输入事件 - 使用线程池优化"""
        # 使用性能优化器的线程池
        performance_optimizer.executor.submit(self.run_task_m_textCtrl3OnTextEnter)

    def m_textCtrl41OnRightDown(self, event):
        event.Skip()

    @lru_cache(maxsize=100)
    def get_directory_contents(self, path):
        """缓存目录内容"""
        return list(os.scandir(path))

    def load_file_list(self, files):
        """分页加载文件列表"""
        start = self.current_page * self.page_size
        end = start + self.page_size
        self.m_listBox5.Clear()
        self.m_listBox5.Append(files[start:end])

    def get_safe_path(self, *parts):
        """安全地组合文件路径"""
        try:
            path = os.path.normpath(os.path.join(*parts))
            # 确保路径在允许的范围内
            if os.path.commonprefix([path, self.present_dir]) == self.present_dir:
                return path
            return None
        except Exception:
            return None
    
    # 新增的优化方法
    def on_load_more_files(self, event):
        """加载更多文件按钮事件"""
        self.current_page += 1
        
        # 获取当前目录路径
        try:
            current_path = self.get_current_directory_path()
            if current_path:
                flag = self.m_textCtrl4.GetValue()
                
                def load_more_task():
                    try:
                        files = list_files(current_path, flag)
                        start = self.current_page * self.page_size
                        end = start + self.page_size
                        
                        if start < len(files):
                            new_files = files[start:end]
                            # 在主线程中更新UI
                            wx.CallAfter(self.append_files_to_list, new_files)
                        else:
                            wx.CallAfter(self.show_no_more_files_message)
                    except Exception:
                        pass
                
                performance_optimizer.executor.submit(load_more_task)
        except Exception:
            pass
    
    def append_files_to_list(self, files):
        """向文件列表追加新文件"""
        for file in files:
            # 添加文件图标
            icon = IconHelper.get_file_icon_text(file)
            self.m_listBox5.Append(f"{icon} {os.path.basename(file)}")
    
    def show_no_more_files_message(self):
        """显示没有更多文件的消息"""
        wx.MessageBox("没有更多文件了", "提示", wx.OK | wx.ICON_INFORMATION)
    
    def get_current_directory_path(self):
        """获取当前选中的目录路径"""
        try:
            selections = [
                self.m_listBox13.GetStringSelection(),
                self.m_listBox12.GetStringSelection(),
                self.m_listBox14.GetStringSelection(),
                self.m_listBox17.GetStringSelection()
            ]
            
            # 过滤空选择
            valid_selections = [s for s in selections if s]
            
            if valid_selections:
                return os.path.join(self.present_dir, *valid_selections)
            else:
                return self.present_dir
        except Exception:
            return None
    
    def on_copy_translation(self, event):
        """复制翻译结果"""
        result = self.m_textCtrl41.GetValue()
        if result:
            cb.copy(result)
            # 显示复制成功的视觉反馈
            AnimationHelper.highlight_button(event.GetEventObject())
            # 使用普通的消息框代替MessageTip
            wx.CallAfter(lambda: wx.MessageBox("翻译结果已复制到剪贴板", "复制成功", wx.OK | wx.ICON_INFORMATION))
    
    @debounce(wait_time=0.5)
    def optimized_search(self, search_text):
        """优化的搜索功能，带防抖"""
        if not search_text.strip():
            return
        
        current_path = self.get_current_directory_path()
        if not current_path:
            return
        
        def search_task():
            try:
                # 重置分页
                self.current_page = 0
                
                # 使用优化的搜索
                files = performance_optimizer.search_files_optimized(
                    current_path, search_text, max_results=500
                )
                
                # 在主线程中更新UI
                wx.CallAfter(self.update_search_results, files)
            except Exception:
                wx.CallAfter(self.update_search_results, [])
        
        performance_optimizer.executor.submit(search_task)
    
    def update_search_results(self, files):
        """更新搜索结果显示"""
        self.m_listBox5.Clear()
        
        # 显示前100个结果
        display_files = files[:100]
        
        for file in display_files:
            try:
                relative_path = os.path.relpath(file, self.present_dir)
                icon = IconHelper.get_file_icon_text(file)
                display_name = f"{icon} {os.path.basename(file)}"
                self.m_listBox5.Append(display_name)
            except Exception:
                continue
        
        # 如果还有更多文件，显示加载更多按钮
        if len(files) > 100:
            self.m_loadMoreBtn.Show()
            self.m_loadMoreBtn.SetLabel(f"📥 加载更多 (还有 {len(files) - 100} 个文件)")
        else:
            self.m_loadMoreBtn.Hide()
        
        self.m_panel17.Layout()
    
    @throttle(interval=2.0)
    def clear_cache_if_needed(self):
        """根据需要清理缓存"""
        stats = performance_optimizer.get_cache_stats()
        if stats['total_cached_items'] > 200:
            performance_optimizer.clear_cache()
