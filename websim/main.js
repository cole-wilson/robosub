import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { DragControls } from 'three/addons/controls/DragControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

let thrusters;
window.THREE = THREE

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.up.set(0, 0, 1)
const renderer = new THREE.WebGLRenderer();
const controls = new OrbitControls( camera, renderer.domElement );
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );


const camcamera = new THREE.PerspectiveCamera( 75, 1, 0.1, 1000 );
const camrenderer = new THREE.WebGLRenderer({preserveDrawingBuffer: true});
camrenderer.setSize( 100, 100 );
document.body.appendChild( camrenderer.domElement );

window.camcanvas = camrenderer.domElement

const geometry = new THREE.TorusGeometry(0.4, 0.05, 16, 100);
const material = new THREE.MeshBasicMaterial( { color: "orange" } );
const note = new THREE.Mesh( geometry, material ); scene.add( note );


let dcontrols = new DragControls( [ note ], camera, renderer.domElement );

eel.expose(getcanvasdata);
function getcanvasdata() {
	var webglCanvas = camcanvas;

	var offscreenCanvas = document.createElement("canvas");
	offscreenCanvas.width = webglCanvas.width;
	offscreenCanvas.height = webglCanvas.height;
	var ctx = offscreenCanvas.getContext("2d");

	ctx.drawImage(webglCanvas,0,0);
	var imageData = ctx.getImageData(0,0, offscreenCanvas.width, offscreenCanvas.height).data;
	var out = Array.from(imageData);
	// console.log(imageData)
	return out;
}

note.rotation.z=(Math.PI/4);
note.rotateY(Math.PI/4);
note.rotateX(Math.PI/4);
note.position.x = -5;
note.position.y = 15;
note.translateZ(1);

// const geometry = new THREE.BoxGeometry(10/12, 10/12, 10/12);
// const material = new THREE.MeshPhongMaterial( { color: 0xff0000 } );

const oloader = new GLTFLoader();
function loadSub() { return new Promise((resolve, reject) => {
	oloader.load( './dirtybubble.glb', function ( gltf ) {
		resolve( gltf.scene );

	}, undefined, function ( error ) {

		reject( error );

	} );
});}
function loadProp() { return new Promise((resolve, reject) => {
	oloader.load( './prop.glb', function ( gltf ) {
		resolve( gltf.scene );

	}, undefined, function ( error ) {

		reject( error );

	} );
});}


const sub = await loadSub();
var bbox = new THREE.Box3().setFromObject(sub);
console.log(bbox)
const prop = await loadProp();
sub.scale.x = 8;
sub.scale.y = 8;
sub.scale.z = 8;
sub.rotation.y = Math.PI
sub.translateY(-1);

let cube = new THREE.Object3D();
window.sub = sub;
cube.add(sub)
// gltfloader.load( './dirtybubble.glb', function ( gltf ) {

// 	cube = gltf.scene;
// 	console.log(cube)
// 	scene.add( gltf.scene );

// }, undefined, function ( error ) {

// 	console.error( error );

// } );

// const cube = gltfloader.load("/sub.gltf")

// const cube = new THREE.Mesh( geometry, material );
scene.add( cube );
window.cube = cube;


const axesHelper = new THREE.AxesHelper( 10 );
scene.add(axesHelper);

// const light = new THREE.AmbientLight(0xFFFFFF);
// light.intensity = 400;
// scene.add(light);
// const light = new THREE.PointLight( 0xffffff, 100, 100);
// light.position.set( 50, 50, 50 );
// scene.add( light );
const directionalLight = new THREE.DirectionalLight( 0xffffff, 100);
directionalLight.position.z = 100
directionalLight.position.y = 0
scene.add( directionalLight );
const directionalLight2 = new THREE.DirectionalLight( 0xffffff, 100);
directionalLight2.position.z = 1
directionalLight2.position.y = 0
scene.add( directionalLight2 );

const loader = new THREE.TextureLoader();
const texture = loader.load( '/floor.jpg' );
texture.colorSpace = THREE.SRGBColorSpace;
texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
texture.repeat.set(1000, 1000);

const ground = new THREE.Mesh(
					new THREE.PlaneGeometry(10000, 10000, 1, 1),
					new THREE.MeshBasicMaterial({map: texture})
				);
				ground.position.z = -2;

				// ground.rotation.x = - Math.PI / 2; // rotates X/Y to X/Z
				ground.receiveShadow = true;
				scene.add( ground );

// const waterline = new THREE.Mesh(
// 					new THREE.PlaneGeometry(10000, 10000, 1, 1),
// 					new THREE.MeshPhongMaterial({color: "blue"})
// 				);
// 				waterline.position.z = 20;

// 				waterline.receiveShadow = true;
// 				scene.add( waterline );

camera.position.x = 2.6;
camera.position.y = -2.8;
camera.position.z = 3.15;
// controls.target = camera.position
controls.update();

window.cam = camera;

let vectorArrows = [];
let vectorArrowsReverse = [];


const Force_M = 1;
const Torque_M = 1;

let speedx = 0;
let speedy = 0;
let speedz = 0;
let rotspeedx = 0;
let rotspeedy = 0;
let rotspeedz = 0;

window.clear = function() {
	for (var i=0;i<thrusters.length;i++) {
		let motor = thrusters[i];
		motor.set_speed(0);
	}
	speedx = 0;
	speedy = 0;
	speedz = 0;
	rotspeedx = 0;
	rotspeedy = 0;
	rotspeedz = 0;
	cube.position.x = 0;
	cube.position.y = 0;
	cube.position.z = 0;
	cube.rotation.x = 0;
	cube.rotation.y = 0;
	cube.rotation.z = 0;
}

function get_gravbouyancy() {
	if (document.getElementById("gravity").checked) {
		return 2;
	} else {
		return 0;
	}
}
function r(a) {
	return Math.round(100*a)/100;
}
let info = document.getElementById("info");
const VECTOR_SCALE = 1;
async function animate() {
	eel.set_network("enabled", document.getElementById("enabled").checked)
	// renderer.setSize( window.innerWidth, window.innerHeight );
	// let results = pyodide.runPython("get_movement(motors)").toJs();
	thrusters = await eel.get_motors()();
	let results = await eel.get_movement()();

	// console.log("results =", results)

	speedx = results[0] * Force_M * (1/60);
	speedy = results[1] * Force_M * (1/60);
	speedz = (results[2] + get_gravbouyancy()) * Force_M * (1/60);
	rotspeedx = results[3] * Torque_M * (1/60);
	rotspeedy = results[4] * Torque_M * (1/60);
	rotspeedz = results[5] * Torque_M * (1/60);

	for (var i=0;i<thrusters.length;i++) {
		let motor = thrusters[i];
		if (motor.speed > 0) {
			vectorArrows[i].setLength(motor.speed * VECTOR_SCALE);
			vectorArrowsReverse[i].setLength(0)
		}
		else {
			vectorArrowsReverse[i].setLength(-motor.speed * VECTOR_SCALE)
			vectorArrows[i].setLength(0);
		}
		// console.log(vectorArrows[i])
	}


	// cube.rotation.reorder( 'ZXY' );
	cube.rotateX(rotspeedx);
	cube.rotateY(rotspeedy);
	cube.rotateZ(rotspeedz);
	// cube.rotation.x -= rotspeedx;
	// cube.rotation.y -= rotspeedy;
	// cube.rotation.z -= rotspeedz;


	info.innerHTML = `
position: (${r(cube.position.x)}, ${r(cube.position.y)}, ${r(cube.position.z)})<br>
rotation: (${r(cube.rotation.x)}, ${r(cube.rotation.y)}, ${r(cube.rotation.z)})<br>
	`;
	// console.log(speedx, speedy, speedz)

	let prevcubepos = new THREE.Vector3();
	prevcubepos.copy(cube.position)

	cube.translateX(speedx);
	cube.translateY(speedy);
	cube.translateZ(speedz);

	controls.target = cube.position;

	camera.position.x -= prevcubepos.x - cube.position.x;
	camera.position.y -= prevcubepos.y - cube.position.y;
	camera.position.z -= prevcubepos.z - cube.position.z;
	// camera.lookAt(cube.position)

	// ground.position.set(cube.position);
	// texture.offset.set(cube.position.x / 900 * texture.repeat.x, cube.position.y / 900 * texture.repeat.y);

	controls.update();
	eel.set_network("IMU/pitch", cube.rotation.x);
	eel.set_network("IMU/roll", cube.rotation.y);
	eel.set_network("IMU/yaw", cube.rotation.z);
	eel.set_network("IMU/accel_x", speedx);
	eel.set_network("IMU/accel_y", speedy);
	eel.set_network("IMU/accel_z", speedz);



	camcamera.position.x = cube.position.x;
	camcamera.position.y = cube.position.y;
	camcamera.position.z = cube.position.z+1.2;
	// camcamera.lookAt(cube.position)
	camcamera.rotation.reorder( 'ZYX' );
	camcamera.rotation.y = cube.rotation.y;
	camcamera.rotation.x = cube.rotation.x + (Math.PI * (90/180));
	camcamera.rotation.z = cube.rotation.z;

	renderer.render( scene, camera );
	camrenderer.render( scene, camcamera );
}


async function main() {
	// let code = await (await fetch("/main.py")).text();
	// pyodide = await loadPyodide();
	// await pyodide.loadPackage("numpy")
	// await pyodide.loadPackage("matplotlib")
	// await pyodide.loadPackage("scipy")
	// pyodide.runPython(code);

	// thrusters = pyodide.globals.get('motors').toJs();
	thrusters = await eel.get_motors()();
	window.motors = thrusters;


	for (var i=0;i<thrusters.length;i++) {
		let motor = thrusters[i];
		var from = new THREE.Vector3( motor.x, motor.y, motor.z);
		let coeffs = motor.force_coefficients;
		// console.log(coeffs);
		let force = 100;
		var to = new THREE.Vector3( motor.x + force*coeffs[0], motor.y + force*coeffs[1], motor.z + force*coeffs[2] );
		var direction = to.clone().sub(from);
		var length = direction.length();
		var arrowHelper = new THREE.ArrowHelper(direction.normalize(), from, length, "purple" );
		arrowHelper.line.material.linewidth = 0.5;
		cube.add( arrowHelper );
		vectorArrows.push(arrowHelper)

		let motorProp = prop.clone();
		motorProp.position.x = motor.x;
		motorProp.position.y = motor.y;
		motorProp.position.z = motor.z;
		motorProp.scale.x = 8;
		motorProp.scale.y = 8;
		motorProp.scale.z = 8;

		motorProp.rotation.reorder( 'ZYX' );
		motorProp.rotation.z = Math.PI * (motor.theta/180)
		motorProp.rotation.x = Math.PI * (motor.phi/180)


		cube.add(motorProp)


		to = new THREE.Vector3( motor.x - force*coeffs[0], motor.y - force*coeffs[1], motor.z - force*coeffs[2] );
		direction = to.clone().sub(from);
		length = direction.length();
		let arrowHelperReverse = new THREE.ArrowHelper(direction.normalize(), from, length, "orange" );
		arrowHelperReverse.line.material.linewidth = 0.5;
		cube.add( arrowHelperReverse );
		vectorArrowsReverse.push(arrowHelperReverse)
	}

	renderer.setAnimationLoop( animate );
}

main();



joypad.set({
	axisMovementThreshold: 0.0,
});
joypad.on('button_press', (e) => {
	eel.set_network("Controller/Button"+e.detail.index, true);
});
joypad.on('button_release', (e) => {
	eel.set_network("Controller/Button"+e.detail.index, false);
});
joypad.on('axis_move', (e) => {
	let axes = e.detail.gamepad.axes;
	for (var i=0;i<axes.length;i++) {
		console.log(axes[i])
		if (axes[i] < 0.1 && axes[i] > -0.1)
			eel.set_network("Controller/Axis"+i, 0);
		else
			eel.set_network("Controller/Axis"+i, axes[i]);
	}
});


let nums = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'i', 'k', 'j', 'l'];

window.onkeydown = (e) => {
	let index = nums.indexOf(e.key);
	if (index > -1) eel.set_network("Controller/Button"+index, true);
	else {
		if (e.key == 'a') eel.set_network("Controller/Axis0", -1);
		else if (e.key == 'd') eel.set_network("Controller/Axis0", 1);
		else if (e.key == 'w') eel.set_network("Controller/Axis1", -1);
		else if (e.key == 's') eel.set_network("Controller/Axis1", 1);
		else if (e.key == 'ArrowLeft') eel.set_network("Controller/Axis2", -1);
		else if (e.key == 'ArrowRight') eel.set_network("Controller/Axis2", 1);
		else if (e.key == 'ArrowDown') eel.set_network("Controller/Axis3", 1);
		else if (e.key == 'ArrowUp') eel.set_network("Controller/Axis3", -1);
	}
}
window.onkeyup = (e) => {
	let index = nums.indexOf(e.key);
	if (index > -1) eel.set_network("Controller/Button"+index, false);
	else {
		if (e.key == 'a') eel.set_network("Controller/Axis0", 0);
		else if (e.key == 'd') eel.set_network("Controller/Axis0", 0);
		else if (e.key == 'w') eel.set_network("Controller/Axis1", 0);
		else if (e.key == 's') eel.set_network("Controller/Axis1", 0);
		else if (e.key == 'ArrowLeft') eel.set_network("Controller/Axis2", 0);
		else if (e.key == 'ArrowRight') eel.set_network("Controller/Axis2", 0);
		else if (e.key == 'ArrowDown') eel.set_network("Controller/Axis3", 0);
		else if (e.key == 'ArrowUp') eel.set_network("Controller/Axis3", 0);
	}
}
