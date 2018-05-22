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



