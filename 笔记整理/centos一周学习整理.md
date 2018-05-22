### 1.文件目录

####目录操作

- 创建：mkdir[^ 1]
- 删除：rmdir[^2];rm[^3]
- 移动：mv[^4]
- 复制：cp[^5]
- 切换目录：cd[^6]
- 显示当前路径：pwd
- 列出当前目录下的文件：ls[^7]
- 查找find/grep[^ 8]


#### 查看文件

- 查看整个文件：cat / tac [^9]
- 显示文件前/后几行： head / tail [^10]
- 一页一页的显示文件：less/more[^11]
- 查看两个文件的差异：diff[^12]

####文件权限

- 改变文件的读、写、执行等权限：chmod[^13]

#### 创建链接

- 硬链接：ln[^14]
- 软连接：ln -s[^ 15]

#### 压缩、归档

- 压缩解压缩：gzip/gunzip[^ 16] ;xz -d/xz -z[^ 17]等
- 归档解归档：tar -cf /tar -xf[^18]

#### 管道和重定向

- 管道   |
- 重定向和错误重定向   >[^19] / 2>



#### 其他

```
ps :查看进程shell
   ps -ef 查看所有进程
   ps -aux 查看所有进程
who:查看登录用户
whoami:查看自己
uname:查看系统 
hostname:主机名
adduser：新建用户
passwd:更改密码     passwd 用户名 ：- 更改该用户名的密码
exit/logout： 退出登录
reboot：重启
shutdown：关机

查看帮助：
man + 命令
info + 命令
命令 --help

whatis:
which:
whereis:

sudo:以管理员身份运行
su:切换用户

history ：查看已经敲过的命令，再用!+命令序号  就可以重新执行该命令

Ctrl + c  终止当前执行的命令

jobs :查看是否后台有任务在执行
fg %数字   将后台执行程序转到前台
bg %数字   将后台暂停的程序在后天激活
```



#### 软件安装

```
yum 安装软件
	yum search 查看有没有该软件
	yum install 安装该软件
rpm 安装软件
	rpm -i 安装
	rpm -e 移除
	rpm -qa | grep 名称 | xargs rpm -e  
	查找已安装的文件，将查找的内容作为参数(xargs)传给后面的命令

源代码构建安装  make && make install
```



#### systemctl

```
centos7.x系统中：
  systemctl start 名称  启动应用
  systemctl stop 名称
  systemctl status 查看任务状态
  systemctl enable 名称  启用开机自启
  systemctl disable 名称  禁用开机自启

在6.x系统中
  service 名称 start
  service 名称 stop
  service 名称 status
```



#### nginx

```
启动： nginx
关闭：kill 进程ID   这里要结束的是nginx: master process的进程ID
```



#### Mysql

```
我们安装的是mariadb -->mysql
启动：systemctl start mariadb
关闭：systemctl stop mariadb
进入mysql:mysql -u root -p,之后会让输入密码，密码为‘空’直接回车
退出mysql:QUIT
```



#### Redis

```
首先要启动redis的服务器端：redis-server myredis.conf > myredis.log &
	注：myredis.conf是我们自己已经修改了的配置文件。需要修改：绑定内网IP；requirepass请求密码
关闭redis服务器端：kill 进程ID
启动redis客户端：redis-cli -h 内网地址；验证密码： auth 密码
退出redis客户端：quit

```



#### vim的使用





#### shell脚本

```
shell脚本注意：
	if语句结束后要加fi
	定义变量：变量名=值  - 等号左右等不能有空格
	$变量  可以取变量的值
	let "变量++" - 可以让变量的值增加
```



#### firewall防火墙

```
1、firewalld的基本使用
启动： systemctl start firewalld
查看状态： systemctl status firewalld 
停止： systemctl disable firewalld
禁用： systemctl stop firewalld
 
2.systemctl是CentOS7的服务管理工具中主要的工具，它融合之前service和chkconfig的功能于一体。
启动一个服务：systemctl start firewalld.service
关闭一个服务：systemctl stop firewalld.service
重启一个服务：systemctl restart firewalld.service
显示一个服务的状态：systemctl status firewalld.service
在开机时启用一个服务：systemctl enable firewalld.service
在开机时禁用一个服务：systemctl disable firewalld.service
查看服务是否开机启动：systemctl is-enabled firewalld.service
查看已启动的服务列表：systemctl list-unit-files|grep enabled
查看启动失败的服务列表：systemctl --failed

3.配置firewalld-cmd

查看版本： firewall-cmd --version
查看帮助： firewall-cmd --help
显示状态： firewall-cmd --state
查看所有打开的端口： firewall-cmd --zone=public --list-ports
更新防火墙规则： firewall-cmd --reload
查看区域信息:  firewall-cmd --get-active-zones
查看指定接口所属区域： firewall-cmd --get-zone-of-interface=eth0
拒绝所有包：firewall-cmd --panic-on
取消拒绝状态： firewall-cmd --panic-off
查看是否拒绝： firewall-cmd --query-panic
 
 
 
那怎么开启一个端口呢
添加
firewall-cmd --zone=public --add-port=80/tcp --permanent    （--permanent永久生效，没有此参数重启后失效）
重新载入
firewall-cmd --reload
查看
firewall-cmd --zone= public --query-port=80/tcp
删除
firewall-cmd --zone= public --remove-port=80/tcp --permanent
```



#### iptables 防火墙



#### Git版本控制

- 自己整理

  ```
  git init - 初始化文件夹，将文件夹变成仓库 -
  git add 文件名 - 将文件加入版本控制 -
  git add .  - 将当前目录的所有文件加入版本控制 - 
  git commit -m '原因' - 提交文件并写说明 -
  git status - 查看暂存区的文件状态 -
  git log - 查看历史版本 -
  git reset --hard 版本号 - 退回某个版本 -
  git reflog - 未来的历史版本 - 
  git checkout --  把暂存区的文件撤回来
  git clone 网络地址 - 把网络地址(远端仓库)克隆到本地 -
  git push origin 分支名称 - 把本地已提交的文件提交到服务器
  		       -master  主分支
  git pull - 把服务器上已更新的文件更新到本地 -
  git remote add origin 网络地址 - 添加远端仓库 -
  	git push -u origin master - 添加远端仓库，第一次提交上要加-u -
  	
  git branch 分支名称  - 创建一个新分支 -
  git branch - 查看所有分支 - 
  git checkout 分支名称 - 选择一个分支 -
  git rm 文件名 - 移除一个文件 -
  git merge 分支名称   - 将分支合并到主干master -
  ```

  ​

- 老师整理

  ```
  本地建仓库再托管到远端服务器
  mkdir hello
  cd hello
  ------------------------------
  git init
  git add .
  git status
  git commit -m 'xyz'
  git log
  git reset --hard id
  git reflog
  git remote add origin <url>
  git push -u origin master
  git pull
  ------------------------------
  远端服务器项目已经存在
  git clone <url>
  cd hello
  git add .
  git checkout --
  git commit -m 'abc'
  git push origin master
  git pull
  ********************************
  Git日常工作流程
  git clone <url>
  cd <dir>
  git branch <name>
  git checkout <name>
  ----------------------
  git add .
  git commit -m 'xyz'
  git push origin <name>
  ----------------------
  git checkout master
  git merge <name>
  git push origin master

  ```

  ​


























































[^ 1]: 创建一个文件夹(目录) 例：mkdir <file>    - 创建了一个file文件夹
[^2]: 只能删除空的文件夹(目录)，非空的文件夹(目录)只能用rm命令
[^3]: 可以删除文件和文件夹(目录)，常用参数：-r(递归)；  -i(交互信息)  -f(强制)  例：rm -rf  <file/目录>   -删除一个文件或非空目录
[^4]: 可以将文件或文件夹(目录)移动到指定位置，如果只在当前目录下”移动“，可以对文件/文件夹(目录)重命名 例1：mv ./file1 ./abc/   -将当前路径下file1 移动到abc文件夹下     例2：mv ./file1 ./file2   -对文件重命名 (在同一个目录下移动可以进行重命名)
[^5]: 可以复制文件或文件夹(目录)移动到指定位置，复制时也可以重命名，常用参数：-r(递归)；例：cp -r <dir>  ./abc/   -将当前路径下dir 移动到abc文件夹下   -复制非空目录
[^6]: 可以切换目录，切换到上一个工作目录： cd - ;切换到home目录： cd or cd ~
[^7]: 可以列出指定目录下文文件，如果未指定则表示当前目录，常用参数：-a(全部文件，包含隐藏文件)；-l(长数据串列出) 例：ls -al  <dir> -列出dir目录下所有文件(含属性)
[^ 8]: find在指定目录查找文件或目录，如果未指定则表示当前目录，常用参数 -name(查找名称) 例：find ./<dir> -name *.txt -在dir目录下查找后缀为.txt的所有文件;grep是文本查找多用于匹配文件内容；两者具体区别请百度
[^9]: cat和tac都是查看整个文件，cat是从第一行开始显示文件内容，tac是从最后一行开始显示内容与cat相反
[^10]: 可以查看文件的前几行或后几行，例：head -5 filename -查看文件的前5行
[^11]: 在查看长文件的时候，可以使用这两个命令一页一页的显示文件内容，查看时可用空格翻页，也可以用pageup,pagedown上下翻页，按q退出查看
[^12]: 用于两个文件的比较，列出两个文件的不同处，例diff file1 file2
[^13]: 用于更改文件的相关权限，格式：chmod [-cfvR] mode file,其中mode 参数有：u(文件拥有者)，g(同组人)，o(其他人)，a(所有人)；+(增加权限),-(取消权限)；r(读),w(写),x(执行)；例：chmod a-r file1 -将file1设为所有人可读；也可以用数字来表示权限r=4,w=2,x =1 例：chmod 777 file -将file权限设为所有人都能读写执行
[^14]: 给文件添加硬链接，将源文件删除一个后还能在其他链接位置找到，相当于给文件进行了备份，例 ：ln file1 ./abc/file2  -给当前文件路径下的file1创建一个硬链接，放在当前路径下的abc目录中重命名为file2
[^ 15]: 给文件添加软连接，将源文件删除后，另一个无法使用，相当于给文件创建了快捷方式，例：ln -s ./abc/file1 file2  - 在当前路径下创建file1的软连接(快捷方式)，重命名为file2
[^ 16]: 针对后缀名为.gz的压缩文件，可以用tar -zcvf 直接归档并压缩/tar -zxvf 直接解压缩解归档
[^ 17]: 针对后缀名为.xz的压缩文件
[^18]: 用于创建归档和解归档。归档：tar -cf 新文件  被归档文件 例：tar -cf dir.tar 1.txt 2.txt   - 将1.txt 2.txt两个文件归档为dir.tar文件；解归档：tar  -xf 文件名 例：tar -xf dir.tar 解归档dir.tar文件。tar -zcf 可以将文件归档并压缩(.gz文件)，tar -zxf 可以直接将.tar.gz文件直接解压并解归档
[^19]: >输出重定向，当再次重定向到同一文件时，会覆盖之前的内容；>>追加输出重定向，当再次重定向到同一文件时，是在文件中继续追加