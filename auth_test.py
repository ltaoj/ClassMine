from csujwc.login import Context
from csujwc.login import CodeLogin

def test_login():
    username = '3903150326'
    password = '123456'
    login = CodeLogin()
    ctx = Context(login)
    ctx.login(username, password)