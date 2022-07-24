# API文档

> 基于这个进行开发吧！

所有的数据包均以json格式进行发送。



### 常规数据包格式:

#### 请求包：

```json
{
	"cmd": 1,           // 操作码
    "data": []           // 数据(可省略)
}
```



#### 回应包：

```json
{
    "code": 0,               // 错误码
    "msg": "login success",     // 提示信息
    "data": [                  // 数据(可省略)
        "asd",
        "123"
    ]
}
```



### 全局操作码(cmd)

```bash
1 => 登录包(客户端发送)
5 => 通知包(服务端发送)(收到消息等等)
10 => 获取聊天记录(客户端发送)
11 => 发消息(客户端发送)
233 => 心跳包(客户端发送)
```



### 全局错误码(code)

```json
0 => ok
999 => unknown err
```





## 登录(cmd=1)

> 连接建立的5s之内需要发送登录包，否则断开连接。

##### 登录包：

```json
{
    "cmd": 1,              // 登录包cmd为1
    "data": {
        "uname": $uname,
        "passwd": $passwd           // 登录信息
    }
}
// 快捷复制(测试用)
// {"cmd":1, "data":{"uname":"Mz1","passwd":"123456"}}
```

登录成功回应：

```json
{
    "code": 0,                  // 错误码
    "msg": "login success",     // 提示信息
    "data": {$用户信息}          // 返回基本用户信息
}
```

错误码：

```json
1 => wrong uname or passwd
```



##### 注册(http)：

注册预计使用http进行？



## 心跳包(cmd=233)

每30s发送一次，不得超过60s

```json
{
	"cmd": 233
}
```



## 通知包(cmd=5)

```json
{
    "cmd": 5,
    "data": {
        "type": "recvmsg",      // 通知类型
        "data": {              // 通知内容(示例为收到消息包)
            "from_uid": $from_uid,
            "text": $text
        }
    }
}
```





## 发消息(cmd=11)

给某某用户发消息

参数：to_uid, text

```json
{
    "cmd": 11,
    "data": {
        "to_uid": $to_uid,         // 给谁发消息
        "text": $text              // 消息内容
    }
}
```



## 获取聊天记录(cmd=10)

```json
{
    "cmd": 10,
    "data": {
        "from_uid": $from_uid,        // 从哪个联系人那边来的聊天记录
        "len": $len,                  // 获取几条，若为空则获取最新的一条
    }
}
```

