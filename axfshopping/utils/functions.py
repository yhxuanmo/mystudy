from random import choice


def create_ticket():
    s='qwertyuiopasdfghjklzxcvbnm1234567890'
    ticket = ''
    for _ in range(256):
        ticket += choice(s)
    return ticket