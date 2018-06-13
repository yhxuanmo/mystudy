## flask框架中的模板

- 在flask中，使用的是jinjia2模板引擎，jinjia2和django的模板引擎有很多相似的地方
- 和django一样我们在html页面中使用{{ name }}来存放后端传递的变量，使用{% tag %}来做逻辑控制等
- {% tag %}在jinjia2中还可以用于定义函数

### 基础模板的定义和继承

- 和django一样，在jinjia2中可以定义基础模板，然后其他html页面继承自基础模板
- 在jinjia2中同样使用{% block xxx %}{% endblock %}来提供占位

```
# 基础模板base.html
<title>
{% block xxx %}

{% endblock %}
</title>
```

- 在其他html中继承基础模板base.html

```
# 引入基础模板
{% extends 'base.html' %}

# 开始填自己的内容
{% block title %}
    分数
{% endblock %}
```

- 有时我们可以将共有的部分写入模板内，如果我们继承之后，需要在该占位符中添加其他的内容，需要用到{{ super() }}将基础模板中的内容导入，然后在写自己的内容。如果直接往占位符中写内容会覆盖模板中原有的内容

```
# 模板 #
{% block extCSS %}
	<link rel="stylesheet" href="/static/css/index.css">
{% endblock %}
# 模板 #

# 继承基础模板 #

{% block extCSS %}
	{{ super() }}
	<link rel="stylesheet" href="/static/css/xxxx.css">
{% endblock %}

# 继承基础模板 #
```

- 注意这里super继承基础模板的内容与django稍有不同。
- Django:{{ block.super }}
- jinjia2：{{ super() }}

### 宏定义和导入

- jinjia2中，有时候我们可以在html中定义函数，代替一些重复的代码，需要使用macro

#### 定义函数

- 可以直接在当前html文件中定义函数，也可以将所有函数定义在公共的html文件中，需要的时候直接导入

```
{% macro show_goods(id, name) %}
	商品id:{{id}}   
	名称：{{ name }}
{% endmacro %}
```

- 定义的函数可以有参数，也可以没有参数

#### 函数的调用

- 定义好函数之后，就可以调用函数了
- 在定义函数的html文件中调用该函数

```
# 直接调用
{{ show_goods(3,'肥宅快乐水') }}
```

- 在其他文件中调用已定义的函数，这就需要导入了，这和python中导入模块的方法类似

```
# 从common.html文件中导入相关函数
{% from 'common.html' import show_goods %}
# 调用
{{ show_goods(3,'肥宅快乐水') }}
```

### 循环和过滤器

#### 循环

- jinjia2中的循环和django中的for循环是一致的

```
{% for X in XX %}
{% endfor %}
```

- 在获取循环信息的时候和django有些不同
- Django：forloop
- jinjia2 : loop

#### 过滤器

- 在解析变量的时候，可以使用过滤器对变量中的数据做一些处理
- 语法：{{ 变量|过滤器|过滤器... }}

```
# 后端传递数据 #
content_h2 = '<h2>仙剑奇侠传</h2>'
# 后端传递数据 #
```

- 对于上述后端传递的带有h2标签的数据，如果直接{{content_h2}}解析，结果只是解析出整个字符串，并不能渲染该标签，这时我们就需要用到过滤器safe

```
渲染样式的: {{ content_h2|safe }}
```

- 其他的过滤器

```
capitalize 单词首字母大写
lower 单词变为小写
upper 单词变为大写
title
trim 去掉字符串的前后的空格
reverse 单词反转
format
striptags 渲染之前，将值中标签去掉
safe 讲样式渲染到页面中
default
last 最后一个字母
first
length
sum
sort
```

### 模板中静态文件的加载

- 在模板中我们需要加载静态文件，这里将jinjia2和django 的加载方式对比来看

#### 直接写死路径

- 直接将静态文件的路径写死，这在jinjia2和django中都是一样的

```
<link rel="stylesheet" href="/static/css/index.css">
```

#### 反解析路径

- 反解析静态文件的路径，这种方式更加灵活方便，就算移动了静态文件位置，我们只需要配置一下设置中的静态路径即可实现全局更改
- django

```
{% load static %}
<link rel="stylesheet" href="{% static 'css/index.css' %}">
```

- jinjia2

```
<link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">
```

