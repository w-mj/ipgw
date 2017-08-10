import encrypt



class UserList:

    def __init__(self):
        self.user_list = dict()
        self.default = ""
        self.current = ""
        self.load()

    def load(self):
        self.user_list.clear()
        try:
            f = open('passwd', 'r') # 以只读方式打开文件
            self.default = f.readline().split('\n')[0]
            self.current = self.default
            for line in f:
                filed = line.split('\n')[0].split(' ')
                self.user_list[filed[0]] = filed[1]
            f.close()
        except FileNotFoundError:
            print("创建新的存档")

    def save(self):
        f = open('passwd', 'w')
        f.write(self.default + '\n')
        for uid, psd in self.user_list.items():
            f.writelines(uid + ' ' + psd + '\n')
        f.close()

    def     is_exists(self, uid):
        t = self.user_list.get(uid)
        if t is None:
            raise Exception("没有这个用户")

    def change_password(self, uid, psd):
        self.is_exists(uid)
        self.user_list[uid] = encrypt.encrypt(uid, psd)

    def add_user(self, uid, psd):
        t = self.user_list.get(uid)
        if t is None:
            self.user_list[uid] = encrypt.encrypt(uid, psd)
            if len(self.user_list) == 1:
                self.default = uid
                self.current = uid
        else:
            raise Exception("该用户已经存在")

    def del_user(self, uid):
        del self.user_list[uid]

    def get_password(self, uid):
        self.is_exists(uid)
        return encrypt.decrypt(uid, self.user_list[uid])

    def set_default(self, uid):
        self.default = uid

    def set_current(self, uid):
        self.current = uid

    def get_current_password(self):
        return self.get_password(self.current)

    def show(self):
        for x in self.user_list:
            print(x)

