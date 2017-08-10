import requests
import random

header_phone = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.114 Mobile Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'}
header_pc = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'}
header_disconnect_all = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.114 Mobile Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'}

url_connect_phone = 'https://ipgw.neu.edu.cn/srun_portal_phone.php?ac_id=1&'
url_connect_pc = 'https://ipgw.neu.edu.cn/srun_portal_pc.php?ac_id=1&'
url_disconnect = 'https://ipgw.neu.edu.cn/srun_portal_phone.php?ac_id=1&'
url_disconnect_all = 'https://ipgw.neu.edu.cn/include/auth_action.php'
url_get_info = 'https://ipgw.neu.edu.cn/include/auth_action.php?k='


def connect_phone(uid, psd):
    params = {'action': 'login',
              'ac_id': '1',
              'user_ip': '',
              'nas_ip': '',
              'user_mac': '',
              'username': uid,
              'password': psd}
    r = requests.post(url_connect_phone, data=params, headers=header_phone)
    return r


def connect_pc(uid, psd):
    params = {'action': 'login',
              'ac_id': '1',
              'user_ip': '',
              'nas_ip': '',
              'user_mac': '',
              'url': '',
              'username': uid,
              'password': psd,
              'save_me': '0'}
    r = requests.post(url_connect_pc, data=params, headers=header_pc)
    return r


def disconnect(ip):
    params = {'action': 'auto_logout',
              'user_ip': ip}
    r = requests.post(url_disconnect, data=params, headers=header_phone)
    return r


def disconnect_all(uid, psd):
    params = {'action': 'logout',
              'username': uid,
              'password': psd,
              'ajax': 1}
    r = requests.post(url_disconnect_all, data=params, headers=header_disconnect_all)
    return r


def get_info():
    k = str(random.randint(10000, 99999))
    params = {'action': 'get_online_info',
              'k': k}
    r = requests.post(url_get_info + k, data=params)
    return r