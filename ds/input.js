
// gamepads =================================================================================
joypad.set({
	axisMovementThreshold: 0.0,
});
joypad.on('button_press', (e) => {
	network["Controller/Button"+e.detail.index] = true;
});
joypad.on('button_release', (e) => {
	network["Controller/Button"+e.detail.index] = false;
});
joypad.on('axis_move', (e) => {
	let axes = e.detail.gamepad.axes;
	for (var i=0;i<axes.length;i++) {
		console.log(axes[i])
		if (axes[i] < 0.1 && axes[i] > -0.1)
			network["Controller/Axis"+i] = 0;
		else
			network["Controller/Axis"+i] = axes[i];
	}
});
let nums = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'i', 'k', 'j', 'l'];
window.onkeydown = (e) => {
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
	}
}
window.onkeyup = (e) => {
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
