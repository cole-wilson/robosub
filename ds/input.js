// gamepads =================================================================================
// joypad.set({
// 	axisMovementThreshold: 0.0,
// });
// joypad.on('button_press', (e) => {
// 	console.log(e.detail.index, e.detail.button.value)
// 	network["Controller/Button"+e.detail.index] = true;
// });
// joypad.on('button_release', (e) => {
// 	console.log(e.detail.index, e.detail.button.value)
// 	network["Controller/Button"+e.detail.index] = false;
// });
// joypad.on('axis_move', (e) => {
// 	let axes = e.detail.gamepad.axes;
// 	for (var i=0;i<axes.length;i++) {
// 		// console.log(axes[i])
// 		if (axes[i] < 0.1 && axes[i] > -0.1)
// 			network["Controller/Axis"+i] = 0;
// 		else
// 			network["Controller/Axis"+i] = axes[i];
// 	}
// });
// let gamepad;
function gameLoop() {
	const gamepads = navigator.getGamepads();
	if (!gamepads) {
		return;
	}

	const gamepad = gamepads[0];

	gamepad.buttons.forEach((button, index) => {
		network["Controller/Button"+index] = button.value
	})

	gamepad.axes.forEach((value, index) => {
		var newval = value;
		if (value < 0.1 && value > -0.1){
			newval = 0;
		};
		network["Controller/Axis"+index] = newval
	})

	if (network["Controller/Rumble"]) {
		gamepad.vibrationActuator.playEffect("dual-rumble", {
		  startDelay: 0,
		  duration: 200,
		  weakMagnitude: network["Controller/Rumble"],
		  strongMagnitude: network["Controller/Rumble"],
		});
	}

	requestAnimationFrame(gameLoop);
}
gamepadInfo = document.getElementById("cominfo");
window.addEventListener("gamepadconnected", (e) => {
	gamepadInfo.textContent = "gamepad connected: "+e.gamepad.id;
	gamepad = navigator.getGamepads()[e.gamepad.index];
	gameLoop();
});
window.addEventListener("gamepaddisconnected", (e) => {
  gamepadInfo.textContent = "Waiting for gamepad.";

  cancelAnimationFrame(start);
});

let nums = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'i', 'k', 'j', 'l'];
function inputKeyDown(e) {
	console.log(e)
	let index = nums.indexOf(e.key);
	if (index > -1) network["Controller/Button"+index]=true;
	else {
		if (e.key == 'a') network["Controller/Axis2"]= -1;
		else if (e.key == 'd') network["Controller/Axis2"]= 1;
		else if (e.key == 'w') network["Controller/Axis3"]= -1;
		else if (e.key == 's') network["Controller/Axis3"]= 1;
		else if (e.key == 'ArrowLeft') network["Controller/Axis0"]= -1;
		else if (e.key == 'ArrowRight') network["Controller/Axis0"]= 1;
		else if (e.key == 'ArrowDown') network["Controller/Axis1"]= 1;
		else if (e.key == 'ArrowUp') network["Controller/Axis1"]= -1;
		else if (e.key == 'Return' || e.key == 'Enter' ||  e.key == ' ' || e.key == 'Space') {e.preventDefault();setEnabled(false);}
		else if (e.key == '\\' || e.key == ']') {e.preventDefault();setEnabled(true);}
	}
}
function inputKeyUp(e) {
	let index = nums.indexOf(e.key);
	if (index > -1) network["Controller/Button"+index] =false;
	else {
		if (e.key == 'a') network["Controller/Axis2"]= 0;
		else if (e.key == 'd') network["Controller/Axis2"]= 0;
		else if (e.key == 'w') network["Controller/Axis3"]= 0;
		else if (e.key == 's') network["Controller/Axis3"]= 0;
		else if (e.key == 'ArrowLeft') network["Controller/Axis0"]= 0;
		else if (e.key == 'ArrowRight') network["Controller/Axis0"]= 0;
		else if (e.key == 'ArrowDown') network["Controller/Axis1"]= 0;
		else if (e.key == 'ArrowUp') network["Controller/Axis1"]= 0;
	}
}
window.onkeydown = inputKeyDown;
window.onkeyup = inputKeyUp;
