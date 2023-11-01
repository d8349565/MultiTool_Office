from MultiTool_Office_app import wx
from MultiTool_Office_app.GUI import MyFrame

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()

# pyinstaller --onefile --noconsole F:\Python_files\MultiTool_Office\app.py
# pyinstaller -F --noconsole app.py -i MultiTool_Office_app\图片1.png
