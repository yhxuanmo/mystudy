### 终端环境下创建Django

- 首先要检查python版本，确定Django安装的版本

1、创建文件夹，用于存放虚拟目录，项目，应用目录(app)

```
mkdir hello_django
```

2、进入hello_django目录，创建虚拟环境

- Windows

  ```
  python -m venv venv
  ```

  注：第二个venv 是虚拟目录名称

- linux

  ```
  python3 -m venv venv
  ```

3、激活虚拟环境

- windows

  - 进入虚拟环境目录下的Scripts，执行activate

  ```
  cd venv/Scripts
  activate
  激活了虚拟环境
  ```

- linux

  - 直接用source 命令执行activate

  ```
  source venv/bin/activate
  激活了虚拟环境
  ```

4、在虚拟环境中安装django

```
pip install django[==1.11]
```

- 这里可以通过  ==1.11  来指定django版本

5、返回上上一级目录(hello_django，这里是和venv同一级目录)，创建项目

```
django-admin startproject hello_dj .
```

- 这里创建了hello_dj 项目  
- 语句后加一个 .  表示在当前目录下创建项目

6、创建应用(app)

```
python manage.py startapp hrs
```

- 这里创建了hrs应用







通过python manage.py runserver命令启动服务器

在阿里云上，python manage.py runserver 0.0.0.0:80，可以指定启动ip和端口

用过deactivate 退出虚拟环境

在pycharm的Terminal终端用：python manage.py shell  可以进入python交互环境，这里的交互环境包含了当前项目下的所有设置

### 项目文件夹

#### __init__.py

- 在这个py文件中，需要在里面添加代码，让我们的app能找到数据库

  ```python
  import pymysql

  pymysql.install_as_MySQLdb()
  ```

#### setting.py

- 这是项目的配置文件

- 文件中的内容：

  - DBUG=True 表示当前项目处于调试状态，如果项目正式上线，那么要改为False

  - ALLOWED_HOSTS=[] 这是表示在应用服务器启动时，允许访问的ip地址

  - INSTALLED_APPS 将我们的应用(app)定义到里面

    ```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'hrs',
    ]
    ```

    'hrs'是我们的一个应用，将它添加进去

  - TEMPLATES 指定我们的应用所要用到的模板(templates目录)地址

    ```python
    # 更改内容
    'DIRS': [os.path.join(BASE_DIR, 'templates')
    ```

  - DATABASE 这里是连接数据库的信息

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'oa',
            'HOST': 'localhost',
            'POST': 3306,
            'USER': 'root',
            'PASSWORD': '123456'
        }
    }
    ```

  - 语言编码

    ```python
    # 改成中文
    LANGUAGE_CODE = 'zh-hans'
    ```

  - 时区

    ```python
    # 对应的时区
    TIME_ZONE = 'Asia/Chongqing'
    ```

  - 添加静态资源目录地址

    ```python
    # 这行代码原文中没有，需要自行添加
    STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
    ```

  - 静态资源url

    ```python
    STATIC_URL = '/static/'
    ```

  - 指定Django序列化器(可以不用指定)

    ```python
    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
    ```

    指定序列化器为PickleSerializer

#### urls.py

- 这个文件主要是映射我们不同的url，对应我们的应用(app)视图(views.py)中的方法的

  ```python
  urlpatterns = [
    # URL = 'localhost:80'  映射的是index方法
      path('', views.index),
    # 这是默认映射，连接的是管理员页面(后台)
      path('admin/', admin.site.urls),
    # 下面的是映射应用中的其他方法
      path('hrs/depts', views.depts),
      path('hrs/emps',views.emps),
      path('hrs/deldept',views.del_dept)
  ]
  ```

### 应用文件夹

#### admin.py

- 这个文件夹主要是配置管理员页面的显示内容的

- 这里上代码，解释见注释

  ```python
  from django.contrib import admin
  
  # Register your models here.
  # 将应用中模型(models.py)的相关类引入
  from hrs.models import Dept, Emp
  
  # 在管理员后台 以表格形式显示内容
  # 这里的类要继承admin.ModelAdmin
  class DeptAdmin(admin.ModelAdmin):
      # 在后台表格显示哪些内容
      list_display = ('no', 'name', 'location', 'excellent')
      # 指定排序方式
      ordering = ('no',)
  
  class EmpAdmin(admin.ModelAdmin):
      list_display = ('no', 'name', 'job', 'mgr', 'sal', 'comm', 'dept')
      ordering = ('no',)
      # 在后台添加搜索框，这定可以搜索的列
      search_fields = ('name', 'job')
  # 注册后台显示的表格
  # 如果没有注册，数据库的表格将不会在后台显示
  admin.site.register(Dept,DeptAdmin)
  admin.site.register(Emp,EmpAdmin)
  ```

- 要使用管理员，首先我们需要在虚拟环境的终端下，通过python manage.py createsuperuser 命令创建一个管理员


#### models.py

- 这个文件主要是配置模型的

- 这里可以定义类，来实现在数据库中创建表格

- 类中的每一个属性，对应表格中的每一列

- 代码

- ```python
  # 定义一个类Emp,继承models.Model
  # 这样可以在数据库中创建一个emp表格
  class Emp(models.Model):
      no = models.IntegerField(primary_key=True)
      name = models.CharField(max_length=20)
      job = models.CharField(max_length=10)
      mgr = models.IntegerField(null=True, blank=True,verbose_name='主管')
      sal = models.DecimalField(max_digits=7, decimal_places=2)
      comm = models.DecimalField(max_digits=7, decimal_places=2,null=True, blank=True)
      dept = models.ForeignKey(Dept, on_delete=models.PROTECT)
      # 重命名表格名称
      class Meta:
          db_table = 'tb_emp'
  ```

  ​



  - 注意：如果某一列不能为空，我们要指定null=True；同时还要指定blank=True，这表示在管理员后台录入数据时可以为空

- 通过生成迁移和执行迁移两步操作，才能在数据库中创建表格

  - 生成迁移

    ```python
    python manage.py makemigrations hrs
    ```

    注：这里生成的迁移文件存放在应用下migrations目录下

  - 执行迁移

    ```python
    python manage.py migrate
    ```

  - 如果我们对models.py中定义的类(表格)做出修改时，都要执行生成迁移和执行迁移操作，这样才能更新数据库中对应的表

- ORM

  ```
  对象模型  <--->  关系模型
  实体类    <--->  二维表
  属性      <--->  列
  实体对象  <--->  一条记录
  ```



#### views.py

- 这个文件是视图的配置

- 在这里，我们通过定义函数来实现对页面请求的响应

- 项目文件下urls.py中映射的方法，就是这里定义的函数

- 代码

  ```python
  from django.shortcuts import render
  # Create your views here.
  # 将模型(models.py)中定义的类引入
  from hrs.models import Dept,Emp

  # 这是处理index页面的
  def index(request):
      return render(request, 'index.html', context={})

  # 这是处理表格页面的
  # django处理页面请求时默认会传入request参数
  def emps(request):
      # url = 'xxxxx/emps?dno=10'
  	# 这里通过request对象的GET属性可以取到url问号(?)后面的值，这里得到的是一个字典(Dict)
      dno = int(request.GET['dno'])
      ctx = {'emp_list': Emp.objects.filter(dept_id=dno)}
      # 通过render方法渲染对应的页面
      # context 对应的是HTML文件中的占位符
      return render(request, 'emps.html', context=ctx)
  ```


### templates(模板)目录

- 这是用来存放HTML文件的

- HTML中的占位符

- 加载静态文件目录，并使用

  ```
  {% load static %}
  <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
  ```

- 使用for循环

  ```
  {% for dept in dept_list %}
  标签
  {% endfor %}
  ```

- 使用条件语句--这里的条件只能是布尔值

  ```
  {% if dept.excellent %}
  标签1
  {% else %}
  标签2
  {% endif %}
  ```

- 占位符 - 与render函数中传递的字典的键对应

  ```
  {{text}}
  ```

  

- POST表单(form)令牌

  ```
  {% csrf_token %}
  ```



- Django  生成的表单

  ```
  {{ f.as_table }}
  ```

  

