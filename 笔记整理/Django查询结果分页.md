### Django查询结果分页

- 在日常的项目中，有时候我们查询的结果有很多，我们希望分页展示，这时候在后端我们就需要将得到的数据进行分页处理

#### 在后端处理分页

- 在后端处理分页，我们需要引入django.core.paginator下的Paginator模块
- 我们通过Paginator将查询结果进行分页，并指定每页数量

```python
def grade(request):
    if request.method == 'GET':
        # 通过equest.GET.get取到url中的参数，如果没有默认为1
        page_num = request.GET.get('page_num', 1)
        grades = Grade.objects.all()
        # 对grades进行分页，每页3条数据
        paginator = Paginator(grades, 3)
        # 通过分页对象.page()获取指定页数的数据
        pages = paginator.page(int(page_num))
        return render(request, 'grade.html',{'pages':pages})
```

- 我们也可以在项目setting中指定默认的分页静态常量
- setting中

```python
# 分页条数
PAGE_NUMBERS = 3
```

- views中

```python
paginator = Paginator(grades, PAGE_NUMBERS)
```

#### 在html中处理分页结果

```
    {% for page in pages %}
<tr>
<td>{{ page.id }}</td>
<td>{{ page.g_name }}</td>
<td>{{ page.g_create_time }}</td>
<td><a href="{% url 'app:changegrade' %}?g_id={{ page.id }}">编辑</a></td>
</tr>
    {% endfor %}
```

#### Paginator对象

- 我们通过Paginator()创建的对象，有很多有用的属性

```python
# 创建对象
paginator = Paginator(grades, 3)
# 属性
paginator.page(number) # 获取指定页数的内容
paginator.page_range # 获取页数的range
paginator.num_pages # 获取总页数
paginator.count # 获取该对象包含信息的总条数
```



#### page对象

- 每一个分页对象(page)，也有很多有用的属性

```python
# 创建指定分页对象
pages = paginator.page(num)
# 属性
pages.number # 获取当前对象对应的页数
pages.has_next() # 判断是否还有下一页
pages.has_previous # 判断是否还有上一页
pages.next_page_number() # 获取下一页的页数
pages.previous_page_number # 获取上一页的页数
```

#### 制作分页页码

- 在html中，我们的分页内容都会有对应的分页页码和上一页、下一页等
- 通过Paginator对象和page对象的相关属性我们可以轻松的制作分页页码

```
<ul id="PageNum">
<li><a href="{% url 'app:grade' %}">首页</a></li>
{% if pages.has_previous%}
<li><a href="{% url 'app:grade' %}?page_num={{ pages.previous_page_number }}">上一页</a></li>
{% endif %}
    {% for i in pages.paginator.page_range %}
<li><a href="{% url 'app:grade' %}?page_num={{ i }}">{{ i }}</a></li>
    {% endfor %}
{% if pages.has_next %}
<li><a href="{% url 'app:grade' %}?page_num={{ pages.next_page_number }}">下一页</a></li>
{% endif %}
<li>当前{{ pages.number }}页</li>
<li><a href="{% url 'app:grade' %}?page_num={{ pages.paginator.num_pages }}">尾页</a></li>
</ul>
```

