### 文件上传和获取

#### HTML页面的文件上传

- 在html页面中我们要有一个上传的文件选择框，同时表单(form)也要有enctype属性

```
<form action="" method="post" enctype="multipart/form-data">
	{% csrf_token %}
	<input name="s_img" type="file">
	<input name="" type="submit" value="提交">
</form>
```

- 注意Django框架下提交post请求，一定要有令牌(csrf_token)

#### 从请求(request)中获取文件

- 在python的Django框架下，我们可以通过request.FILES.get()来获取传递过来的文件

```python
def func(request):
    if request.method == 'POST':
        s_img = request.FILES.get('s_img')
        pass
```

- 我们可以向储存其他变量的方式将**文件的地址**存入数据库的表中

#### 在应用下的models.py中

- 在models的代码中，我们要指定文件存储的相关参数

```python
class Table(models.Model):
    s_img = models.ImageField(upload_to='upload')
```

- 这里我们存的是图片，所以指定的是ImageField
- 指定图片加载到upload路径下，这个目录是存放文件的
- 如果我们设置了静态文件存放目录(static)，那么upload目录将会被创建在static目录下
- 但是我们一般会将用户上传的文件单独放置，所以我们需要在与应用同级目录下创建一个media目录，用于存放用户上传的文件

![1527596043035](C:\Users\ADMINI~1\AppData\Local\Temp\1527596043035.png)

- 需要注意的是，django并不知道我们设置了新的目录用于存放用户上传的文件，这时候我们就需要在项目的setting中设置路径

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
```

- 完成了上述操作，上传文件并储存的功能才算实现了

#### 读取上传的文件

- 用户上传文件储存后，我们要实现文件读取，需要在项目的urls文件中配置文件路径
- 我们需要使用django.contrib.staticfiles.urls下的static模块
- 将项目setting中配置的MEDIA_URL和MEDIA_ROOT添加到urls中

```python
from django.contrib.staticfiles.urls import static
from XXX.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
```



### 注册登录

#### 在HTML文件

- 中我们通过提交表单(form)的方式(post)，向服务器发送注册和登录的信息

```
<form action="" method="post" enctype="multipart/form-data">
	{% csrf_token %}
	<input name="username" type="text">
	<input name="pwd" type="password">
	<input name="" type="submit" value="提交">
</form>
```

#### Django原生注册和登录

- Django为我们提供了原生的注册和登录验证方法，我们可以快速的实现注册登录功能

#####原生注册

- 我们要用到django.contrib.auth.models模块下的User,它是Django中自带的用户信息储存模型，对应数据库中的auth_user表(Django自动创建的)

```python
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        # 验证信息完整性和正确性
        
        User.objects.create_user(username=username, password=pwd)
        # User.objects.create_superuser(username=username, password=pwd)
```

- 通过request.POST.get()方法获取到用户提交的信息，验证验证信息完整性和正确性后，我们将信息存入数据库中的auth_user表中
- 我们可以通过User.objects.create，User.objects.create_user，User.objects.create_superuser 三种方法在auth_user表中创建数据
- 需要注意的是User.objects.create，创建的数据，密码部分是没有加密处理的，而User.objects.create_user，User.objects.create_superuser 两种方法创建的数据都是经过加密处理的
- User.objects.create_user创建的是普通用户
- User.objects.create_superuser 创建的是超级用户——管理员

##### 原生登录验证

- 我们要用到django.contrib模块下的auth

```python
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        # 验证用户是否存在
        user = auth.authenticate(username=username,password=pwd)
        if user:
            auth.login(request,user)
```

- 通过request.POST.get()方法获取到用户提交的信息
- 通过auth.authenticate方法验证用户是否存在，如果存在返回用户对象，如果不存在返回空
- 如果用户对象存在，我们就可以通过auth.login(request,user)方法进行登录
- 只用通过了auth.login方法让用户登录了，用户下次的请求(request)中的user才会存有当前用户的信息

##### 原生退出

- 我们通过Django原生登录后需要用到auth.logout(request)方法来退出，这个方法会清除请求(request)中的user的信息

##### 原生验证是否登录

- 使用了Django原生的登录验证，我们在请求登陆后才能访问的页面是，就需要对是否登录进行验证
- 我们使用django.contrib.auth.decorators模块中login_required方法处理urls中的方法

```python
urlpatterns = [
#Django 验证是否登录login_required
url(r'^index/', login_required(views.index), name='index'),
]
```

- 如果验证通过，将调用views中对应的方法
- 如果验证没通过，我们需要告诉Django要跳转到的页面，就需要在项目的setting中指定跳转地址

```python
# 没有登录跳转地址
LOGIN_URL = '/user/login/'
```





#### 自定义的注册登录

- 有时候我们因项目需要，需要自己写用户的注册登录这里我们要自己生成验证是否登录的ticket，在我们自己定义的user表和cookie中都存入同一个ticket，用来验证用户是否登录

##### 自定义的注册

- 自定义注册和用Django自带的注册大同小异，唯一不同的是，我们需要自己创建一个user表用于存放用户的注册信息，表中有一列为ticket存放用户是否登录
- 需要注意的是ticket不要用bool类型，用字符串，用bool类型很容易被骗过登录认证

##### 自定义登录

- 这里我们要自己生成验证是否登录的ticket，在我们自己定义的user表和cookie中都存入同一个ticket，用来验证用户是否登录

```python
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user=Users.objects.filter(username=username,password=pwd).first()
        if user:
            # 用随机方法生成ticket的值
            ticket = 'xxxxx'
            # 将ticket存入对应用户表中
            user.ticket = ticket
            user.save()
            response = HttpResponseRedirect(reverse('app:index'))
            # 保存到用户端的cookie中
            response.set_cookie('ticket',ticket)
            return response

```

- 这里需要注意的是，ticket最好用随机的方式生成
- 将ticket存入服务端的表和用户端的cookie中
- 在请求登录后的页面的时候，我们要讲请求(request)和服务器中的ticket进行验证

##### 自定义退出

- 由于我们自定义登录的时候，在cookie中存入了ticket，在退出登录时我们就要将cookie中的ticket删除掉

```python
def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect(reverse('user:login'))
        response.delete_cookie('ticket')
        return response
```

##### 验证是否登录

##### 装饰器方法

- 我们可以通过装饰器，装饰views中每个处理页面请求的方法
- 在装饰器中实现验证方法

```python
def CheckTicket(func):
    def inner(request):
        ticket = request.COOKIES.get('ticket')
        user = Users.objects.filter(ticket=ticket)
        if user:
            return func(request)
        else:
            return HttpResponseRedirect(reverse('user:login'))
    return inner
        
```

- 这里我们定义了验证登录的装饰器，验证原理也是验证ticket
- 我们用装饰器装饰views中每个处理页面请求的方法

```python
@CheckTicket
def index(request):
    psss
```



##### 通过中间件验证是否登录

- 我们还可以通过中间件来对请求进行过滤，不满足要求的请求(request)过滤掉，也就是不再往后台传递
- 我们需要使用到process_request请求拦截，在定义的中间件类中，方法名必须为process_request
- 我们需要在与应用同一级的目录中创建一个utils目录用于存放我们自定义的中间件

![1527601196008](C:\Users\ADMINI~1\AppData\Local\Temp\1527601196008.png)

- 定义中间件类，在utils目录中创建py文件，要记得加上__init__.py文件。为了作为包导入

```python
class UserAuthMiddle(MiddlewareMixin):
    def process_request(self,request):
        # 获取当前请求的url
        path = request.path
        # 设置过滤的url
        s = ['/user/login/','/user/register/']
        if path in s :
            return None
        
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))
        user = Users.objects.filter(ticket=ticket)
        if not user:
            return HttpResponseRedirect(reverse('user:login'))
        # 如果验证通过，将user存在request的user中
        request.user = user
```

- 我们还需要在项目的setting文件中配置我们自定义的中间件类

```python
MIDDLEWARE = ['utils.UserAuthMiddleware.UserAuthMiddle',]
```



### 小结

- 如果想要快速的搭建注册登录，选择Django自带的方法。一般情况都会自己写注册登录，我们在给cookie设置ticket的时候，可以指定ticket的存活时间
- 验证是否登录，我们首选中间件类的方法，中间件的使用相当于一夫当关万夫莫开，直接对所有的请求进行过滤；而如果使用装饰器的话，需要给views中每个需要的函数都添加一次，稍显麻烦