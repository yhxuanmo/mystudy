class User(object):
    def __init__(self, name, tel=None, addr=None, email=None):
        self._name = name
        self._tel = tel
        self._addr = addr
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name

    @property
    def tel(self):
        return self._tel

    @tel.setter
    def tel(self, tel):
        self._tel = tel

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, addr):
        self._addr = addr

    @property
    def email(self):
        return self._email

    @name.setter
    def email(self, email):
        self._email = email



