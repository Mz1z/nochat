# NoChat

[![OSCS Status](https://www.oscs1024.com/platform/badge/Mz1z/nochat.svg?size=small)](https://www.oscs1024.com/project/Mz1z/nochat?ref=badge_small)

基于websocket的聊天工具(开发中)

author: Mz1

email: mzi_mzi@163.com

如果有问题可以issue~

**如果有小伙伴想参与开发可以给我发邮件！**



<hr/>

### 不知道为什么会被收录得到的徽章

[![OSCS Status](https://www.oscs1024.com/platform/badge/Mz1z/nochat.svg?size=large)](https://www.oscs1024.com/project/Mz1z/nochat?ref=badge_large)

<hr/>

### 项目环境(python>=3.7)：

```python
websockets==10.3
```



<hr/>

### 文件目录：

```bash
web/                # web客户端 
db/*.db             # 数据库文件

serve.py               # 服务器脚本
```

<hr/>

### 前端设计

使用原生html+jquery

跨页面的数据保存使用本地储存来实现（还没做）

将和服务器交互的使用封装成一层(正在弄，web/js/NoChatCore.js)
