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



### 全局错误码

```json
0 => ok
999 => unknown err
```



## 登录/注册

##### 登录包：

```json
{
    "cmd": 1,              // 登录包cmd为1
    "data": {
        "uname": $uname,
        "passwd": $passwd           // 登录信息
    }
}
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
