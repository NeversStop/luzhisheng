from urllib.parse import quote
import http.client
import requests
import json


conn = http.client.HTTPSConnection("www.douyin.com")


def get_ac_nonce(encoded_text):
    url = f"/search/{encoded_text}?source=normal_search&type=user"
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
                  'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }
    conn.request("GET", url=url, headers=headers)
    response = conn.getresponse()
    print(response.read().decode())
    cookie_dict = get_cookie_dict(response)
    __ac_nonce = cookie_dict.get('__ac_nonce')
    conn.close()
    return __ac_nonce


def get_ac_signature(__ac_nonce):
    url = "http://192.168.2.144:3005/_ac_signature"
    payload = json.dumps({"_ac_nonce": __ac_nonce})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def get_ttwid(ac_nonce, __ac_signature, encoded_text):
    url = f"/search/{encoded_text}?source=normal_search&type=user"
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': f'__ac_nonce={ac_nonce}; __ac_signature={__ac_signature};',
        'pragma': 'no-cache',
        'referer': f'https://www.douyin.com/search/{encoded_text}?source=normal_search&type=user',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }
    print(headers['cookie'])
    conn.request("GET", url=url, headers=headers)
    response = conn.getresponse()
    # print(response.read().decode())
    try:
        cookie_dict = get_cookie_dict(response)
        ttwid = cookie_dict.get('ttwid')
        conn.close()
        return ttwid
    except Exception as e:
        print(f"报错{e}")


def get_cookie_dict(response):
    cookies_dict = {}
    if response.getheader("Set-Cookie"):
        cookie_str = response.getheader("Set-Cookie").replace('secure, ', '')
        cookies_list = cookie_str.split(";")
        for cookie in cookies_list:
            if "=" in cookie.strip():
                name, value = cookie.strip().split("=", 1)
                cookies_dict[name] = value
        return cookies_dict
    else:
        raise ValueError('Set-Cookie为空')


if __name__ == '__main__':
    search_keyword = '半斤塘口'
    encoded_text = quote(search_keyword)
    __ac_nonce = get_ac_nonce(encoded_text)
    print(__ac_nonce)
    # __ac_signature = get_ac_signature(__ac_nonce)
    # print(__ac_signature)
    ttwid = get_ttwid('064ce080e00b43ebb7c7c', '02B4Z6wo00f01UE5LIwAAIDCvsbTcD0Pl91BGygAAFBT', encoded_text)
    print(ttwid)
