### Flask中的一对多模型关系

- 关系型数据库中表的一对多关系，在flask框架下的定义和django中有很大的不同
- 这里我们创建班级和学生的一对多关系模型
- 学生模型

```python
class Student(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(16))
    s_age = db.Column(db.Integer,default=18)
    grades = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

    __tablename__ = 'student'
```

- 班级模型

```python
class Grade(db.Model):
    g_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(16), unique=True, nullable=False)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    students = db.relationship('Student', backref='grade', lazy=True)

    __tablename__ = 'grade'
```

- 需要注意的是，在 ‘一’ 的一方指定关联关系relationship，在 ‘多’ 的一方指定外键ForeignKey，
- 定义关系时relationship('Student', backref='grade', lazy=True)，第一个参数为**类名**，第二个参数是backref是一个反向身份的代理,相当于在Student类中添加了grade的属性，第三个参数lazy默认为True
- 建立外键关联db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)，需要注意的是db.ForeignKey('grade.g_id')中的参数是，**表名.列名**

#### lazy参数

- 官网解释有如下几个lazy的参数：

```
lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据:，有如下四个值:

select/True: (which is the default) means that SQLAlchemy will load the data as necessary in one go using a standard select statement.

joined/False: tells SQLAlchemy to load the relationship in the same query as the parent using a JOIN statement.

subquery: works like ‘joined’ but instead SQLAlchemy will use a subquery.

dynamic: is special and useful if you have many items. Instead of loading the items SQLAlchemy will return another query object which you can further refine before loading the items. This is usually what you want if you expect more than a handful of items for this relationship

```

- select就是访问到属性的时候，就会全部加载该属性的数据，**占用内存多，但是访问数据快。**
- joined则是在对关联的两个表进行join操作，从而获取到所有相关的对象。
- dynamic则不一样，在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相应方法才可以获取对象。

#### 一找多

- 通过班级找学生

```python
grade = Grade.query.get(g_id)
student_list = grade.students
#student_list结果#
[<Student 8>, <Student 21>, <Student 31>, <Student 32>]
#student_list结果#
```

- 直接通过班级结果.students(班级模型中的relationship字段)

#### 多找一

- 通过学生找班级

```python
student = Student.query.get(s_id)
grade = student.grade
```

- 学生的结果.grade(班级模型中，backref的值)

### Flask中的多对多模型关系

- 在flask中，多对多关系模型，需要自己定义中间表
- 这里我们创建学生和课程的多对多模型
- 学生模型

```python
class Student(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(16))
    s_age = db.Column(db.Integer,default=18)
```

- 课程模型

```python
class Course(db.Model):
    c_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    c_name = db.Column(db.String(32), unique=True)
    c_create_time = db.Column(db.DateTime, default=datetime.now)
    students = db.relationship('Student', secondary=sc, backref='course')
```

- 中间表

```python
sc = db.Table('sc',
              db.Column('s_id', db.Integer, db.ForeignKey('student.s_id'), primary_key=True),
              db.Column('g_id', db.Integer, db.ForeignKey('course.c_id'), primary_key=True)
              )
```

- 多对多模型中，relationship放在任意一个模型中都可以，需要注意的是：在relationship中要指定**secondary参数关联中间表**
- 在中间表中第一个参数要与中间表名一致(这里指的是sc和‘sc’)，在中间表指定两个外键分别关联学生模型和课程模型
- sc表由**db.Table声明**，我们不需要关心这张表，因为这张表将会由SQLAlchemy接管，它唯一的作用是作为students表和courses表关联表 

#### 添加学生和课程的关系

- 学生和课程的get查询结果是一个列表，可以通过append向列表中追加数据，在commit()提交，就可以建立关联关系了
- 方式一：课程的学生列表中添加学生对象

```python
stu = Student.query.get(s_id)
course = Course.query.get(c_id)
course.students.append(stu)
db.session.add(course)
db.session.commit()
```

- 方式二：学生的课程列表中添加课程对象

```python
stu = Student.query.get(s_id)
cour = Course.query.get(c_id)
student.course.append(cour)
db.session.add(student)
db.session.commit()
```

#### 删除学生和课程的关系

- 学生和课程的get查询结果是一个列表，可以通过remove移除列表中的对象，在commit()提交，就可以删除关联关系了
- 方式一：课程的学生列表中删除学生对象

```python
stu = Student.query.get(s_id)
course = Course.query.get(c_id)
course.students.remove(stu)
db.session.commit()
```

- 方式二：学生的课程列表中删除课程对象

```python
student = Student.query.get(s_id)
cour = Course.query.get(c_id)
student.course.remove(cour)
db.session.commit()
```

#### 学生找课程

```python
stu = Student.query.get(id)
course_list = stu.course
```

- 学生的结果.grade(课程模型中，backref的值)

#### 课程找学生

```python
cou = Course.query.get(id)
student_list = cou.students
```

- 直接通过课程结果.students(课程模型中的relationship字段)

### 一对一模型

- 一对一模型关系的建立，只需要在一对多的模型的relationship()中加入uselist=False参数即可，这里不再举例说明