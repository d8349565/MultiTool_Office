import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from .performance import performance_optimizer, debounce, throttle


def list_files(start_path, flag='', max_results=1000):
    """优化的文件列表获取函数"""
    if not os.path.exists(start_path):
        return []
    
    # 使用性能优化器的搜索功能
    return performance_optimizer.search_files_optimized(start_path, flag, max_results)


def list_dirs(start_path):
    """优化的目录列表获取函数"""
    if not os.path.exists(start_path):
        return []
    
    # 使用性能优化器的缓存目录功能
    return performance_optimizer.get_directory_contents_cached(start_path)


@debounce(wait_time=0.3)
def list_files_debounced(start_path, flag='', callback=None):
    """防抖版本的文件搜索，避免频繁搜索"""
    def search_task():
        try:
            results = list_files(start_path, flag)
            if callback:
                callback(results)
        except Exception as e:
            if callback:
                callback([])
    
    # 异步执行搜索
    performance_optimizer.executor.submit(search_task)


def list_dirs_async(start_path, callback):
    """异步获取目录列表"""
    performance_optimizer.get_directory_contents_async(start_path, callback)


def batch_scan_directories(paths, flag=''):
    """批量扫描多个目录"""
    all_results = []
    
    def scan_single_dir(path):
        return list_files(path, flag)
    
    # 使用批量操作优化
    results = performance_optimizer.batch_operation(paths, scan_single_dir)
    
    for result in results:
        if isinstance(result, list):
            all_results.extend(result)
    
    return all_results


def get_file_info_optimized(file_path):
    """获取优化的文件信息"""
    try:
        stat = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'is_dir': os.path.isdir(file_path),
            'extension': os.path.splitext(file_path)[1].lower()
        }
    except (OSError, FileNotFoundError):
        return None


def scan_directory_with_progress(start_path, progress_callback=None, flag=''):
    """带进度回调的目录扫描"""
    if not os.path.exists(start_path):
        return []
    
    results = []
    total_dirs = 0
    processed_dirs = 0
    
    # 首先计算总目录数（用于进度计算）
    try:
        for root, dirs, _ in os.walk(start_path):
            total_dirs += 1
            if total_dirs > 1000:  # 限制最大扫描目录数
                break
    except Exception:
        total_dirs = 1
    
    # 实际扫描
    try:
        for root, dirs, files in os.walk(start_path):
            processed_dirs += 1
            
            # 更新进度
            if progress_callback and total_dirs > 0:
                progress = min(100, int((processed_dirs / total_dirs) * 100))
                progress_callback(progress)
            
            # 处理文件
            for file in files:
                if not flag or flag.lower() in file.lower():
                    results.append(os.path.join(root, file))
            
            # 限制扫描深度和数量
            depth = root.replace(start_path, '').count(os.sep)
            if depth > 4 or len(results) > 2000:
                break
                
    except Exception:
        pass
    
    if progress_callback:
        progress_callback(100)  # 完成
    
    return results
