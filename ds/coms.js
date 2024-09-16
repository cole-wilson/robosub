var WS = new WebSocket("ws://localhost:20001");
WS.onmessage = (d) => {
	let obj = JSON.parse(d.data);
	Object.keys(obj).forEach(k=> {
		network["__noset__"+k] = obj[k];
	});
	// console.error("");
}
function reconnect() {
	setTimeout(() => {
		WS = new WebSocket("ws://localhost:20001");
		// WS.onerror = console.error
	}, 1000)
}
WS.onclose = reconnect

var network = new Proxy({}, {
	get(target, name) {
		// console.log("get", name);
		return target[name];
	},
	set(target, name, value) {
		if (!name.startsWith("__noset__")) {
			let obj = {};
			obj[name] = value;
			WS.send(JSON.stringify(obj));
		} else {
			name = name.substring(9)
		}
		// console.log("set", name, value);
		target[name] = value;
		return true;
	}
})
