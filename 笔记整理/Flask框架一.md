### Flask框架下最小项目代码结构

- flask适用于web开发的为框架，通过flask框架我们可以快速的搭建起一个小项目
- 一下是官方文档中的最小项目- 文件名hello.py -

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run()
```

- 引入flask中的Flask模块创建一个实例对象(app)，Flask的第一个参数是应用模块或者包的名称，这里使用的是单一模块，所以应该使用__name__
- 我们定义一个处理某个url请求的函数，并通过route()装饰器来装饰该函数，我们在route()中指定url格式
- 通过run()方法来让应用运行在本地服务器上

#### 匹配路由规则

- 我们可以通过设置匹配规则来定制url

#### string

-  默认，匹配字符串

```python
@blue.route('/hello/<name>/')
def hello_person(name):
    return render_template('hello.html',name = name)
```

- URL类型：172.0.0.1/hello/xxx/   ;172.0.0.1/hello/123/   ;172.0.0.1/hello/12.4/   ;都可以匹配到

####int

- 匹配整型

```python
@blue.route('/hello/<int:id>/')
def hello_person(id):
    return render_template('hello.html',id = id)
```

- URL类型：172.0.0.1/hello/123/ ,只能匹配整型

#### float

- 匹配浮点型

#### path

-  匹配路径

```python
@blue.route('/hellopath/<path:path>/')
def hello_path(path):
    return render_template('hello.html', path=path)
```

- URL类型：172.0.0.1/hello/123/xxx/sss/ ,匹配hello之后的路径

### 模块的拆分

- 在flask框架下，它允许仅用一个py文件来存放整个项目的代码内容，但是这并不是一个好的方式，如果代码量巨大，那么在debug和后期维护上就会带来很多麻烦
- 我们需要将我们的项目代码拆分成不同的模块，各司其职，这样不仅项目结构清晰，也方便维护管理
- flask框架也是cvp模式，我们可以参照django的模块形式，将代码拆分到不同的py文件中
- 代码的拆分因人而异，flask没有明确的规范要求，这里我将代码拆分成utils(工具)、app(应用)、manage.py(项目管理文件)

#### utils中的functions

- utils目录中存放的是我们自定义的一些工具，这里我们新建一个function.py文件用于存放拆分的代码——Flask实例化部分的内容

```python
import os
from flask import Flask

# 引入应用中的蓝图，在Flask实例化后注册
from user.user_views import user_blueprint


def create_app():
    # 获取项目根目录地址，并指定静态文件和模板文件目录
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    # 注册蓝图
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

    return app

```

- 我们将代码按功能拆分之后，各部分并不能自动建立关联，所以我们需要使用到蓝图
- 获取项目根目录地址，并指定静态文件和模板文件目录，在Flask实例化对象时需要指定静态文件和模板文件目录
- 注意，Flask实例化对象时，参数中默认指定了静态文件(static_folder='static')和模板文件目录(template_folder='templates')，但是这两个目录都是对应的当前文件同一级目录下的static和templates

#### 应用(app)中的views

- 参照django，我们在应用目录中创建views.py文件，用于存放该应用处理url请求的方法

```python
from flask import Blueprint
user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/')
def hello():
    return 'hello'

```

- 首先通过Blueprint实例化一个蓝图对象，蓝图对象要在Flask实例化后注册
- 定义处理某个url的方法，并用route()装饰

#### 项目管理(manag.py)中

- 在manage中我们只需要简单的配置项目，指定管理的对象就好了

```python
#导入Manager对象
from flask_script import Manager
#导入utils中自定义的实例化app的方法
from ufils.functions import create_app

#获取Flask实例化的对象
app = create_app()
# 实例化manage对象
manage = Manager(app=app)


if __name__ == '__main__':
    manage.run()

```

- 这里我们需要获取到utils目录下function中实例化的Flask对象
- 通过manager对象来管理我们的项目，这样我们就可以像django在启用项目时那样指定端口等信息了

```
# -p 指定以8083端口运行项目    -d debug=True
python manage.py runserver -p 8083 -d
```



#### 蓝图

- 在Flask项目中可以用Blueprint(蓝图)实现模块化的应用，使用蓝图可以让应用层次更清晰，开发者更容易去维护和开发项目。蓝图将作用于相同的URL前缀的请求地址，将具有相同前缀的请求都放在一个模块中，这样查找问题，一看路由就很快的可以找到对应的视图，并解决问题了。 
- 要使用蓝图，我们需要pip安装flask_blueprint包

```python
from flask import Blueprint
#实例化蓝图对象
user_blueprint = Blueprint('user', __name__)
#注册蓝图，并指定url前缀
app = Flask(__name__)
app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
```

- 在实例化蓝图时，第一个参数是蓝图的名称，第二个参数表示蓝图所在包或模块名
- 我们通过Flask实例化的对象中的register_blueprint注册蓝图，第一个参数是蓝图对象，第二个参数是蓝图的url前缀，所有url请求必须以/user开始，才能访问到该蓝图装饰的方法

### 渲染模板/响应/重定向/反向解析

#### 渲染模板

- 在处理完某个url的请求后，需要返回某个页面(渲染该页面)

```python
from flask import Blueprint, render_template
user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/login/')
def login():
    return render_template('login.html')
```

- 需要引入flask中的render_template来渲染模板页面

#### 响应

- 在处理完某个url的请求后，需要给页面响应

```python
from flask import Blueprint, make_response
user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/user_resp/')
def get_user_response():
    response = make_response('<h3>墨雨小轩</h3>', 200)
    return response
```

- 需要引入flask中的make_response来创建响应，第一个参数是响应的内容，第二个参数是状态码
- 我们还可以通过response.set_cookie()来设置cookie

#### 重定向和反向解析

- 在处理完某个url的请求后，需要重定向到新的url

```python
from flask import Blueprint,redirect, url_for
user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/redirect/')
def user_redirect():
    # 直接重定向到某个url
    return redirect('/user/login/')
	# 重定向到反向解析的url
    return redirect(url_for('user.login'))
```

- 需要引入flask中的redirect来实现重定向
- 需要引入flask中的url_for来实现url反向解析，参数为:蓝图名.方法名

### 获取请求(request)中的数据

- 在url请求时，会传递某些参数，我们可以在request中获取

```python
@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        return username
```

- 在route中指定methods方式
- request.form--获取POST方式提交的数据；request.args--获取GET方式提交的数据;request.files--获取上传的文件
- 注意：request.form是一个类字典类型(不是字典)，不同于字典，可以通过同一个键获取对应的多个值

```
form = {ImmutableMultiDict}ImmutableMultiDict([('username', 'XXX'), ('username', 'aaaa')])
```

- 通过request.form.getlist('username'),可以得到一个列表['xxx','aaaa'],如果只通过get方法来取值的，只会获取第一个对应的值