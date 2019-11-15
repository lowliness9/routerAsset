# routerAsset
A script is designed to discover routers in the network

脚本用于发现网络中的路由器设备,通过发送http请求,进行**规则匹配**,输出结果。

### 使用说明
- - -
![usage.png](https://github.com/lowliness9/routerAsset/blob/master/images/usage.png)

usage: router.py [-h] [-f FILE] [-t TIMEOUT] [-c COUNT]

routerAsset v1.0

optional arguments:  

  -h, --help            show this help message and exit 
 
  -f FILE, --file FILE  文件可以为纯ip或者ip:port形式

### 规则文件
- - -
规则只能匹配响应头中的Server或响应体中的内容
{'type':'respbody_banner','routerName':'','feature':''}
{'type':'respheader_server','routerName':'','feature':''}

### 使用情况
- - -
![task.png](https://github.com/lowliness9/routerAsset/blob/master/images/task.png)

### 其它
- - -
规则目前不太准,误报不少,只能通过http,会漏很多。


