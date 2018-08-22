## Django-rest前后端分离

在日常的开发工作中，有时候我们会把前后端的工作分离开来，前端负责html页面渲染、数据渲染，而后端只接受请求和返回响应，前后端通过接口(api)来联系，这样做分工明确。



### HTTP请求方式

- GET:用于获取数据
- POST:用于创建数据
- PUT:用于修改数据(修改全部属性)
- PATCH:用于修改数据(修改部分属性)
- DELETE:用于删除数据
- 对于同一个url，不同的请求方式，结果不一样
- 如url:http://127.0.0.1:8081/app/api/student/
  - GET请求：获取所有的学生信息
  - POST请求：创建的学生
- 如url:http://127.0.0.1:8081/app/api/student/2/
  - GET请求：获取学生中id为2的那一个学生
  - PUT/PATCH请求：修改学生中id为2的学生信息
  - DELETE请求：删除学生中id为2的学生

### 使用rest framework 框架

- 我们需要通过pip安装djangorestframework包

#### 项目setting中的配置

- 需要将rest_framework添加到INSTALLED_APPS列表中

```python
INSTALLED_APPS = ['rest_framework',]
```

- 添加REST_FRAMEWORK字典，这个字典中填写与rest相关的配置

```python
REST_FRAMEWORK = {
    # 默认的分页方式--如果不使用分页可以忽略
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 每页数据量
    'PAGE_SIZE':2,
    # rest默认权限验证
    'DEFAULT_AUTHENTICATION_CLASSES':()
}
```

- 注意： -- 如果使用了中间件且在中间件方法中重写了request中的user,这里需要把默认权限验证设置为空，否则会提示is_active不存在。我们还可以在我们自定义的用户表中将is_active列加上并赋值(0/1),这样也可以解决这个问题，但是不推荐这么做。

####应用urls中的配置

- 我们需要从rest_framework.routers引入SimpleRouter模块，并创建router对象，注册url

```python
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'^api/student',views.api_student)
router.register(r'^api/grade',views.api_grade)

urlpatterns += router.urls
```

- 我们还需要把注册的url添加到urlpatterns中

#### 定义序列化类

- 我们需要新建py文件来编写序列化类
- 在这个类中需要指明对应的model、需要序列化的列（fields）

```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定对应的模型
        model = Student
        # 指定需要序列化的列
        fields = ['s_name', 's_chinese','id']
    def to_representation(self, instance):
        # 序列化当前表的数据
        data = super().to_representation(instance)
        # 如果要添加与该对象关联的表中的内容，需要自行添加
        data['g_name'] = instance.g.g_name
        return data
```

- to_representation中instance是当前循环的学生的对象

#### views中定义对应的类

- 在views中我们需要定义实现相关功能的类

```python
class api_student(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    # 查询学生的多有信息
    queryset = Student.objects.all().filter(s_delete=0)
    # 序列化类型
    serializer_class = StudentSerializer
	# 重写了删除方法
    def perform_destroy(self, instance):
        instance.s_delete = 1
        instance.save()
```

- queryset查询的结果，该变量名不可改变
- serializer_class序列化类型，该变量名不可改变；StudentSerializer是我们定义的序列化类
- 在项目中，有时候我们删除数据时只希望软删除(数据还存在表中，只是状态是删除，可以用bool值来控制)，这是默认的删除方法就不能用了，我们需要重写这个默认的删除方法perform_destroy



####前后端通过api通信——ajax

- 在后端程序中实现了对应功能的api接口，我们在前端可以用ajax发请求实现前后端的通信，从请求成功的msg中提取我们需要的数据

### ajax请求方式

#### GET请求

```
$.get(url, function(msg){
	
})
```

- url表示请求的地址，function(msg)代表，请求成功后的回调函数，msg是api返回的结果

#### POST请求

```
$.post(url, function(msg){
		
})
```

- url表示请求的地址，function(msg)代表，请求成功后的回调函数，msg是api返回的结果

#### ajax通用请求

```
$.ajax({
	url:'', # 请求的url地址，
	type:'', # GET POST PATCH PUT DELETE
	data：{'name':name,'sex':sex}，  # 代表请求的参数
	dataType:'json',
	headers:{'X-CSRFToken': csrf}  # 代表传递的csrf值
	success:function(msg){
		成功执行回调函数
	},
	error:function(msg){
		失败执行回调函数
	}

});
```



