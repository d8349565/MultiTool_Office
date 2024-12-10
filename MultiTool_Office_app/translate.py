import requests
import urllib3
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
import threading
from queue import Queue
import time

class TranslateAPI:
    def __init__(self):
        self.session = requests.Session()
        # 添加重试机制
        retry = Retry(total=3, backoff_factor=0.1)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.token_queue = Queue(maxsize=5)
        threading.Thread(target=self._token_manager, daemon=True).start()
    
    def _token_manager(self):
        """预先获取和维护token"""
        while True:
            try:
                if self.token_queue.qsize() < 3:
                    response = self.session.get('https://translate.alibaba.com/api/translate/csrftoken')
                    token = response.json()['token']
                    self.token_queue.put(token)
            except Exception:
                pass
            time.sleep(30)

def translate(text,lang='zh'):
    headers = {
        'referer': 'https://translate.alibaba.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    response = requests.get('https://translate.alibaba.com/api/translate/csrftoken')
    token = response.json()['token']
    headerName = response.json()['headerName']
    cookies = {
        't': token
    }
    headers2 = {
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarydN22oEArThuPSI4m',
        'origin': 'https://translate.alibaba.com',
        'referer': 'https://translate.alibaba.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-xsrf-token_property_item': f'{token}',
    }
    data = f'------WebKitFormBoundarydN22oEArThuPSI4m\r\nContent-Disposition: form-data; name="srcLang"\r\n\r\nauto\r\n------WebKitFormBoundarydN22oEArThuPSI4m\r\nContent-Disposition: form-data; name="tgtLang"\r\n\r\n{lang}\r\n------WebKitFormBoundarydN22oEArThuPSI4m\r\nContent-Disposition: form-data; name="domain"\r\n\r\ngeneral\r\n------WebKitFormBoundarydN22oEArThuPSI4m\r\nContent-Disposition: form-data; name="query"\r\n\r\n{text}\r\n------WebKitFormBoundarydN22oEArThuPSI4m\r\nContent-Disposition: form-data; name="_csrf"\r\n\r\n{token}\r\n------WebKitFormBoundarydN22oEArThuPSI4m--\r\n'.encode()

    response = requests.post('https://translate.alibaba.com/api/translate/text', cookies=cookies, headers=headers2, data=data)
    result = response.json()['data']
    return result['translateText'].replace('&#39;',"'")
    


if __name__ == '__main__':
    text = '你好'
    print(translate(text,'en'))