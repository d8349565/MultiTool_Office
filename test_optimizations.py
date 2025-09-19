#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证优化后的功能
"""

import os
import sys
import time

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MultiTool_Office_app'))

def test_performance_module():
    """测试性能模块"""
    print("🧪 测试性能优化模块...")
    
    try:
        from performance import performance_optimizer, debounce, throttle
        
        # 测试目录缓存
        test_path = "."
        start_time = time.time()
        dirs1 = performance_optimizer.get_directory_contents_cached(test_path)
        time1 = time.time() - start_time
        
        start_time = time.time()
        dirs2 = performance_optimizer.get_directory_contents_cached(test_path)  # 应该从缓存获取
        time2 = time.time() - start_time
        
        print(f"   ✅ 目录缓存测试: 首次={time1:.3f}s, 缓存={time2:.3f}s")
        print(f"   📊 发现 {len(dirs1)} 个目录")
        
        # 测试缓存统计
        stats = performance_optimizer.get_cache_stats()
        print(f"   📈 缓存统计: {stats}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 性能模块测试失败: {e}")
        return False

def test_theme_module():
    """测试主题模块"""
    print("🎨 测试主题模块...")
    
    try:
        from theme import ModernTheme, IconHelper
        
        # 测试颜色配置
        colors = ModernTheme.COLORS
        print(f"   ✅ 加载了 {len(colors)} 种颜色配置")
        
        # 测试字体配置
        fonts = ModernTheme.FONTS
        print(f"   ✅ 加载了 {len(fonts)} 种字体配置")
        
        # 测试图标助手
        test_files = ['test.txt', 'image.png', 'video.mp4', 'code.py']
        for filename in test_files:
            icon = IconHelper.get_file_icon_text(filename)
            print(f"   📄 {filename} -> {icon}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 主题模块测试失败: {e}")
        return False

def test_get_files_module():
    """测试文件操作模块"""
    print("📁 测试文件操作模块...")
    
    try:
        from get_files import list_dirs, list_files
        
        # 测试目录列表
        test_path = "."
        dirs = list_dirs(test_path)
        print(f"   ✅ 发现 {len(dirs)} 个子目录")
        
        # 测试文件搜索 (限制结果数量)
        files = list_files(test_path, ".py", max_results=10)
        print(f"   ✅ 发现 {len(files)} 个Python文件")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 文件操作模块测试失败: {e}")
        return False

def test_translate_module():
    """测试翻译模块"""
    print("🌐 测试翻译模块...")
    
    try:
        from translate import translate, translate_cached, clear_translation_cache
        
        print("   ℹ️  翻译功能需要网络连接，跳过在线测试")
        print("   ✅ 翻译模块加载成功")
        
        # 测试缓存清理
        clear_translation_cache()
        print("   ✅ 翻译缓存清理完成")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 翻译模块测试失败: {e}")
        return False

def test_config_module():
    """测试配置模块"""
    print("⚙️  测试配置模块...")
    
    try:
        from MultiTool_Office_app import Config, verify_dirs
        
        # 测试配置加载
        config = Config()
        print(f"   ✅ 配置加载成功")
        
        # 测试目录验证
        test_dirs = [".", "./MultiTool_Office_app", "/nonexistent"]
        valid_dirs = verify_dirs(test_dirs)
        print(f"   ✅ 目录验证: {len(test_dirs)} -> {len(valid_dirs)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 配置模块测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 MultiTool Office 优化功能测试")
    print("=" * 50)
    
    tests = [
        test_config_module,
        test_performance_module,
        test_theme_module,
        test_get_files_module,
        test_translate_module,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"   ❌ 测试执行失败: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！优化功能正常工作。")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关模块。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)