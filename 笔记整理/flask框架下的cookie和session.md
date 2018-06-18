### cookie

#### 创建cookie

- Cookie是通过服务器创建的Response来创建的

```python
from flask import Blueprint, make_response
user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/setcookie/')
def set_cookie():
    temp = render_template('cookies.html')
    # 创建响应时可以绑定页面
    response = make_response(temp)
    # set_cookie(key, value, max_age, expires)
    response.set_cookie('ticket', '123123', max_age=10)

    return response
```

- 通过response.set_cookie()来设置cookie中的键值，可以指定存活(有效)时间
- 注意通过make_response创建响应时，可以绑定页面

```python
temp = redirect('/user/success/')
response = make_response(temp)

temp = render_template('cookies.html')
response = make_response(temp)
```

#### 删除cookie

- 直接在浏览器端清空cookie
- 重新设置cookie中对应键的值为空，过期时间0

- 通过delete_cookie()删除对应的键

```python
@blue.route('/delcookie/')
def del_cookie():
    temp = render_template('index.html')
    response = make_response(temp)
	# 第一种方式，通过set_cookie去删除
    response.set_cookie('name','',expires=0)
	# 第二种方式，del_cookie删除
	response.del_cookie('name')
    return response
```

#### 获取cookie中的值

- 通过request中的cookies可以获取cookie中存的值

```python
request.cookies.get('username')
```

### session

- session是存在于服务端的数据，我们可以通过flask框架下的session组建来保存session到多个地方，如：redis,mongodb,sqlalchmey等
- 我们需要通过pip安装flask-session模块
- 这里我们将session存在redis中，所以还需要pip安装redis模块

#### 设置session

```python
session['key'] = value
```

#### 读取session中的值

- 通过键找值

```python
result = session['key'] ：如果内容不存在，将会报异常

result = session.get('key') ：如果内容不存在，将返回None
```

- 这里推荐使用get()方法来获取数据

#### 删除session中的数据

- 通过pop()方法,可以删除对应的键

```python
session.pop('key')
```

- 通过clear()方法，可以清空session中的所有数据

```python
session.clear()
```

#### 将session保存到redis中

- 在Flask实例化的app对象中配置session相关参数，并初始化session

```python
from flask import Flask
from flask_session import Session
import redis
def create_app():
    app = Flask(__name__,)
    # 秘钥
    app.config['SECRET_KEY'] = 'secret_key'
    # 指定session类型
    app.config['SESSION_TYPE'] = 'redis'
    # redis服务器 ip和端口，默认127.0.0.1:6379
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
    # 初始化session第一种方法
    # sess = Session()
    # sess.init_app(app=app)
    #初始化session第二种方法
    Session(app=app)
    return app
```

- 需要配置SECRET_KEY密钥，必须
- 指定session的类型，这里是redis
- 配置redis服务器的端口，ip ，默认为127.0.0.1:6379
- 需要将session初始化，如果没有初始化，rides可能不会存入session数据

