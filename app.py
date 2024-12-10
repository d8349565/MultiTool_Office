import wx
from MultiTool_Office_app.GUI_add import ChildClass
import multiprocessing

def main():
    app = wx.App()
    frame = ChildClass(None)
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    # Windows下使用multiprocessing需要这样启动
    multiprocessing.freeze_support()
    main()


# pyinstaller -F --noconsole app.py -i MultiTool_Office_app\图片1.png 使用这个打包
# pyinstaller --onedir --noconsole app.py -i MultiTool_Office_app\favicon.icoc
# .\venv\Scripts\activate # 激活虚拟环境
# pip freeze > requirements.txt