### JSONRenderer定制返回msg格式

- 在前后端分离的模式下，前端通过Ajax向后端发起请求，后端处理完毕后，会返回一些数据给前端，前端只需要在msg中提取需要的信息即可
- 返回的msg格式并非固定的，我们不同的设置或者自定义格式之后，可以设置出我们想要的msg

#### 默认返回格式

- rest framework 框架中默认的msg返回格式，没有分页设置，没有定制

```
[
    {
        "s_name": "aaa",
        "s_chinese": 81,
        "id": 2,
        "g_name": "C++"
    },]
```

- 可以看出，默认的返回格式是一个列表，里面以字典的形式存放单个对象
- 注：返回的数据其实是json -->Content-Type: application/json

#### 配置了分页的返回格式

- 在数据量很庞大的时候，我们需要对数据进行处理，使其分页（输出一部分）
- 我们经过分页设置之后，msg的格式将发生变化

```
  {
    "count": 9,
    "next": "http://127.0.0.1/app/api/student/?page=2",
    "previous": null,
    "results": [
        {
            "s_name": "aaa",
            "s_chinese": 81,
            "id": 2,
            "g_name": "C++"
        },
     ]
  }
```

- 可以看出，我们使用了分页之后，返回的是一个字典，相关的结果存放在

"results"中

- count：查询结果的总个数
- next：下一页的url
- previous：上一页的url
- 注：返回的数据其实是json -->Content-Type: application/json

#### JSONRenderer定制msg返回格式

- 这里定制的格式，根据需求的不同，格式也不同，这里只举一例，简单说明一下

##### 编写自定义格式类

- 我们需要自定义一个类来描述我们要自定义的msg格式
- 创建一个py文件，保存在工具(utils)目录下(也可以保存在其他地方)
- 在文件中创建自定义类，需要继承自JSONRenderer(从rest_framework.renderers模块中引入)，重写render方法

```python
class CustomJSONRenderer(JSONRenderer):
    """
    返回结果构造
    {
        'data': results,
        'code': 200,
        'msg':'请求成功'
    }
    """
    # 重写方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data, dict):
                code = data.pop('code', 0)
                msg = data.pop('msg', '请求成功111')
            else:
                code = 0
                msg = '请求成功'
            # 定制返回格式
            res = {
                'code': code,
                'msg': msg,
                'data': data,
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
```

- 上面的代码，我们定制了返回结果由‘data’,'msg','code'三部分组成，其中data存放的是后端默认返回的数据

##### 在项目setting中配置

- 编写好自定义返回格式后，我们需要在setting中配置
- 在setting的REST_FRAMEWORK中配置我们的自定义格式文件

```python
REST_FRAMEWORK = {'DEFAULT_RENDERER_CLASSES': (
        'utils.functions.CustomJsonRenderer',
    ),}
```

- 注意这里'DEFAULT_RENDERER_CLASSES'的值为一个**元祖**

##### 自定义返回格式

- 通过上面的步骤，我们自定义的msg就设置好了

```
{
    "code": 0, 
    "msg": "请求成功111", 
    "data": {
        "count": 9, 
        "next": "http://127.0.0.1/app/api/student/?page=2", 
        "previous": null, 
        "results": [
            {
                "s_name": "aaa", 
                "s_chinese": 81, 
                "id": 2, 
                "g_name": "C++"
            }
        ]
    }
}
```

- 由于是在分页的基础上完成的定制msg,所以data中包含了分页的信息

### 过滤器

- 在日常项目中，我们需要对查询信息进行过滤，筛选出我们期待的结果
- 在rest framework框架中我们可以通过过滤器来实现

#### 在接口中直接过滤

- 如果我们处理请求的某个类(接口)只处理一种条件的查询，那么我们可以直接在这个类中重写get_queryset()方法来实现筛选

```python
class api_student(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Student.objects.all().filter(s_delete=0)
    serializer_class = StudentSerializer
    # 重写方法
    def get_queryset(self):
        query = self.queryset
        # 通过request.query_params.get方法获取url中的参数
        s_name = self.request.query_params.get('s_name')
        return query.filter(s_name__contains=s_name)
```

- 这里我们重写了get_queryset()方法，实现了对名称的模糊查询
- 注意：我们url的格式应该为http://127.0.0.1/app/api/student?s_name=value格式
- 通过request.query_params.get可以获取url中？后面的参数
- 但是这种方法在实际案例中并不推荐使用，因为这样重写方法后，我们一个类就只能处理特定条件的筛选了

#### 定制过滤器

##### 创建过滤器类

- 在日常项目中，我们一个接口可能要处理多种条件的查询，我们就不能再接口类中直接重写get_queryset方法来实现条件过滤了，这时候就需要我们来写一个过滤器文件
- 在当前app中创建过滤器py文件，在文件中定义过滤器类，该类继承自rest_framework中的filters.FilterSet
- 在写过滤器文件之前需要pip安装django_filters(1.1.0),同时djangorestframework(3.4.6)

```python
import django_filters
from rest_framework import filters
from app.models import Student
class StudentFilter(filters.FilterSet):
	# 指定允许的查询条件
    s_name = django_filters.CharFilter('s_name', lookup_expr='contains')
    s_yuwen_min = django_filters.NumberFilter('s_yuwen', lookup_expr='gte')
    s_yuwen_max = django_filters.NumberFilter('s_yuwen', lookup_expr='lte')
	# 绑定查询模型
    class Meta:
        model = Student
        fields = ['s_name', ]
```

- 注意：Meta下的fields中存放的是精确查找的字段，如果没有在fields中指定的字段或者没有指定条件查询，那么将无法查询出期待的结果

##### 在项目setting中配置过滤器

- 过滤器创建好之后，我们需要在项目setting的REST_FRAMEWORK中配置过滤器

```python
REST_FRAMEWORK = {'DEFAULT_FILTER_BACKENDS':(
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter'
    ),}
```



##### 在views中对应的接口指定过滤器

- 配置好过滤器后，我们需要在views中对应的接口指定过滤器

```python
class api_student(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Student.objects.all().filter(s_delete=0)
    serializer_class = StudentSerializer
	# 指定过滤器
    filter_class = StudentFilter
```

