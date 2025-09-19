import os
import wx
from MultiTool_Office_app.GUI import MyFrame, json
from MultiTool_Office_app.theme import ModernTheme, IconHelper, AnimationHelper
from MultiTool_Office_app.performance import performance_optimizer

config = wx.Config("MultiTool_Office_app")

class ChildClass(MyFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 调用父类的构造函数
        
        # 创建第三个标签页的布局
        bSizer161 = wx.BoxSizer(wx.VERTICAL)
        
        # 创建程序管理面板
        programs_panel, programs_sizer = ModernTheme.create_titled_panel(self.m_panel5, "🚀 独立程序管理")
        
        # 创建网格布局来放置按钮
        gSizer1 = wx.GridSizer(0, 4, 8, 8)  # 增加间距
        programs_sizer.Add(gSizer1, 0, wx.EXPAND | wx.ALL, 10)
        
        # 创建日志/信息显示区域
        log_panel, log_sizer = ModernTheme.create_titled_panel(self.m_panel5, "📝 操作日志")
        
        self.m_textCtrl7 = wx.TextCtrl(log_panel, wx.ID_ANY, 
                                      u"✨ 欢迎使用独立程序管理器!\n" +
                                      u"💡 左键点击：运行程序\n" +
                                      u"🎛️ 右键点击：重命名按钮\n" +
                                      u"⚙️ 鼠标滚轮：绑定程序文件\n", 
                                      wx.DefaultPosition, wx.DefaultSize, 
                                      wx.TE_MULTILINE | wx.TE_READONLY)
        ModernTheme.apply_text_style(self.m_textCtrl7)
        self.m_textCtrl7.SetBackgroundColour(ModernTheme.COLORS['card'])
        log_sizer.Add(self.m_textCtrl7, 1, wx.ALL | wx.EXPAND, 5)
        
        # 添加清空日志按钮
        clear_log_btn = ModernTheme.apply_button_style(
            wx.Button(log_panel, label="🗑️ 清空日志"), 'secondary'
        )
        clear_log_btn.Bind(wx.EVT_BUTTON, self.on_clear_log)
        log_sizer.Add(clear_log_btn, 0, wx.ALL | wx.EXPAND, 5)
        
        bSizer161.Add(programs_panel, 0, wx.EXPAND | wx.ALL, 5)
        bSizer161.Add(log_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel5.SetSizer(bSizer161)
        self.m_panel5.Layout()
        bSizer161.Fit(self.m_panel5)

        # 创建28个按钮，使用现代化样式
        self.program_buttons = []
        for i in range(28):
            button = wx.Button(programs_panel, label=f"🔧 程序 {i + 1}", size=(120, 40))
            ModernTheme.apply_button_style(button, 'secondary')
            
            # 绑定事件
            button.Bind(wx.EVT_MOUSEWHEEL, self.bind_file)
            button.Bind(wx.EVT_LEFT_DOWN, self.run)
            button.Bind(wx.EVT_RIGHT_DOWN, self.rename_button)
            
            # 添加悬停效果
            button.Bind(wx.EVT_ENTER_WINDOW, self.on_button_hover)
            button.Bind(wx.EVT_LEAVE_WINDOW, self.on_button_leave)
            
            gSizer1.Add(button, 0, wx.ALL | wx.EXPAND, 3)
            self.program_buttons.append(button)

        self.m_notebook8.AddPage(self.m_panel5, u"🚀 独立程序", True)
        self.m_panel1.Layout()
        self.Layout()
        self.Centre(wx.BOTH)

        # 从配置中恢复按钮名称
        self.load_button_configurations()
        
        # 添加日志记录
        self.log_message("程序管理器初始化完成")

    def __del__(self):
        pass
    
    def load_button_configurations(self):
        """从配置中加载按钮名称"""
        for button in self.program_buttons:
            button_id = str(button.GetId())
            saved_name = config.Read(button_id)
            if saved_name:
                # 保持图标，更新文本
                if not saved_name.startswith('🔧'):
                    saved_name = f"🔧 {saved_name}"
                button.SetLabel(saved_name)
    
    def log_message(self, message):
        """添加日志消息"""
        import time
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.m_textCtrl7.AppendText(log_entry)
    
    def on_clear_log(self, event):
        """清空日志"""
        self.m_textCtrl7.Clear()
        self.log_message("日志已清空")
    
    def on_button_hover(self, event):
        """按钮悬停效果"""
        button = event.GetEventObject()
        button.SetBackgroundColour(ModernTheme.COLORS['hover'])
        button.Refresh()
    
    def on_button_leave(self, event):
        """按钮离开效果"""
        button = event.GetEventObject()
        ModernTheme.apply_button_style(button, 'secondary')
        button.Refresh()
    
    def bind_file(self, event):
        """绑定文件到按钮 - 优化版本"""
        button_id = str(event.GetId())
        button = event.GetEventObject()
        
        self.log_message(f"开始为按钮 '{button.GetLabel()}' 绑定文件")
        
        with wx.FileDialog(None, "🔍 选择要绑定的程序文件", 
                          wildcard="可执行文件 (*.exe)|*.exe|所有文件 (*.*)|*.*",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_OK:
                selected_file = file_dialog.GetPath()
                
                try:
                    # 保存到配置文件
                    with open('MultiTool_Office_app\\settings.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    
                    data[button_id] = selected_file
                    
                    with open('MultiTool_Office_app\\settings.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=2)
                    
                    # 更新按钮显示
                    filename = os.path.basename(selected_file)
                    button.SetToolTip(f"绑定程序: {selected_file}")
                    
                    self.log_message(f"✅ 文件绑定成功: {filename}")
                    
                    # 添加动画效果
                    AnimationHelper.highlight_button(button)
                    
                except Exception as e:
                    self.log_message(f"❌ 文件绑定失败: {str(e)}")
                    wx.MessageBox(f"绑定文件时发生错误：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
            else:
                self.log_message("用户取消了文件选择")

    def run(self, event):
        """运行绑定的程序 - 优化版本"""
        button_id = str(event.GetId())
        button = event.GetEventObject()
        
        self.log_message(f"尝试运行程序: {button.GetLabel()}")
        
        try:
            with open('MultiTool_Office_app\\settings.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            if button_id in data:
                program_path = data[button_id]
                
                if os.path.exists(program_path):
                    # 异步运行程序，避免阻塞UI
                    def run_program():
                        try:
                            os.startfile(program_path)
                            wx.CallAfter(self.log_message, f"✅ 程序启动成功: {os.path.basename(program_path)}")
                        except Exception as e:
                            wx.CallAfter(self.log_message, f"❌ 程序启动失败: {str(e)}")
                    
                    performance_optimizer.executor.submit(run_program)
                    
                    # 添加视觉反馈
                    AnimationHelper.highlight_button(button, 150)
                    
                else:
                    self.log_message(f"❌ 程序文件不存在: {program_path}")
                    wx.MessageBox(f"程序文件不存在：{program_path}", "错误", wx.OK | wx.ICON_ERROR)
            else:
                self.log_message(f"⚠️ 按钮未绑定程序文件")
                wx.MessageBox("此按钮尚未绑定程序文件，请使用鼠标滚轮绑定文件", "提示", wx.OK | wx.ICON_INFORMATION)
                
        except Exception as e:
            self.log_message(f"❌ 运行程序时发生错误: {str(e)}")
            wx.MessageBox(f"运行程序时发生错误：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def rename_button(self, event):
        """重命名按钮 - 优化版本"""
        button_id = event.GetId()
        button = event.GetEventObject()
        current_label = button.GetLabel()
        
        # 移除图标前缀来显示纯文本
        display_name = current_label.replace("🔧 ", "") if current_label.startswith("🔧") else current_label
        
        with wx.TextEntryDialog(None, 
                               "💬 请输入新的按钮名称:", 
                               "重命名按钮", 
                               display_name,
                               style=wx.OK | wx.CANCEL) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                new_name = dialog.GetValue().strip()
                
                if new_name:
                    # 添加图标前缀
                    full_name = f"🔧 {new_name}"
                    button.SetLabel(full_name)
                    
                    # 保存到配置
                    config.Write(str(button_id), new_name)
                    config.Flush()
                    
                    self.log_message(f"✅ 按钮重命名成功: '{display_name}' → '{new_name}'")
                    
                    # 添加动画效果
                    AnimationHelper.highlight_button(button)
                else:
                    self.log_message("⚠️ 按钮名称不能为空")
                    wx.MessageBox("按钮名称不能为空", "提示", wx.OK | wx.ICON_WARNING)
