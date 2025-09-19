# -*- coding: utf-8 -*-
"""
现代化主题系统 - UI美化组件
提供统一的颜色方案、字体配置和控件样式
"""
import wx

class ModernTheme:
    """现代化主题配置类"""
    
    # 颜色方案 - 使用现代化的色彩搭配
    COLORS = {
        # 主色调 - 深蓝色系
        'primary': wx.Colour(33, 150, 243),      # 主要蓝色
        'primary_dark': wx.Colour(21, 101, 192), # 深蓝色
        'primary_light': wx.Colour(144, 202, 249), # 浅蓝色
        
        # 背景色
        'background': wx.Colour(250, 250, 250),   # 主背景 - 浅灰白
        'surface': wx.Colour(255, 255, 255),     # 表面色 - 纯白
        'card': wx.Colour(248, 249, 250),        # 卡片背景
        
        # 文本色
        'text_primary': wx.Colour(33, 33, 33),   # 主文本 - 深灰
        'text_secondary': wx.Colour(117, 117, 117), # 次要文本
        'text_disabled': wx.Colour(189, 189, 189),  # 禁用文本
        
        # 边框和分隔线
        'border': wx.Colour(224, 224, 224),      # 边框色
        'divider': wx.Colour(238, 238, 238),     # 分隔线
        
        # 状态色
        'success': wx.Colour(76, 175, 80),       # 成功绿色
        'warning': wx.Colour(255, 152, 0),       # 警告橙色
        'error': wx.Colour(244, 67, 54),         # 错误红色
        
        # 选中和悬停
        'selected': wx.Colour(227, 242, 253),    # 选中背景
        'hover': wx.Colour(245, 245, 245),       # 悬停背景
    }
    
    # 字体配置
    FONTS = {
        'default': wx.Font(9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL),
        'title': wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD),
        'subtitle': wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL),
        'caption': wx.Font(8, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL),
    }
    
    # 控件样式配置
    STYLES = {
        'button_padding': 8,
        'panel_margin': 10,
        'border_radius': 4,
        'shadow_offset': 2,
    }
    
    @classmethod
    def apply_button_style(cls, button, style='primary'):
        """为按钮应用现代化样式"""
        if style == 'primary':
            button.SetBackgroundColour(cls.COLORS['primary'])
            button.SetForegroundColour(wx.Colour(255, 255, 255))
        elif style == 'secondary':
            button.SetBackgroundColour(cls.COLORS['surface'])
            button.SetForegroundColour(cls.COLORS['text_primary'])
        
        button.SetFont(cls.FONTS['default'])
        return button
    
    @classmethod
    def apply_panel_style(cls, panel):
        """为面板应用现代化样式"""
        panel.SetBackgroundColour(cls.COLORS['surface'])
        return panel
    
    @classmethod
    def apply_text_style(cls, text_ctrl, style='default'):
        """为文本控件应用现代化样式"""
        text_ctrl.SetBackgroundColour(cls.COLORS['surface'])
        text_ctrl.SetForegroundColour(cls.COLORS['text_primary'])
        
        if style == 'search':
            text_ctrl.SetFont(cls.FONTS['default'])
        
        return text_ctrl
    
    @classmethod
    def apply_listbox_style(cls, listbox):
        """为列表框应用现代化样式"""
        listbox.SetBackgroundColour(cls.COLORS['surface'])
        listbox.SetForegroundColour(cls.COLORS['text_primary'])
        listbox.SetFont(cls.FONTS['default'])
        return listbox
    
    @classmethod
    def create_titled_panel(cls, parent, title):
        """创建带标题的面板"""
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(cls.COLORS['surface'])
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 创建标题
        title_text = wx.StaticText(panel, label=title)
        title_text.SetFont(cls.FONTS['subtitle'])
        title_text.SetForegroundColour(cls.COLORS['text_secondary'])
        
        sizer.Add(title_text, 0, wx.ALL | wx.EXPAND, 5)
        
        # 添加分隔线
        line = wx.StaticLine(panel, style=wx.LI_HORIZONTAL)
        line.SetBackgroundColour(cls.COLORS['divider'])
        sizer.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        
        panel.SetSizer(sizer)
        return panel, sizer

class AnimationHelper:
    """动画辅助类 - 提供简单的UI动画效果"""
    
    @staticmethod
    def fade_in(control, duration=300):
        """淡入动画"""
        def on_timer(event):
            opacity = getattr(control, '_opacity', 0)
            opacity += 10
            if opacity >= 255:
                opacity = 255
                timer.Stop()
            setattr(control, '_opacity', opacity)
            control.Refresh()
        
        timer = wx.Timer()
        timer.Bind(wx.EVT_TIMER, on_timer)
        timer.Start(duration // 25)
        return timer
    
    @staticmethod
    def highlight_button(button, duration=200):
        """按钮高亮效果"""
        original_color = button.GetBackgroundColour()
        highlight_color = ModernTheme.COLORS['hover']
        
        button.SetBackgroundColour(highlight_color)
        button.Refresh()
        
        def restore_color():
            button.SetBackgroundColour(original_color)
            button.Refresh()
        
        wx.CallLater(duration, restore_color)

class IconHelper:
    """图标辅助类"""
    
    @staticmethod
    def create_icon_button(parent, label, icon_text="", size=(100, 32)):
        """创建带图标的按钮"""
        button = wx.Button(parent, label=f"{icon_text} {label}", size=size)
        ModernTheme.apply_button_style(button)
        return button
    
    @staticmethod
    def get_file_icon_text(filename):
        """根据文件类型返回对应的图标文本"""
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        
        icon_map = {
            'txt': '📄', 'doc': '📄', 'docx': '📄',
            'pdf': '📕', 'xlsx': '📊', 'xls': '📊',
            'ppt': '📈', 'pptx': '📈',
            'jpg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
            'mp4': '🎬', 'avi': '🎬', 'mov': '🎬',
            'mp3': '🎵', 'wav': '🎵',
            'zip': '📦', 'rar': '📦', '7z': '📦',
            'py': '🐍', 'js': '📜', 'html': '🌐',
        }
        
        return icon_map.get(ext, '📄')