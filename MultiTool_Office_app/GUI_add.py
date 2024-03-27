import os

import wx
from MultiTool_Office_app.GUI import MyFrame, json
config = wx.Config("MultiTool_Office_app")

class ChildClass(MyFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 调用父类的构造函数
        bSizer161 = wx.BoxSizer(wx.VERTICAL)
        gSizer1 = wx.GridSizer(0, 4, 0, 0)
        bSizer161.Add(gSizer1, 0, wx.EXPAND, 5)

        self.m_panel5.SetSizer(bSizer161)
        self.m_panel5.Layout()
        bSizer161.Fit(self.m_panel5)
        self.m_textCtrl7 = wx.TextCtrl(self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)
        bSizer161.Add(self.m_textCtrl7, 1, wx.ALL | wx.EXPAND, 5)
        for i in range(12):
            button = wx.Button(self.m_panel5, label=f"按钮 {i + 1}")
            gSizer1.Add(button, 0, wx.ALL | wx.EXPAND, 5)
            button.Bind(wx.EVT_MOUSEWHEEL, self.bind_file)
            button.Bind(wx.EVT_LEFT_DOWN, self.run)
            button.Bind(wx.EVT_RIGHT_DOWN, self.rename_button)

        self.m_notebook8.AddPage(self.m_panel5, u"其他独立程序", True)
        self.m_panel1.Layout()
        self.Layout()
        self.Centre(wx.BOTH)

        children = self.m_panel5.GetChildren()
        for child in children:
            if isinstance(child, wx.Button):
                new_name = config.Read(str(child.Id))
                if new_name:
                    child.SetLabel(config.Read(str(child.Id)))

    def __del__(self):
        pass
    def bind_file(self, event):
        Id = str(event.GetId())
        with wx.FileDialog(None, "选择文件", wildcard="所有文件 (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_OK:
                selected_file = file_dialog.GetPath()
        if selected_file:
            with open('MultiTool_Office_app\\settings.json', 'r') as file:
                data = json.load(file)
                data[Id] = selected_file
            with open('MultiTool_Office_app\\settings.json', 'w') as file:
                json.dump(data, file)

    def run(self, event):
        Id = str(event.GetId())
        with open('MultiTool_Office_app\\settings.json', 'r') as file:
            data = json.load(file)
            path = data[Id]
            # os.chdir(os.path.dirname(os.path.abspath(__file__)))
            os.startfile(path)

    def rename_button(self, event):
        Id = event.GetId()
        with wx.TextEntryDialog(None, "请输入需要修改的名称", "新的命名", style=wx.OK | wx.CANCEL) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                entered_text = dialog.GetValue()
                button_obj = self.FindWindowById(Id)  # 通过 ID 获取按钮对象
                if button_obj:
                    button_obj.SetLabel(entered_text)  # 修改按钮的标签属性
                    config.Write(str(Id),entered_text)
