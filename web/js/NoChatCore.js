// 数据包类
class NoChatPacket{
	constructor(serial=-1, data=null){
		this.code = 0
		this.cmd = 5
		this.msg = "ok"
		this.serial = serial
		this.data = data
	}
	loads(str){
		// 将字符串转化成包
		// console.log(str)
		let _pack = JSON.parse(str)
		this.code = _pack.code
		this.cmd = _pack.cmd
		this.msg = _pack.msg
		this.serial = _pack.serial
		this.data = _pack.data
		console.log(this)
	}
	code_dumps(){
		// 将包转化为json字符串
		var _pack = {}
		_pack['code'] = this.code
		_pack['msg'] = this.msg
		_pack['data'] = this.data
		return JSON.stringify(_pack)
	}
	cmd_dumps(){
		// 将包转化为json字符串
		var _pack = {}
		_pack['cmd'] = this.cmd
		_pack['serial'] = this.serial
		_pack['data'] = this.data
		return JSON.stringify(_pack)
	}
}

// 用户使用的类
// 前面有下划线的函数为内部函数，不应该被外部使用
class NoChat{
	constructor(uname, passwd){
		// 没啥意义的输出
		console.log('################################')
		console.log('#####  NoChat Core v0.0.1  #####')
		console.log('################################')
		// websocket 连接对象
		this.conn = null
		this.url = "ws://127.0.0.1:2333"
		this.uname = uname
		this.passwd = passwd

		this.serial = 1
		this.pack_list = []      // 发包后等待回包的列表
	}
	login(){
		this.conn = new WebSocket(this.url)      // 建立连接
		// 设置回调函数
		let that = this
		this.conn.onerror = function (event){
	        that._onError(event);
	    };
	    // 打开websocket
	    this.conn.onopen = function (event){
	        that._onOpen(event);
	    };
	    //监听消息
	    this.conn.onmessage = function (event){
	        that._onMessage(event);
	    };
	    this.conn.onclose = function (event){
	        that._onClose(event);
	    }
	}
	// 给谁发消息
	talk_to(to_uid, text){
		var pack = new NoChatPacket(this.serial)
		this.serial ++
		pack.cmd = 11
		pack.data = {}
		pack.data['to_uid'] = to_uid
		pack.data['text'] = text
		this.pack_list.push(pack)          // 将要发送的包推入发送列表的结尾
		console.log(this.pack_list)        // 测试用，输出当前的等待回包列表
		this._send(pack.cmd_dumps())
	}
	// 加好友
	add_friend(uid){
		// ...
	}
	// 删除好友
	delete_friend(uid){
		// ...
	}
	// 确认已读消息
	read_msg(){
		// ...
	}
	// 获取未读消息
	// 此函数应该在每次登陆之后就调用
	// 在用户主动刷新的时候也应调用此函数
	// cmd=14
	fetch_msg(){
		var pack = new NoChatPacket(this.serial)
		this.serial ++
		pack.cmd = 14
		this.pack_list.push(pack)      // 将数据包推入等待回包的列表
		console.log(this.pack_list)    // 测试用
		this._send(pack.cmd_dumps())
	}

	//关闭监听websocket
    _onError(event){
        console.log("close - error:"+event.data);
    }
    _onOpen(event){
        console.log("open:"+this._sockState());
        //console.log(this.conn);
        console.log('已连接上服务器: '+this.conn.url)
        // 发送登录包
        var _pack = new NoChatPacket(this.serial)
        this.serial ++
        _pack.cmd = 1 //登录包
        _pack.data = {}
        _pack.data.uname = this.uname
        _pack.data.passwd = this.passwd
        this._send(_pack.cmd_dumps())
    };
    _onMessage(event){
        console.log("recv: "+event.data)
        // 解包，检查响应包的序列号与之前的哪个包相符
        let pack = new NoChatPacket()
        pack.loads(event.data)
        // 之后做相应的处理
        // 检查是不是响应包
        if (pack.serial != -1 && pack.code !== undefined){
        	// 是响应包，与列表中的包进行对比
        	for(let i = 0; i < this.pack_list.length; i ++){
        		if (pack.serial == this.pack_list[i].serial){
        			// 找到确认的包
        			console.log('收到回包~')
        			// 做一些处理啥的
        			// ...
        			// 从列表中删除这个包
        			this.pack_list.splice(i, 1)
        			break
        		}
        	}
        	console.log(this.pack_list)
        }

    }
    _onClose(event){
        console.log("close: "+ this._sockState());
        this.conn.close();
    }
    _sockState(){
        var status = ['未连接','连接成功，可通讯','正在关闭','连接已关闭或无法打开'];
            return status[this.conn.readyState];
    }
    // 底层发包函数，直接发包不做处理
 	_send(pack){
        // console.log(this.conn);
        console.log("send:" + this._sockState());
        console.log(pack);
        this.conn.send(pack);
    }
    _close(event){
        this.conn.close();
    }
    // 发送心跳包的函数
    _heartbeat(){
    	// ...
    	// 需要确认回包(目前是这样设计的)
    }
}


let chat = new NoChat('Mz1', '123456')
chat.login()