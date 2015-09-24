# wechat_forward
基于阿里云Aliyun的微信后台,仅实现转发功能

Fork 自 https://github.com/zhangxc11/wechat_forward.git

----
代码包括两部分
## server
这一部分Python2.7代码运行在阿里云服务器上。部署方法:

* 安装Flask
* 将/Python_server/server.py拷贝到服务器,运行即可.

要实现微信转发,需以下步骤:

* 将需要转发的微信公众号的服务器地址设为服务器地址。

## C# 程序
这一部分是C#程序，实现windows系统中的弹幕功能。程序尝试访问server后，接收从server发送的TCP包，将接收到的内容以弹幕的形式显示在桌面上。在tcpevent.cs中设置好服务器地址，然后使用VS 2012打开，编译即可。