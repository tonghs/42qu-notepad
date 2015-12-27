是在线的随手贴 
================

### 使用
可以随意的自定义网址来 自己记录 或与 朋友分享 文字 , 比如 :

```http://42qu.cc/test```

为避免自定义的网址相互冲突 

建议您以自己的用户名作为网址前缀 , 比如 :

```http://42qu.cc/zsp/test```

编辑内容的页面 , 每隔三秒会自动保存一次

网页小图标 黑色 , 表示已保存 ; 灰色 , 表示待保存

还有实用的命令行小工具 , Linux / Mac 用户可用以下指令安装

```easy_install -U 42qucc```

粘贴文件 到 随机网址

```42qucc < hi.txt```

 粘贴文件 到 自定义网址 ( http://42qu.cc/test )

```42qucc test < hi.txt```

列出当前目录下的文件 , 并粘贴到 42qu.cc

```ls | 42qucc```

手工输入 , 在命令行中输入内容 ; 按 Ctrl + D , 然后回车 , 结束输入

```42qucc ```

下载文件

```42qucc http://42qu.cc/hi > hi.txt```


### About
诞生于 首届Python中国黑客马拉松 比赛 , 获三等奖

创作团队来自 42qu.com ; 分别是:

张沈鹏、 吕大超、 赵晨旭、 葛原野

现在由天使汇主站开发团队来维护;

原项目部署在 SAE , 现在稍作修改运行在云主机上 , 稍后可能会将修改后的代码开源到 GitHub 上

此项目还有很多可以去细化的地方

比如 浏览修改历史(已经记录 , 但是未展示) , 每日邮件汇总更变 , 设置密码, 利用tornado长连接传送diff做实时同步方便协同办公 , 自定义背景图和字体 , 定义错误提示页面并汇总出错信息 , 搜索自己的笔记 , 编写API文档 , 提供手机版 , 备份表结构的脚本 , 自动化部署到私人的SAE并写文档 , 移植url到kv数据库 等等

*欢迎贡献代码*

最后 , 创意来自 notepad.cc , 设计来自 orderedlist.com
创作的初衷是为想学习python网站开发的新人提供一个演示项目
教程见 网站开发 . 漫游指南 , 其中代码对应的 changeset 是 d8f73e1

### API 文档

API 地址

```http://42qu.cc/:api/txt/```

录入笔记 : POST
使用上传文件的方式 , 上传一个文件名为txt , 经过bzip压缩的文本文件
返回值为生成的随机网址
如果想自定义网址 , 可以使用诸如
http://42qu.cc/:api/txt/test1234

的API地址

```http://42qu.cc/:api/txt/test1234```

读取笔记 : GET

其中 , test1234 为自定义的网址

返回纯文本

