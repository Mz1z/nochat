
class NoChatPacket{
	constructor(serial=-1, data=null){
		this.code = 0
		this.cmd = 5
		this.msg = "ok"
		this.serial = -1
		this.data = data
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

class NoChat{
	constructor(uname, passwd){
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
		this._send(pack.cmd_dumps())
	}
	//关闭监听websocket
    _onError(event){
        console.log("close - error:"+event.data);
    }
    _onOpen(event){
        console.log("open:"+this._sockState());
        //console.log(this.conn);
        console.log('连接到: '+this.conn.url)
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
        // console.log("onMessage")
        console.log("recv: "+event.data)
        // 解包，检查响应包的序列号与之前的哪个包相符
        // 之后做相应的处理
        // ...
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

    }
}

console.log('#####  NoChat Core v0.0.1  #####')
let chat = new NoChat('Mz1', '123456')
chat.login()