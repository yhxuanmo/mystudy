from myUser import User

class MySystem(object):
    def showWelcome(self):
        print('+--------------------------------------------+')
        print('|                                            |')
        print('|                  欢迎来到                  |')
        print('|                 xxxx通讯录                 |')
        print('|                                            |')
        print('|       1.进入                   2.退出      |')
        print('|                                            |')
        print('+--------------------------------------------+')

    def showMenu(self):
        print('+--------------------------------------------+')
        print('|                1.创建新联系人              |')
        print('|                2.更改联系人                |')
        print('|                3.查询联系人                |')
        print('|                4.显示联系人                |')
        print('|                5.删除联系人                |')
        print('|                6.退出                      |')
        print('+--------------------------------------------+')

    def createUser(self, cursor):
        """
        创建用户
        :param cursor: 连接服务器的对象
        :return:
        """
        uname = input('姓名：')
        if self.isNone(uname):
            return False
        # 创建用户，如果不存在则创建，存在则提示
        if cursor.execute("select 1 from tbuser where uname=%s",(uname,)):
            print('该用户已经存在')
            return False

        utel = input('电话:')
        uaddr = input('地址:')
        uemail = input('邮箱:')
        # user = User(uname, tel=utel, addr=uaddr, email=uemail)
        # 给服务器发送SQL添加数据
        cursor.execute("insert into tbuser (uname, utel, uaddr, uemail) values (%s,%s,%s,%s)", (
                       uname, utel, uaddr, uemail))
        print('添加成功')

    def updateUser(self,cursor):
        """
        更改联系人
        """
        uname = input('姓名：')
        if  not cursor.execute("select 1 from tbuser where uname=%s",(uname,)):
            print('该用户不存在')
            return False
        # 读取对应的用户信息
        cursor.execute("select * from tbuser where uname=%s",(uname,))
        res = cursor.fetchone()
        newName = input('新姓名：')
        newTel = input('新电话：')
        newAddr = input('新住址：')
        newEmail = input('新邮箱：')
        # 如果输入值位空，表示当前信息不做修改
        if newName == '':
            newName= res['uname']
        if newTel == '':
            newTel= res['utel']
        if newAddr == '':
            newAddr= res['uaddr']
        if newEmail == '':
            newEmail= res['uemail']

        cursor.execute("update tbuser set uname=%s,utel=%s,uaddr=%s,uemail=%s where uname=%s",\
        (newName,newTel,newAddr,newEmail,uname))
        print('更新成功')


    def checkUser(self,cursor):
        uname = input('姓名：')
        if  not cursor.execute("select 1 from tbuser where uname=%s",(uname,)):
            print('该用户不存在')
            return False
        cursor.execute("select * from tbuser where uname=%s",(uname,))
        res = cursor.fetchone()
        print('+--------------------------------------------+')
        print('|                 联系人信息                 |')
        print('|'+('姓名:'+res['uname']).center(42) + '|')
        print('|'+('电话:'+(res['utel'] if res['utel'] != None else '空' )).center(42) + '|')
        print('|'+('住址:'+(res['uaddr'] if res['uaddr'] != None else '空') ).center(42) + '|')
        print('|'+('邮箱:'+(res['uemail'] if res['uemail'] != None else '空') ).center(42) + '|')
        print('+--------------------------------------------+')

    def showAllUser(self, cursor):
        """
        显示所有联系人
        """
        cursor.execute('select uname from tbuser')
        res = cursor.fetchone()
        print('+--------------------------------------------+')
        print('|                 所有联系人                 |')
        while res:
            print('|', end='')
            print(res['uname'].center(44),end='')
            print('|')
            res = cursor.fetchone()
        print('+--------------------------------------------+')

    def delUser(self,cursor):
        uname = input('姓名：')
        if not cursor.execute("select 1 from tbuser where uname=%s", (uname,)):
            print('该用户不存在')
            return False
        isSure = input('您确定要删除%s吗？y/n' %(uname))
        if isSure == 'n':
            print('已取消删除')
            return False
        elif isSure == 'y':
            cursor.execute("delete from tbuser where uname=%s",(uname,))
            print('删除成功')
        else:
            print('命令错误，操作取消')
            return False

    def isNone(self,uname):
        if uname == '':
            print('姓名不能为空')
            return True
        return False






