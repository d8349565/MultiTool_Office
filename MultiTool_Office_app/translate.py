import requests

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