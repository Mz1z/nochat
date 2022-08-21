class NoChat{
	constructor(uname, passwd){
		// websocket 连接对象
		this.conn = null
		this.url = "ws://127.0.0.1:2333"
		this.uname = uname
		this.passwd = passwd
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
	//关闭监听websocket
    _onError(event){
        console.log("close - error:"+event.data);
    }
    _onOpen(event){
        console.log("open:"+this._sockState());
        //console.log(this.conn);
        console.log('连接到: '+this.conn.url)
        // 发送登录包
        var _pack = {}
        _pack.cmd = 1 //登录包
        _pack.data = {}
        _pack.data.uname = this.uname
        _pack.data.passwd = this.passwd
        console.log(_pack)
        this.conn.send(JSON.stringify(_pack))
    };
    _onMessage(event){
        console.log("onMessage")
        console.log("recv: "+event.data)
    }
    _onClose(event){
        console.log("close: "+ this._sockState());
        this.conn.close();
    }
    _sockState(){
        var status = ['未连接','连接成功，可通讯','正在关闭','连接已关闭或无法打开'];
            return status[this.conn.readyState];
    }
 	_send(msg){
        console.log(this.conn);
        console.log("send:" + this._sockState());
        console.log(msg);
        this.conn.send(msg);
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