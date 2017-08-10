import net, findip, formatInfo, users
import requests, sys

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
            r = net.connect_pc(uid, psd)
        elif cmd == 'connect phone':
            r = net.connect_phone(uid, psd)
        elif cmd == 'disconnect all':
            r = net.disconnect_all(uid, psd)
        elif cmd == 'disconnect':
            r = net.disconnect(findip.find_ip())
        else:
            print("未知命令")
            return -2

        ans = r.content.decode()
        for i in range(0, len(msgs)):
            if ans.find(msgs[i]) != -1:
                print(msgs[i])
                return i
        return -1


def show_info():
    r = net.get_info()
    if r.status_code == requests.codes.ok:
        # 45278986,13189,45.00,,0,58.154.209.141
        # 流量，时长，余额，，0，IP地址
        m = r.content.decode().split(',')
        print("已用流量: " + formatInfo.format_flux(m[0]))
        print("已用时间: " + formatInfo.format_time(m[1]))
        print("当前余额: " + m[2] + '元')
        print("IP地址: " + m[5])


def loop():
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

def l_get(l, i):
    try:
        return l[i]
    except:
        return None

if __name__ == '__main__':
    '''
    ipgw [-p] connect [<user id>] 
    ipgw [-sdp] connect <user id> <password>  
    ipgw disconnect [all]
    ipgw disconnect all <user id> [<password>]
    ipgw show info
    ipgw show users
    ipgw user del <user id>
    ipgw user add <user id> <password>
    ipgw user change <user id> <new password>
    ipgw set default <user id>
    '''
    if len(sys.argv) == 1:
        loop()
    else:
        user = users.UserList()
        phone = save = setDefault = False
        if sys.argv[1][0] == '-':  # 如果第一个参数是以-开头, 视为是命令项
            setting = sys.argv[1]
            if 's' in setting:
                save = True
            if 'd' in setting:
                setDefault = True
            if 'p' in setting:
                phone = True
            arg1 = l_get(sys.argv, 2)
            arg2 = l_get(sys.argv, 3)
            arg3 = l_get(sys.argv, 4)
            arg4 = l_get(sys.argv, 5)
        else:
            arg1 = l_get(sys.argv, 1)
            arg2 = l_get(sys.argv, 2)
            arg3 = l_get(sys.argv, 3)
            arg4 = l_get(sys.argv, 4)

        if arg1 == 'set':
            if arg2 == 'default':
                user.is_exists(arg3)
                user.set_default(arg3)
            else:
                raise Exception("无法识别的参数:" + arg2)
        elif arg1 == 'user':
            if arg2 == 'del':
                user.is_exists(sys.argv[3])
                user.del_user(sys.argv[3])
            elif arg2 == 'add':
                user.add_user(arg3, arg4)
            elif arg2 == 'change':
                user.add_user(arg3, arg4)
            else:
                raise Exception("无法识别的参数:" + arg2)
        elif arg1 == 'show':
            if arg2 == 'info':
                show_info()
            elif arg2 == 'users':
                user.show()
            else:
                raise Exception("无法识别的参数:" + arg2)
        elif arg1 == 'disconnect':
            if arg2 is None:
                operate('disconnect', user.current, user.get_current_password())
            elif arg2 == 'all':
                if arg3 is not None:
                    if arg4 is not None:
                        operate('disconnect all', arg3, arg4)
                    else:
                        operate('disconnect all', sys.argv[3], user.get_password(sys.argv[3]))
                else:
                    operate('disconnect all', user.current, user.get_current_password())
            else:
                raise Exception("无法识别的参数:" + arg2)

        elif arg1 == 'connect':
            if arg2 is not None and arg3 is not None:
                if phone:
                    operate('connect phone', arg2, arg3)
                else:
                    operate('connect pc', arg2, arg3)
                if save:
                    user.add_user(arg2, arg3)
                if setDefault:
                    user.set_default(arg2)
                user.save()
            else:
                if arg2 is not None:
                    if phone:
                        operate('connect phone', arg2, user.get_password(arg2))
                    else:
                        operate('connect pc', arg2, user.get_password(arg2))
                else:
                    if phone:
                        operate('connect phone', arg2, user.get_password(arg2))
                    else:
                        operate('connect pc', user.current, user.get_current_password())
        else:
            raise Exception("无法识别的参数:" + arg1)