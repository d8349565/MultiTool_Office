# -*- coding: utf-8 -*-
"""
性能优化模块 - 提供缓存、异步操作和内存优化功能
"""
import os
import threading
import time
from functools import lru_cache, wraps
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, Empty
import weakref
import gc

class PerformanceOptimizer:
    """性能优化器 - 管理缓存、线程池和内存优化"""
    
    def __init__(self, max_workers=4, cache_size=128):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.cache_size = cache_size
        self._dir_cache = {}
        self._file_cache = {}
        self._cache_timestamps = {}
        self.cache_expire_time = 300  # 5分钟缓存过期
        
        # 启动缓存清理线程
        self._start_cache_cleaner()
    
    def _start_cache_cleaner(self):
        """启动缓存清理线程"""
        def cache_cleaner():
            while True:
                try:
                    current_time = time.time()
                    expired_keys = []
                    
                    for key, timestamp in self._cache_timestamps.items():
                        if current_time - timestamp > self.cache_expire_time:
                            expired_keys.append(key)
                    
                    for key in expired_keys:
                        self._dir_cache.pop(key, None)
                        self._file_cache.pop(key, None)
                        self._cache_timestamps.pop(key, None)
                    
                    # 强制垃圾回收
                    if len(expired_keys) > 10:
                        gc.collect()
                    
                    time.sleep(60)  # 每分钟清理一次
                    
                except Exception:
                    pass
        
        cleaner_thread = threading.Thread(target=cache_cleaner, daemon=True)
        cleaner_thread.start()
    
    def get_directory_contents_async(self, path, callback):
        """异步获取目录内容"""
        def task():
            try:
                result = self.get_directory_contents_cached(path)
                wx.CallAfter(callback, result)
            except Exception as e:
                wx.CallAfter(callback, [])
        
        self.executor.submit(task)
    
    def get_directory_contents_cached(self, path):
        """获取目录内容（带缓存）"""
        if not os.path.exists(path):
            return []
        
        # 检查缓存
        cache_key = f"dir_{path}"
        current_time = time.time()
        
        if cache_key in self._dir_cache:
            cached_time = self._cache_timestamps.get(cache_key, 0)
            if current_time - cached_time < self.cache_expire_time:
                return self._dir_cache[cache_key]
        
        # 获取目录内容
        try:
            dirs = []
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        dirs.append(entry.name)
            
            dirs.sort()
            
            # 更新缓存
            self._dir_cache[cache_key] = dirs
            self._cache_timestamps[cache_key] = current_time
            
            return dirs
            
        except (PermissionError, FileNotFoundError, OSError):
            return []
    
    def search_files_optimized(self, start_path, pattern="", max_results=1000):
        """优化的文件搜索"""
        if not os.path.exists(start_path):
            return []
        
        cache_key = f"files_{start_path}_{pattern}"
        current_time = time.time()
        
        # 检查缓存
        if cache_key in self._file_cache:
            cached_time = self._cache_timestamps.get(cache_key, 0)
            if current_time - cached_time < self.cache_expire_time:
                return self._file_cache[cache_key]
        
        results = []
        count = 0
        
        try:
            for root, dirs, files in os.walk(start_path):
                # 限制搜索深度，避免过度深入
                depth = root.replace(start_path, '').count(os.sep)
                if depth > 5:  # 最大深度5层
                    dirs.clear()
                    continue
                
                for file in files:
                    if count >= max_results:
                        break
                    
                    if pattern.lower() in file.lower():
                        file_path = os.path.join(root, file)
                        results.append(file_path)
                        count += 1
                
                if count >= max_results:
                    break
                    
        except (PermissionError, FileNotFoundError, OSError):
            pass
        
        # 更新缓存
        self._file_cache[cache_key] = results
        self._cache_timestamps[cache_key] = current_time
        
        return results
    
    def batch_operation(self, items, operation, batch_size=50):
        """批量操作优化"""
        results = []
        
        def process_batch(batch):
            batch_results = []
            for item in batch:
                try:
                    result = operation(item)
                    batch_results.append(result)
                except Exception:
                    continue
            return batch_results
        
        # 分批处理
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            future = self.executor.submit(process_batch, batch)
            try:
                batch_results = future.result(timeout=5)  # 5秒超时
                results.extend(batch_results)
            except Exception:
                continue
        
        return results
    
    def clear_cache(self):
        """清空所有缓存"""
        self._dir_cache.clear()
        self._file_cache.clear()
        self._cache_timestamps.clear()
        gc.collect()
    
    def get_cache_stats(self):
        """获取缓存统计信息"""
        return {
            'dir_cache_size': len(self._dir_cache),
            'file_cache_size': len(self._file_cache),
            'total_cached_items': len(self._cache_timestamps)
        }

class LazyLoader:
    """延迟加载器 - 用于大量数据的分页加载"""
    
    def __init__(self, data_source, page_size=50):
        self.data_source = data_source
        self.page_size = page_size
        self.current_page = 0
        self._loaded_data = []
        self._total_pages = 0
    
    def load_next_page(self):
        """加载下一页数据"""
        if callable(self.data_source):
            # 如果数据源是函数，调用它获取数据
            start_idx = self.current_page * self.page_size
            end_idx = start_idx + self.page_size
            
            try:
                page_data = self.data_source(start_idx, end_idx)
                if page_data:
                    self._loaded_data.extend(page_data)
                    self.current_page += 1
                    return page_data
            except Exception:
                pass
        else:
            # 如果数据源是列表，直接切片
            start_idx = self.current_page * self.page_size
            end_idx = start_idx + self.page_size
            
            if start_idx < len(self.data_source):
                page_data = self.data_source[start_idx:end_idx]
                self._loaded_data.extend(page_data)
                self.current_page += 1
                return page_data
        
        return []
    
    def reset(self):
        """重置加载器"""
        self.current_page = 0
        self._loaded_data.clear()
    
    def get_loaded_data(self):
        """获取已加载的所有数据"""
        return self._loaded_data.copy()

def debounce(wait_time=0.5):
    """防抖装饰器 - 防止频繁调用"""
    def decorator(func):
        timer = None
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal timer
            
            def delayed_call():
                func(*args, **kwargs)
            
            if timer:
                timer.cancel()
            
            timer = threading.Timer(wait_time, delayed_call)
            timer.start()
        
        return wrapper
    return decorator

def throttle(interval=1.0):
    """节流装饰器 - 限制调用频率"""
    def decorator(func):
        last_called = [0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if current_time - last_called[0] >= interval:
                last_called[0] = current_time
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

class MemoryMonitor:
    """内存监视器"""
    
    @staticmethod
    def get_memory_usage():
        """获取当前内存使用情况"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            return {
                'rss': memory_info.rss / 1024 / 1024,  # MB
                'vms': memory_info.vms / 1024 / 1024,  # MB
            }
        except ImportError:
            return {'rss': 0, 'vms': 0}
    
    @staticmethod
    def force_garbage_collection():
        """强制垃圾回收"""
        collected = gc.collect()
        return collected

# 全局性能优化器实例
performance_optimizer = PerformanceOptimizer()

# 导入wx用于CallAfter
try:
    import wx
except ImportError:
    # 如果wx不可用，提供一个简单的替代
    class MockWx:
        @staticmethod
        def CallAfter(func, *args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                pass
    wx = MockWx()