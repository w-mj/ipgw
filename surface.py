import ipgw, findip, formatInfo, users
import requests

msgs = [r'Authentication failed',
        r'无法登录',
        r'You are already online',
        r'密码错误',
        r'网络已断开',
        r'网络已连接',
        r'注销成功',
        r'无法连接到IPGW网关',
        r'内部服务器错误',
        r'未知的主机异常',
        r'phone连接成功',
        r'您似乎未曾连接到网络',
        r'用户不存在',
        r'已欠费',
        r'操作不合法',
        r'操作失败']


def operate(cmd, uid, psd):
    while True:
        print("Input operate")
        if cmd == 'connect pc':
            r = ipgw.connect_pc(uid, psd)
        elif cmd == 'connect phone':
            r = ipgw.connect_phone(uid, psd)
        elif cmd == 'disconnect all':
            r = ipgw.disconnect_all(uid, psd)
        elif cmd == 'disconnect':
            r = ipgw.disconnect(findip.find_ip())
        else:
            r = None

        ans = r.content.decode()
        for i in range(0, len(msgs)):
            if ans.find(msgs[i]) != -1:
                return i
        return -1


def show_info():
    r = ipgw.get_info()
    if r.status_code == requests.codes.ok:
        # 45278986,13189,45.00,,0,58.154.209.141
        # 流量，时长，余额，，0，IP地址
        m = r.content.decode().split(',')
        print("已用流量: " + formatInfo.format_flux(m[0]))
        print("已用时间: " + formatInfo.format_time(m[1]))
        print("当前余额: " + m[2] + '元')
        print("IP地址: " + m[5])


if __name__ == '__main__':
    user = users.UserList()
    while True:
        cmd = input('input operation')
        sp = cmd.split(' ')
        if sp[0] == 'disconnect' or sp[0] == 'connect':
            result = operate(cmd, user.current, user.get_current_password())
            print(msgs[result])
        elif cmd == 'show info':
            show_info()
        elif cmd == 'show users':
            for x in user.user_list:
                print(x)
        elif cmd == 'add user':
            uid = input("输入账号: ")
            psd = input("输入密码: ")
            user.add_user(uid, psd)
            user.save()
        elif cmd == 'del user':
            uid = input("输入账号: ")
            user.del_user(uid)
            user.save()
        elif cmd == 'change password':
            uid = input("输入账号: ")
            psd = input("输入新密码: ")
            user.change_password(uid, psd)
        elif cmd == 'change default':
            uid = input("输入账号: ")
            user.set_default(uid)
        elif cmd == 'change current':
            uid = input("输入账号")
            user.set_current(uid)
        elif cmd == 'exit':
            break
