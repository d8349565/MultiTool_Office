import requests
import urllib3
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
import threading
from queue import Queue
import time
import json
from functools import lru_cache

class TranslateAPI:
    """翻译API管理类 - 优化版本"""
    
    def __init__(self):
        self.session = requests.Session()
        # 添加重试机制
        retry = Retry(
            total=3, 
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # 设置合理的超时时间
        self.session.timeout = (5, 10)  # 连接超时5秒，读取超时10秒
        
        # Token缓存队列
        self.token_queue = Queue(maxsize=5)
        self.token_manager_running = False
        self._start_token_manager()
    
    def _start_token_manager(self):
        """启动token管理器"""
        if not self.token_manager_running:
            self.token_manager_running = True
            threading.Thread(target=self._token_manager, daemon=True).start()
    
    def _token_manager(self):
        """预先获取和维护token"""
        while True:
            try:
                # 保持队列中有足够的token
                if self.token_queue.qsize() < 3:
                    response = self.session.get(
                        'https://translate.alibaba.com/api/translate/csrftoken',
                        timeout=10
                    )
                    if response.status_code == 200:
                        token_data = response.json()
                        if 'token' in token_data:
                            self.token_queue.put(token_data['token'])
            except Exception:
                pass
            time.sleep(30)  # 每30秒检查一次
    
    def get_token(self):
        """获取可用的token"""
        try:
            # 首先尝试从队列获取
            if not self.token_queue.empty():
                return self.token_queue.get_nowait()
        except:
            pass
        
        # 如果队列为空，直接请求
        try:
            response = self.session.get(
                'https://translate.alibaba.com/api/translate/csrftoken',
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get('token')
        except Exception:
            pass
        return None

# 全局翻译API实例
translate_api = TranslateAPI()

@lru_cache(maxsize=100)
def translate_cached(text, lang='zh'):
    """带缓存的翻译函数"""
    return translate(text, lang)

def translate(text, lang='zh'):
    """优化的翻译函数"""
    if not text or not text.strip():
        return ""
    
    # 文本长度限制
    if len(text) > 5000:
        return "文本过长，请分段翻译"
    
    try:
        # 获取token
        token = translate_api.get_token()
        if not token:
            return "获取翻译token失败，请稍后重试"
        
        # 准备请求头
        headers = {
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarydN22oEArThuPSI4m',
            'origin': 'https://translate.alibaba.com',
            'referer': 'https://translate.alibaba.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-xsrf-token_property_item': token,
        }
        
        # 准备请求数据
        data = f'''------WebKitFormBoundarydN22oEArThuPSI4m\r
Content-Disposition: form-data; name="srcLang"\r
\r
auto\r
------WebKitFormBoundarydN22oEArThuPSI4m\r
Content-Disposition: form-data; name="tgtLang"\r
\r
{lang}\r
------WebKitFormBoundarydN22oEArThuPSI4m\r
Content-Disposition: form-data; name="domain"\r
\r
general\r
------WebKitFormBoundarydN22oEArThuPSI4m\r
Content-Disposition: form-data; name="query"\r
\r
{text}\r
------WebKitFormBoundarydN22oEArThuPSI4m\r
Content-Disposition: form-data; name="_csrf"\r
\r
{token}\r
------WebKitFormBoundarydN22oEArThuPSI4m--\r
'''.encode('utf-8')
        
        # 设置cookies
        cookies = {'t': token}
        
        # 发送翻译请求
        response = translate_api.session.post(
            'https://translate.alibaba.com/api/translate/text',
            cookies=cookies,
            headers=headers,
            data=data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'data' in result and 'translateText' in result['data']:
                translated_text = result['data']['translateText']
                # 处理HTML实体
                translated_text = translated_text.replace('&#39;', "'")
                translated_text = translated_text.replace('&quot;', '"')
                translated_text = translated_text.replace('&amp;', '&')
                translated_text = translated_text.replace('&lt;', '<')
                translated_text = translated_text.replace('&gt;', '>')
                return translated_text
            else:
                return "翻译响应格式错误"
        else:
            return f"翻译服务响应错误: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "翻译请求超时，请检查网络连接"
    except requests.exceptions.ConnectionError:
        return "网络连接错误，请检查网络设置"
    except requests.exceptions.RequestException as e:
        return f"翻译请求失败: {str(e)}"
    except json.JSONDecodeError:
        return "翻译响应解析失败"
    except Exception as e:
        return f"翻译过程发生未知错误: {str(e)}"

def translate_async(text, lang='zh', callback=None):
    """异步翻译函数"""
    def translate_task():
        try:
            result = translate(text, lang)
            if callback:
                callback(result)
        except Exception as e:
            if callback:
                callback(f"翻译失败: {str(e)}")
    
    # 使用线程池执行翻译任务
    threading.Thread(target=translate_task, daemon=True).start()

def clear_translation_cache():
    """清空翻译缓存"""
    translate_cached.cache_clear()

if __name__ == '__main__':
    # 测试翻译功能
    test_texts = [
        ('你好', 'en'),
        ('Hello', 'zh'),
        ('こんにちは', 'zh')
    ]
    
    for text, target_lang in test_texts:
        result = translate(text, target_lang)
        print(f"{text} -> {result}")
        
    # 测试缓存
    print("\n测试缓存:")
    start_time = time.time()
    result1 = translate_cached('你好', 'en')
    time1 = time.time() - start_time
    
    start_time = time.time()
    result2 = translate_cached('你好', 'en')  # 应该从缓存获取
    time2 = time.time() - start_time
    
    print(f"首次翻译: {result1} (耗时: {time1:.3f}s)")
    print(f"缓存翻译: {result2} (耗时: {time2:.3f}s)")