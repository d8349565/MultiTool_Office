import os
import wx.xrc
import json
wx = wx
xrc = wx.xrc

with open('MultiTool_Office_app\\settings.json', 'r') as file:
    data = json.load(file)
root_dirs = data['root_dirs']
root_dirs_dict = {os.path.basename(i): i for i in root_dirs}
