



#### Django 获取前端传递的参数

1-在url后跟上?键值对传递数据：<url>?key=value

  ```python
# 请求的url:<url>?key=value
def func(request):
    no = request.GET['KEY']
  ```

- 这种方法传递的数据，我们可以通过request对象的GET属性来取值，GET属性返回的是字典，我们通过键(key)来取值(value)

2-把值当做路径的一部分，通过urls.py中的映射来取值

url: <url>/example/value

urls.py中的相关代码:

2-1-Django 2.x版本

```python
urlpatterns = [
    path('depts/emps/<int:no>', views.emps, name='empsindept'),]
```

- 在Django 2.x版本中，在路径后跟上占位符 <<int:no>>,表示匹配当前位置的值，并赋值给变量no

2-2-Django 1.x版本

```
urlpatterns = [
    # url('depts/emps/(?P<no>[0-9]+)', views.emps, name='empsindept'),]
```

- 在Django 1.x版本中，在路径中跟上正则表达式（命名分组）将匹配到的值存在命名分组中

这样在views.py中定义相关函数是，就要传递参数了

```python
def func(request, no):
    # 这里的no参数，就是urls中从路径中匹配到的值
    pass
```

3-Ajax发送POST携带数据

如：

```javascript
$.ajax({
        url: '/xxxx',
        type: 'post',
        data: {
               'key': value,
               'csrfmiddlewaretoken': token
        },
        dataType: 'json',
```

- 上述代码通过ajax的post方式提交数据，在data中指定键值对
- 需要注意的是，Django框架中，要发送POST请求，数据中必须携带csrf_token令牌

在views.py中定义相关函数

```python
def func(request):
    value = request.POST['key']
```

- 我们通过request对象的POST属性来取到传递的data，data中的数据是键值对形式的



#### 浏览器向服务器请求JSON时的一些注意事项

1.发送json数据需要对数据进行序列化

- 序列化/串行化/腌咸菜 - 把对象按照某种方式处理成字节或者字符的序列
- 反序列化/反串行化 - 把字符或者字节的序列重新还原成对象
- Python实现序列化和反序列化的工具模块 - json / pickle / shelve

2.直接可以序列化的对象

- 这一类的对象我们可以使用json.dumps()方法直接序列化，然后返回就行了

  ```python
  return HttpResponse(json.dumps(obj), content_type='application/json;charset=utf-8')
  ```

  最好指定一下返回参数为json类型，并指定字符编码为utf-8

3.使用JsonResponse序列化对象

- model.objects.all()和model.objects.filter()等方法，返回的是QuerySet对象
- QuerySet使用看惰性查询 - 如果不是非得取到数据，name不会发出SQL语句这样做是为了节省服务器内存的开销 - 延迟加载 - 节省空间势必浪费时间
- QuerySet对象不能直接用json.dumps()方法序列化
- 使用JsonResponse序列化对象,我们首先要定义对象序列化编码器

```
class ExampleEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__
```

- 代码：

```
return JsonResponse(obj, encoder=ExampleEncoder,safe=False)
```

- 参数说明：
  - obj是要转换成JSON格式(序列化)的对象
  - encoder参数要指定完成自定义对象序列化的编码器(JSONEncoder的子类型)
  - safe参数的值如果为True那么传入的第一个参数只能是字典

4-使用serializers.serialize序列化对象

```python
 from django.core.serializers import serialize
 return HttpResponse(serialize('json', obj), content_type='application/json; charset=utf-8')
```

- serialize('json', obj)，需要先指定序列化的类型

#### 通过Django生成表单(form)

1-需要在views中创建生成表单的类

```python
class CarRecordForm(forms.ModelForm):
    carno = forms.CharField(min_length=7, max_length=7, label='车牌号', error_messages={'carno': '请输入有效的车牌号'})
    reason = forms.CharField(max_length=50, label='违章原因')
    punish = forms.CharField(max_length=50, required=False, label='处罚方式')
    class Meta:
        # 绑定models.py中的相关类
        model = CarRecord
        # 指定要绑定的字段
        fields = ('carno', 'reason', 'punish')
```

2- 创建对象

```python
def add(request):
    if request.method == 'GET':
        # 创建一个新表单对象，可以通过initial指定初始值
        f = CarRecordForm(initial={'reason': '打警察', 'punish': '牢底坐穿'})
    else:
        f = CarRecordForm(request.POST)
        # 通过.is_valid()方法验证表单的有效性
        if f.is_valid():
            # 通过.save()方法将数据保存到数据库中
            f.save()
            return redirect('/search2')
    return render(request, 'add.html', {'f': f})
```

- 这里通过render渲染页面，当f为一个新表单对象时，会在html页面中生成新的表单(form)

3-html中的代码

```
<form action="/add" method="post">
        <table>
        {% csrf_token %}
        {{ f.as_table }}
        </table>
        <input type="submit" value="添加">
</form>
```

- 在表单form标签下添加占位符{{ f.as_table }}，将在此处创建表单
- 注意表单的提交方式是POST，需要在表单中加入防止跨站工具的令牌token

#### cookie和session

1-cookie

- Cookie是保存在浏览器临时文件中的用户数据(通常是识别用户身份的ID/token或者是用户的偏好设置)

- 因为每次请求服务器时在HTTP请求的请求头中都会携带本网站的Cookie数据

- 那么服务器就可以获取这些信息来识别用户身份或者了解用户的偏好 这就是所谓的用户跟踪

- 因为HTTP本身是无状态的 所以需要使用Cookie/隐藏域/URL重写这样的技术来实现用户跟踪

- 从请求中读取指定的cookie - 通过cookie的名字找到对应的值

- 我们可以通过request.COOKIES.get()方法来取到请求中cookies中的值，如果请求中没有指定名字的cookie可以通过get方法的第二个参数设置一个默认的返回值

- 在返回响应时，可以通过set_cookie方法设置cookie

  ```python
  # 先获取render的响应对象
  response = render(request, 'search2.html',{'last': last_visit_time})
  # 通过render渲染页面后先用set_cookie方法设置cookie后再返回HttpResponse对象
  # 第一个参数是cookie的名字 第二个参数是cookie的值 第三个参数是过期时间(秒)
  response.set_cookie('cookie_key', value, max_age=MAX_AGE)
  return response
  ```

2-session

- 通过request对象的session属性可以获取到session
- session相当于是服务器端用来保存用户数据的一个字典
- session利用了Cookie保存sessionid
- 通过sessionid就可以获取与某个用户对应的会话(也就是用户数据)
- 如果在浏览器中清除了Cookie那么也就清除了sessionid,再次访问服务器时服务器会重新分配新的sessionid这也就意味着之前的用户数据无法找回
- 默认情况下Django的session被设定为持久会话而非浏览器续存期会话,通过SESSION_EXPIRE_AT_BROWSER_CLOSE和SESSION_COOKIE_AGE参数可以修改默认设定
-  Django中的session是进行了持久化处理的因此需要设定session的序列化方式,1.6版开始Django默认的session序列化器是JsonSerializer
- 可以通过SESSION_SERIALIZER来设定其他的序列化器(例如PickleSerializer)

```python
# 通过get方法取到session中键所对应的值
cart = request.session.get('cart')
```

