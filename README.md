# maoyanTop100
抓取猫眼电影top100的数据

### 简介
第一次接触“正统”的swift项目，发现与之前的OC项目的结构有很大的改变，其中最大的的一点区别是在于在以前的MVC基础之上又独立出一层Manager,如题中所说的MVCM。对比以前的MVC架构，Manager层面主要抽离的是网络访问层面，即在Controller层不会再看早和网络请求数据详细相关的代码，但是会在controller增加一个Manager类型的属性，用以触发请求，以及数据的使用。

### 代码的结构及调用顺序分析
### Manager
* 代码结构
   下面是我自己总结的代码的书写顺序，首先仅代表本人的书写习惯，不一定代表广泛性，另外，我是按照数据获取流程标记的，仅作为思考的顺序，真正的书写的顺序可以根据代码的的美观简洁做具体调整
	1. 继承自网络访问工具类
	2. 定义数据请求函数<br>参数：不做详述，根据具体需求填写<br>网络请求：<br>1.访问网络<br>2.网络访问成功对进行数据存储（存储到结构体）<br>3.回调:此层回调不是以前节结构中的数据网络访问成功时的回调，而是将Manager数据下载存储完毕后对外界的通知，通知控制器可以进行使用数据
	3. 分页相关的代码（一句具体要需求增减)<br>不赘述
	4. 数据存储容器声明及初始化<br>在swift的数据一般存储在结构体中，代替以前的模型类，一般通过json进行初始化，
	5. 回调<br>闭包进行回调，作用参考2中解释typealias dataManagerCallback = (type: HSDataManagerCallType, msg: String, isRefresh: Bool) -> Void
	   以下通过具体代码进行演示<br>
	   ![img M1](http://upload-images.jianshu.io/upload_images/954728-29d28d26b6d00bda.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
	   ![img M2](http://upload-images.jianshu.io/upload_images/954728-83f35fb2ab4577e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### Controller
* 代码结构
控制器中没有了网络访问相关的代码，取而代之的是要对Manager的声明以及初始化，以及通过Manager进行网络请求（在Manager中写好函数，controller中Manager调用函数来触发网络请求）以及在回调中对数据进行获取（如果是tableView 一般是进行刷新数据源操作）
	1. 懒加载Manager，初始化
	2. 发起网络请求
	3. 网络回调
![img C](http://upload-images.jianshu.io/upload_images/954728-44fb112db1d67aa5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### Cell
* 代码结构
关于cell的说一下几点
	1. 与tableView的分离
	cell的创建依旧依赖于tableView，但是在cell的控件的赋值的过程移到cell内部，外部提供一个数据源的接口，在controller层面屏蔽cell内部细节，在cell中懒加载一个数据模型类型的属性，在其didSet进对组件进行复制
	![img Ce1](http://upload-images.jianshu.io/upload_images/954728-0a5814c9d01188fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
	2. tableView 的行高的计算
	在以前的计算行高，用frame 或者 自动布局和frame混合计算，前者对于动态的尺寸的计算，代码量比较大，适合纯代码的开发，后者比前者的优势在于很大部分的布局可以用自动布局实现，实现了大部分的自动化，但是对于行高计算cell行号，要综合计算所有组件的行高的综合，需要用frame进行计算。那么有没有一种可以用自动布局全部搞定的方法，彻底实现自动化。
	#### systemLayoutSizeFittingSize
	![img Ce2](http://upload-images.jianshu.io/upload_images/954728-aaae3af0507475db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
	简单的翻译下官方文档：
	标题是自动布局中的测量
	#### Parameters 
	指出满足约束的最大的或者最小的可能的值
	#### Fitting Size
	此值是以上函数的参数的取值，是个枚举量
	![img Ce3](http://upload-images.jianshu.io/upload_images/954728-6765b4cb7601e102.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
	#### UILayoutFittingCompressedSize 
	使用最小的值作为选项 
	#### UILayoutFittingExpandedSize
	使用最小的值作为选项
	#### 函数总结
	对于button imageView label 等内部有内容的空间可以在固定宽度的情况下，通过systemLayoutSizeFittingSize函数进行压缩（UILayoutFittingCompressedSize）或者（UILayoutFittingExpandedSize）来获取高度值,且系统自动计算。
	![img Ce4](http://upload-images.jianshu.io/upload_images/954728-b9b153a3b623d159.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
	
	3. tableView的优化
##### 数据源方法的执行顺序
###### （1）tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int
###### （2）tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell<br>
##### 代理方法的执行顺序
###### （1）tableView(tableView: UITableView, estimatedHeightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat
执行N次，N为cell的个数
###### （2.1）tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat
###### （2.2）tableView(tableView: UITableView, willDisplayCell cell: UITableViewCell, forRowAtIndexPath indexPath: NSIndexPath) ===>引入此代理就是为了将cell的创建和灌入数据彻底分开，此方法用于灌值
2.1执行一次，2.2执行一次，然后2.1执行，这一套在estimatedHeight之后一对一的配套执行N次N为cell的个数
##### cell展示顺序和数据的灌入（即行高的计算）的矛盾
在cell被灌入数据之前是不能得到精确的行高的，即2.2的执行需在2.1，但是与系统的调用顺序相违背。
##### 解决方案
系统的调用顺序是无法更改的，所以考虑在展示之前先将cell的高度进行计算，然后缓存。高度的计算，依据上文总结只要有了数据即可计算行高，但是前提此方法要依赖cell去执行，故考虑在数据源中增加一个属性，计算每个cell的高度，由于需要对数据进行缓存，故此属性进行懒加载
![](http://upload-images.jianshu.io/upload_images/954728-6cbb352f9b2c5e7d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![img Ce4](http://upload-images.jianshu.io/upload_images/954728-b9b153a3b623d159.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
##### tableView中的调用
![](http://upload-images.jianshu.io/upload_images/954728-ee347b6e7f06843f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)