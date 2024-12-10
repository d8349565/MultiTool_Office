import os
from concurrent.futures import ThreadPoolExecutor


def list_files(start_path, flag=''):
    if not os.path.exists(start_path):
        return []
        
    results = []
    
    def scan_directory(path):
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if flag in file:
                        results.append(os.path.join(root, file))
        except (PermissionError, FileNotFoundError):
            pass
            
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(scan_directory, start_path)
        
    return results


def list_dirs(start_path):
    if not os.path.exists(start_path):
        return []
        
    try:
        _, dirs, _ = next(os.walk(start_path))
        return sorted(dirs)
    except (PermissionError, FileNotFoundError):
        return []
