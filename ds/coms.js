const WS_URL = "ws://"+location.hostname+":20001";

var WS = new WebSocket(WS_URL);


var tosend = {};

function reconnect() {
	setTimeout(() => {
		WS = new WebSocket(WS_URL);
		// WS.onerror = console.error
	}, 1000)
}
WS.onclose = alert

WS.onmessage = (d) => {
	let obj = JSON.parse(d.data);
	Object.keys(obj).forEach(k=> {
		network["__noset__"+k] = obj[k];
	});
	// console.error("");
}
window.network = new Proxy({}, {
	get(target, name) {
		// console.log("get", name);
		return target[name];
	},
	set(target, name, value) {
		if (name == ("__noset____stdout")) {
			logOutput(value);
			return true;
		}
		if (!name.startsWith("__noset__")) {
			let obj = {};
			obj[name] = value;
			tosend[name] = value;
		} else {
			name = name.substring(9)
		}
		// console.log("set", name, value);
		target[name] = value;
		return true;
	}
})
console.log("wait 2 seconds...")
setTimeout(()=>{
	console.log("connecting...");
setInterval(()=>{
	WS.send(JSON.stringify(tosend));
	tosend = {};
}, 20)
}, 2000);
