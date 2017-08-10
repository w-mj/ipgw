import requests
import re


# 找到自己的IP地址
# return: tuple result
# result[0]: 由http://pv.sohu.com/cityjson返回的IP地址
# result[1]: 由http://geoip.neu.edu.cn/返回的IP地址
def find_ip():
    regular = re.compile(r'((25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9]).){3}(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])')
    # 匹配IP地址
    r = requests.get('http://pv.sohu.com/cityjson')
    if r.status_code == requests.codes.ok:
        result0 = regular.search(r.text)
    else:
        result0 = None
    r = requests.get('http://geoip.neu.edu.cn/')
    if r.status_code == requests.codes.ok:
        result1 = regular.search(r.text)
    else:
        result1 = None
    return result0, result1


if __name__ == '__main__':
    print(find_ip())