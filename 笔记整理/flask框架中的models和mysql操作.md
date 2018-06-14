## flask框架中的models和mysql操作

### 模型models

- Flask默认并没有提供任何数据库操作的API ，我们可以选择任何适合自己项目的数据库来使用 
- 在flask中可以使用原生语句实现功能，也可以选择ORM（SQLAlchemy，MongoEngine） 
- 这里我们主要是对mysql进行操作，所以需要pip安装flask-sqlalchemy，pymysql

#### 定义简单的模型

- 和django一样，需要定义模型类，可以创建models.py文件在存放模型类

```python
from flask_sqlalchemy import SQLAlchemy
# 实例化对象
db = SQLAlchemy()

class Student(db.Model):
    s_id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(16), unique=True)
    s_age = db.Column(db.INTEGER, default=18)
	# 表格名称
    __tablename__ = 'student'
```

- 需要使用flask_sqlalchemy模块下的SQLAlchemy实例化db对象
- 通过db.Column创建表格中的列
- 如果不通过__tablename__指定表格名称，在数据库中的表格默认为模型类名

#### 初始化SQLALchemy对象/配置数据库

- 我们初始化db对象，并配置合适的数据库信息才能将数据存入数据库

```python
from flask import Flask
from App.models import db

def create_app():
    app = Flask(__name__)
    # 配置mysql数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/db_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	# 初始化db
    db.init_app(app=app)
    return app
```

- 在初始化db的时候有两种方法

```
第一种：

from flask_sqlalchemy import SQLALchemy

app = Flask(__name__)
db = SQLAlchemy(app)

第二种：

from App.models import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
```

##### 配置数据库

-  数据库连接的格式： 

```
dialect+driver://username:password@host:port/database
-- dialect数据库实现
-- driver数据库的驱动
```

- 举例：访问mysql数据库，驱动为pymysql，用户为root，密码为123456，数据库的地址为本地，端口为3306，数据库名称db_flask

```
'mysql+pymysql://root:123456@localhost:3306/db_flask'
```

- 注意在配置数据库时，我们至少需要配置'SQLALCHEMY_DATABASE_URI'和'SQLALCHEMY_TRACK_MODIFICATIONS'

```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/db_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

#### 创建删除数据表

- 在视图函数中我们引入models.py中定义的db 

```python
from App.models import db

@blue.route("/createdb/")
def create_db():
    db.create_all()
    return "创建成功"

@blue.route('/dropdb/')
def drop_db():
    db.drop_all()
    return '删除成功'
```

- db.create_all()将models中定义的所有表创建到数据库中
- db.drop_all()删除数据库中所有表

### mysql的CRUD操作

#### 查询

##### 普通条件查询

```python
# filter筛选
stus = Student.query.filter(Student.s_name == 'xx')
# filter_by筛选
stus = Student.query.filter_by(s_name='yy')
# all
stus = Student.query.all()
stus = Student.query
# get
stus = Student.query.get(id)
```

- 注意：在django中是类名.objects.xxx；在flask中是类名.query.xxx
- 在使用filter筛选时，条件中要跟上类名，如filter(Student.s_name == 'xx')；在filter_by筛选中，只需要用列名就行
- Student.query.all()和Student.query都可以查询所有，但是查询结果的类型不同，但都可以迭代

```
Student.query --> class 'flask_sqlalchemy.BaseQuery'
Student.query.all() --> class 'list'
```

- 也可以直接通过get(id)获取id对应的值，相比于filter,get如果id不存在会报错

##### 使用运算符查询

- 在flask中，可以像django一样使用运算符进行查询
- 使用运算符查询只能用filter，不能使用filter_by

```
filter(类名.属性名.运算符(‘xxx’))

filter(类名.属性 数学运算符  值)
```

- 常用运算符

```
contains： 包含
startswith：以什么开始
endswith：以什么结束
in_：在范围内
like：模糊   %--匹配一个或多个   _(下划线)--只匹配一个
__gt__: 大于
__ge__：大于等于
__lt__：小于
__le__：小于等于
```

- 用于筛选/排序

```
offset(n)  跳过前n个
limit(n)  只取n个
order_by('id')  id升序排序  order_by('-id')  id降序
get(id)  通过id获取对象
first()  获取第一个
paginate() 分页
```

- 逻辑运算

```
与:and_
	filter(and_(条件,条件…))

或:or_
	filter(or_(条件,条件…))

非:not_
	filter(not_(条件),条件…)
```

##### 查询结果分页

- 在flask中我们也可以对查询结果进行分页
- 直接通过   类名.qurey.paginate(页数，每页条数)就能获取分页对象

```python
@user_blueprint.route('/paginate/', methods=['GET'])
def stu_paginate():
    if request.method == 'GET':
        # 获取要显示的页数
        page = int(request.args.get('page',1))
        # 每页条数
        pagenum = 5
        # 分页对象
        paginate = Student.query.order_by('s_id').paginate(page,pagenum)
        # 将对象转成可迭代
        stus = paginate.items

        return render_template('stu_paginate.html', stus=stus, paginate=paginate)
```

- 如果在前端需要通过for循环来遍历数据，一定要通过.items转成可迭代对象
- 分页对象的属性

```
paginate.items      转成可迭代
paginate.page       当前页数
paginate.prev_num   上一页页数
paginate.next_num   下一页页数
paginate.has_prev   如果有上一页，返回True
paginate.has_next   如果有下一页，返回True
paginate.pages      查询得到的总页数
paginate.per_page   每页显示的记录数量
paginate.total      查询返回的记录总数
paginate.query      分页的源查询
```



#### 添加

```python
@user_blueprint.route('/create_stu/', methods=['GET'])
def create_stu():
    stu = Student()
    stu.s_name = 'yy'
    stu.s_age = '21'

    db.session.add(stu)
    db.session.commit()
    return '添加学生成功'
```

- 创建新的实例化对象，并add添加到db.session中，再commit提交
- 区别于django: 对象.save()

##### 批量增加

- 在flask中还提供了批量增加的操作db.session.add_all(),参数为一个存放多个对象的列表

```python
@user_blueprint.route('/add_course/')
def add_course():
    courses = ['python', 'java', 'c++', 'c#', 'php', ]
    course_list = []
    for c_name in courses:
        course = Course()
        course.c_name = c_name
        course_list.append(course)
    db.session.add_all(course_list)
    db.session.commit()
    return '课程创建成功'
```



#### 更改

- 获取查询对象，直接更改对应属性的值

```python
students = Student.query.filter_by(s_id=3).first()
students.s_name = '哈哈'
db.session.commit()
```

- 通过update更改

```python
Student.query.filter_by(s_id=3).update({'s_name':'娃哈哈'})
db.session.commit()
```

#### 删除

```python
students = Student.query.filter_by(s_id=2).first()
db.session.delete(students)
db.session.commit()
```

#### 注意

在增删改中如果不commit的话，数据库中的数据并不会更新，只会修改本地缓存中的数据，所以一定需要db.session.commit() 