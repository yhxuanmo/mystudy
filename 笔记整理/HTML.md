### HTML

#### 标签

```
HTML - Hyper Text Markup Language - 超文本标签语言
Tag:标签 - Content(装数据、内容)
CSS:层叠样式表 - Display(显示页面、渲染页面)
JavaScript：Behavior(交互行为)

源数据：描述数据的数据

SEO - Search Engine Optimization - 搜索引擎优化

<h1></h1> ……<h6></h6>  总共只有h6

<hr>  水平标尺
<br>  折行标签
<p>   段落标签
<em>  斜体
<strong>   加粗
<sup>	上标
<sub>	下标


快速创建列表
ol>li*5>{Item $}  + tab

<ol>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
    <li>Item 4</li>
    <li>Item 5</li>
</ol>

表格：table /tr/td/th  caption(rowspan/colspan)
快速创建表格	tr 行   td列
table>tr*3>td*4	+tab

图像：img(scr / alt)

表单：form 



划分逻辑区域：div(块级)/span(行级）

标签可以大致分为：行级元素(标签)：一行满了之后再换行；块级元素(标签)：独占一整行
```



#### CSS - 属性

```
:active / :hover
font-size
font-family
font-style
font-weight
color
text-align
letter-spacing
text-decoration
width
height
padding
border
background-image
background-color
margin
display
visibility
list-style
list-style-position
border-collapse

```

- 就近原则

- 具体性原则 Id选择器>类选择器>标签选择器>通配符选择器

- 重要性原则

- 块级元素(block) / 行级(内联)元素(inline)

  - static - 正常文档流
  - relative - 相对定位(相对于元素原来的位置定位 没有脱离文档流 对兄弟元素没有影响)
  - absolute - 绝对定位(相对于父元素来设置位置 脱离了文档流 对兄弟元素有影响)
  - fixed - 固定定位(相对于浏览器窗口来设置元素的位置 脱离了文档流)

-  CSS hack - CSS黑科技(黑客技)

  - 当div中的子元素设置了浮动，外面的父div就没有了高度，要让其有高度值

    ```
    1:在末尾添加一个空的div 设置其属性-清除所有样式：
    <div style="clear: both;"></div>
    2.在父div样式表中添加属性：
    overflow: auto
    ```

- 选择器

  ```
  1标签选择器-对所有的h1标签生效
  2ID选择器:只对指定ID的标签有效
  3类选择器:只对指定的class属性标签生效
  4后代选择器:只有在指定ID下面的div才有效['>'号表示只能是ID的直接子类[如果是空格:表示所有的子类(孙子什么的)有效]
  5伪类:.center>input:hover
  6并列选择器:对他们做同样的事情
  7通配符选择器:对所有的元素有效
  8平级兄弟选择器:.calss~h2(对所有平级的h2有效
  9相邻兄弟选择器:.class+h2(对h2相邻的有效
  ```

  ​


#### JavaScript

- JavaScript 包含

  ```
   ECMAScript - 语法规范 - ES5.1
   BOM - Browser Object Model - 浏览器对象模型 - window
   DOM - Document Object Model - 文档对象模型 - document
  ```

- JS语法

  ```
  1.表示条件用括号括起来
  2.and --> &&    or --> ||    not -->   !
  3.typeof 关键字可以检查数据类型
  4.数据类型：简单数据类型 - number string boolean null undefind array(数组)复杂数据类型 - object
  5.JavaScript中有隐式类型转换‘==’；不带类型转换的比较(全等于/严格等)‘===’
  算术运算符: + - * / %
  赋值运算符: = += -= *= /= %=
  关系运算符: > >= < <= == != === !==
  逻辑运算符: &&(短路与) ||(短路或) !
  位运算符 / 自增自减运算符
  ```

  - js中定义类是通过键值对的形式来实现的

  ```javascript
  // 创建类
  var hotel = {
    	// 对象属性
      'name':'xxx',
    	// 对象方法
    	'func':function(){
      }
  }

  调用对象方法
  hotel.func()
  ```

  - 注意

    ```
    1.如果定义了同名的函数，后定义的会把先定义的函数给覆盖；
    2.函数也可以有可变参数，定义函数的时候‘()’内不写参数，就定义了一个可变参数函数，通过遍历隐藏的arguments对象可以取到传入的值；
    condition ? value1 : value2 - 三元条件运算符 - 问号前面的条件如果成立取冒号前面的值否则取冒号后面的值
    要修改样式直接通过元素的style属性就可以做到
    要读取样式的话需要通过window对象getComputedStyle()
    style属性 - 只写不读
    getComputedStyle() - 只读不写
    addEventListener 方法的第三个参数表示事件处理方式
    	true - 事件捕获 - 从外向里传播事件
    	false - 事件冒泡 - 从里向外传播事件
    preventDefault - 阻止事件的默认行为
    stopPropagation - 阻止事件的传播行为
    evt参数代表的是事件对象 - 绑定了和事件相关的所有信息
    如果事件回调函数中要用到和事件相关的属性和方法就最好指定evt参数
    不管函数是否指定了evt参数当事件发生回调该函数时都会传入该参数
    ```

- window 对象

  ```
  属性
  -location - 地址栏 - href / reload / replace()
  -history - 历史记录 - go() / forward() / back ()
  -navigator - 浏览器
  -screen - 操作系统屏幕 - availWidth / availHeight / width / height
  -alert() / prompt() / confirm()
  -open() / close()
  -setTimeout() / setInterval()
  -clearTimeout() / clearInterval()
  ```

  ​

- document对象

  ```
  查找元素方法：- getElementById() / getElementsByTagName() / getElementsClassName() / querySelector() / 

  querySelectorAll()
  修改节点内容：- textContent / innerHTML / nodeValue
  修改节点属性：- 访问成员运算符 / setAttribute() / getAttribute() / removeAttribute()
  创建新节点： - createElement()
  追加新节点：appendChild() / insertBefore(li,ul.firstChild)
  删除子节点：removeChild()
  ## 如果已经获得一个节点，如何访问它的父节点，子节点，兄弟节点
    父节点:parentNode 
    子节点:children / firstChild / lastChild
    兄弟节点:nextSibling / prevSibling
  ```

- js中的全局函数

  ```
  isNaN() - 判断是不是 不是一个数；
  parseInt() - 取整数，如果取不出返回NaN
  parseFloat() - 取小数，如果取不出返回NaN
  isFinite() - 是不是一个有限数值   无穷大返回false
  eval() - 非常强大的函数
  decodeURIComponent() - 将百分号编码还原
  encodeURIComponent() - 处理成百分号编码

  ```

  ​

#### jQuery

- jQuery 的$函数的作用

  ```
  1. $(function(){}) - $函数中传入的参数是一个函数
  作用：绑定页面加载完成之后要执行的回调函数
  2. $(selector) - $函数中传入的参数是一个选择器
  作用：通过选择器获得对应的元素并将其处理成jQuery对象
  jQuery对象的本质是一个数组
  如果需要将jQuery对象还原成原生的JS对象 - 下标运算[index] / get()
  3. $(elem) - $函数中传入的参数是一个原生JS对象
  作用：将原生JS对象转换为jQuery对象(更多的属性，更多的方法)
  通过jQuery对象的方法在写代码的时候不需要考虑浏览器兼容问题(jQuery已经做了处理)
  4. $(tag) - $函数传入的参数是一个标签
  作用：创建和标签对应的元素并处理成jQuery对象
  ```

- 注意

  ```
  引入多个JS库出现冲突时，可以通过下面的方式让出$函数jQuery.noConflict()
  让出$函数以后原来用$函数的地方全部换成jQuery
  ```

#### Ajax

