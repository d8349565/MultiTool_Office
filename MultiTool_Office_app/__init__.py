import os
import wx.xrc
import json
from pathlib import Path

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config_path = Path('MultiTool_Office_app/settings.json')
            self.load_config()
            self.initialized = True
    
    def load_config(self):
        try:
            if self.config_path.exists():
                with self.config_path.open('r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = self.get_default_config()
        except Exception:
            self.data = self.get_default_config()
            
    @staticmethod
    def get_default_config():
        return {
            "root_dirs": ["./"],
            "size_x": 700,
            "size_y": 600
        }

wx = wx
xrc = wx.xrc

def verify_dirs(dirs):
    """验证目录是否存在，如果不存在则返回默认目录"""
    valid_dirs = []
    for dir_path in dirs:
        if os.path.exists(dir_path):
            valid_dirs.append(dir_path)
    return valid_dirs if valid_dirs else ["."]

try:
    with open('MultiTool_Office_app\\settings.json', 'r') as file:
        data = json.load(file)
    root_dirs = verify_dirs(data.get('root_dirs', ["."]))
    root_dirs_dict = {os.path.basename(i): i for i in root_dirs}
except Exception as e:
    print(f"配置加载错误: {e}")
    root_dirs = ["."]
    root_dirs_dict = {".": "."}
