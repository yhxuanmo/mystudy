from time import sleep
import pymysql

from mysystem import MySystem
from myUser import User


def choiseFunction(uinput, mysystem, conn, cursor):
    if uinput == '1':
        mysystem.createUser(cursor)
        conn.commit()
    elif uinput == '2':
        mysystem.updateUser(cursor)
        conn.commit()
    elif uinput == '3':
        mysystem.checkUser(cursor)
    elif uinput == '4':
        mysystem.showAllUser(cursor)
    elif uinput == '5':
        mysystem.delUser(cursor)
        conn.commit()
    elif uinput == '6':
        return False
    return True

def main():
    mysystem = MySystem()
    # mysystem.showWelcome()
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='123456', charset='utf8',
                           db='contacts', cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            isGo = True
            while isGo:
                mysystem.showMenu()
                uinput = input('请输入操作：')
                isGo = choiseFunction(uinput, mysystem,conn , cursor)
                # sleep(1)

    finally:
        cursor.close()




if __name__ == '__main__':
    main()
