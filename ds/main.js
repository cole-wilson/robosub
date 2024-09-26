var GUI = lil.GUI;
document.getElementById("dashboard").dataset.view = localStorage.getItem("dashboardtype") || "simulation";
document.getElementById("dashboardview").value = localStorage.getItem("dashboardtype") || "simulation";
document.getElementById("dashboardview").onchange = (e) => {
	document.getElementById("dashboard").dataset.view = e.target.value;
	localStorage.setItem("dashboardtype", e.target.value)
}

function setEnabled(value) {
	network.enabled = value;
	if (value)
		document.getElementById("enabler").classList.add("enabled")
	else
		document.getElementById("enabler").classList.remove("enabled")
}



// db_gui = new GUI();
db_folders = {};
db_keys = [];

function update() {
	let parent_el = document.getElementById("networktable");
	parent_el.innerText = JSON.stringify(network, null, 2);


	// // let db = document.getElementById("dashboardpanel");
	// Object.keys(network).forEach(key=>{
	// 	if (!(db_keys.includes(key))) {
	// 		db_keys.push(key)
	// 		split = key.split("/");
	// 		try {
	// 			if (split.length > 1) {
	// 				if (!(split[0] in db_folders)) {
	// 					db_folders[split[0]] = db_gui.addFolder(split[0])
	// 				}
	// 				db_folders[split[0]].add(network, key).name(split[1]);
	// 			} else {
	// 				db_gui.add(network, key).name(key)
	// 			}
	// 		} catch {

	// 		}
	// 	}
	// })

}
setInterval(update, 100)

document.getElementById('sim').contentWindow.addEventListener('keydown',function(e) {e.preventDefault();inputKeyDown(e)}, true);
document.getElementById('sim').contentWindow.addEventListener('keyup',function(e) {e.preventDefault();inputKeyUp(e)}, true);
let textBuffer = "";
function logOutput(a) {
	textBuffer += a;
	const MAXLEN = 10000;
	if (textBuffer.length > MAXLEN) {
		textBuffer = textBuffer.substring(textBuffer.length - MAXLEN);
	}
	let log = document.getElementById("log")
	log.scrollTop = log.scrollHeight;
		log.textContent = textBuffer+"\n";}

document.getElementById("enable").onkeydown = inputKeyDown;
document.getElementById("enable").onkeyup = inputKeyUp;
document.getElementById("disable").onkeydown = inputKeyDown;
document.getElementById("disable").onkeyup = inputKeyUp;
