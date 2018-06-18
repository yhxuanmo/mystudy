### 模板继承

- 在HTML页面中，页面不同，但是其中的某些内容(代码)是相同的，如：CSS,JS等。我们可以将这些相同的部分提炼出来，作为一个基础模板，其他的HTML页面都继承自这个模板，这样我们就不用写重复的代码了。
- 优点：修改一处，就能实现多出更改，可避免遗漏了某些文件的更改
- 基础模板base.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>
        {% block title %}
        {% endblock %}
    </title>
    {% block extCSS %}
    {% endblock %}
    {% block extJS %}
    {% endblock %}
</head>
{% block indexbody %}
{% endblock %}
<body>
{% block content %}
{% endblock %}

{% block footer %}
{% endblock %}

</body>
</html>
```

- 在模板中，我们用{% block xxx %}和{% endblock %}来占位
- 还可以在模板中将共有的部分添加到占位符内

```
{% block extJS %}
    <script type="text/javascript" src="/static/js/jquery.min.js"></script>
{% endblock %}
```

- 我们在其他html文件中，如果要继承该模板，需要将模板引入

```
{% extends 'base_amin.html' %}
{% block title %}
    首页左侧导航
{% endblock %}
{% block extJS %}
	{{ block.super }}
	<script type="text/javascript" src="/static/js/public.js"></script>
{% endblock %}
```

- 在文件中，将该文件自己的内容填入占位符中
- 需要注意的是，如果模板占位符中已有代码，同时我们又要在该占位符中添加自己的内容，需要用到{{ block.super }}将模板中的内容给导入。如果直接往占位符中写内容会覆盖模板中原有的内容

```
# 模板 #
{% block extJS %}
    <script type="text/javascript" src="/static/js/jquery.min.js"></script>
{% endblock %}
# 模板 #
```

- 以上是一个有内容的模板，如果我们文件对应部分与模板内容一样的

  ```
  # 1 我们在文件中可以不用写该部分的占位符，即直接继承模板该部分的内容
  [此处继承模板，不用写内容]
  
  
  # 2 可以写占位符，但是必须加上super
  
  {% block extJS %}
  	{{ block.super }}
  {% endblock %}
  ```

- 注意：如果我们写了占位符，但是没有用super，那么模板中对应位置的代码将会被【空】覆盖，即该处没有任何代码

### 权限

- 在日常设计中，我们针对不同的用户要设置不同的权限
- 我们常用的做法是：用户<-->角色《----》权限
- 用户和角色：一对一或者一对多关系
- 角色和权限：多对多 （有中间表）
- 这样的好处是，我们将用户与权限的直接对应隔离开，当用户不存在了，我们只需要处理用户表和角色表，而角色和权限的对应关系可以保持不变，再有用户时，只需关联对应角色就好了

### 多个表之间的正查和反查

- 前提：这里有一个学生表和班级表，多对一的关系

```python
# 班级
class Grade(models.Model):
    g_name = models.CharField(max_length=20)
    g_create_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'grade'

# 学生
class Student(models.Model):
    s_name = models.CharField(max_length=20,null=False, unique=True)
    s_create_time = models.DateTimeField(auto_now_add=True)
    s_operate_time = models.DateTimeField(auto_now=True)
    g = models.ForeignKey(Grade)

    class Meta:
        db_table = 'student'
```

#### 一对多

#####多找一

- 我们首先通过学生类找到学生，在通过学生【点】外键【点】属性，就能查找到学生对应的班级信息

```python
student = Student.objects.filter(s_name='')
# 学生对应的班级名称
name = student.g。g_name
```

##### 一找多

- 我们通过班级类找到班级，再通过班级【点】学生_set，可以查找该班级对应的学生

```python
grade = Grade.objects.filter(g_name='python2').first()
# 找到该班级下所有的学生
students = grade.student_set.all()
# 按条件筛选
stu = students.filter(s_chinese__gt= F('s_math')+10)###
```

#### 一对一

- 如果两个表是一对一的关系，假设有唯一性的外键存在于学生表中
- 学生查班级

```python
student.g.g_name
```

- 班级查学生

```python
grade.student.s_name
```

#### F/Q

- 在查询写条件是，有时候我们会用到F/Q函数

##### F函数

- 该函数用于查询条件做计算时
- 如：查询A的值比B的值大10符合条件的结果

```python
students.filter(A__gt= F('B') + 10)
```

- 这里filter不能直接写两个条件的运算，所有要将B用F()函数给包起来
- 注意

```
A__gt    # A大于多少
A__gte    # A大于等于多少
A__lt    # A小于多少
A__lte    # A小于等于多少
```

##### Q函数

- 该函数用于过滤信息
- 如：查询A大于20，或者B小于10   满足条件的结果

```python
students.filter(Q(A__gt=20) | Q(B__lt=10))
```

- 这里的条件运算符有

```
| 或者
& 并且
~ 取反
```



