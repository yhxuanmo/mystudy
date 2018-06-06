from random import choice
from datetime import datetime


def create_ticket():
    s='qwertyuiopasdfghjklzxcvbnm1234567890'
    ticket = ''
    for _ in range(256):
        ticket += choice(s)
    return ticket


def create_order_num():
    time = datetime.now()
    order_num = str(time.year)+str(time.month).rjust(2,'0')+str(time.day).rjust(2,'0')
    s = '1234567890'
    for _ in range(8):
        order_num += choice(s)

    return order_num