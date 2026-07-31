// Import the Three.js library used to create the 3D scene.
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
// Creates the entire Three.js scene and returns methods that allow Vue to update or destroy the chart.
export function createThreeChart(container, data){
// Create a new 3D scene where all objects will be placed.
const scene = new THREE.Scene();

// Create a perspective camera so the chart appears in 3D.
const camera = new THREE.PerspectiveCamera(
60,

container.clientWidth/container.clientHeight,
0.1,
1000
);

// Position the camera so all bars are visible.
camera.position.set(8,10,18);

camera.lookAt(0,4,0);

// Create the WebGL renderer that draws the scene.
const renderer = new THREE.WebGLRenderer({
antialias:true
});
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Match the renderer size to the Vue component.
renderer.setSize(
container.clientWidth,
container.clientHeight
);

// Attach the Three.js canvas to the HTML container.
container.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);

controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enablePan = true;
// Add a directional light to illuminate the bars.
const light = new THREE.DirectionalLight(0xffffff,2);

light.position.set(10,20,20);
light.castShadow = true;
scene.add(light);
// Ambient light softens shadows and brightens the scene.
scene.add(new THREE.AmbientLight(0xffffff,1));

const floor = new THREE.Mesh(

new THREE.PlaneGeometry(25,25),

new THREE.ShadowMaterial({

opacity:0.25

})

);

floor.rotation.x = -Math.PI/2;

floor.receiveShadow = true;

scene.add(floor);

// Store references to all bars so they can be updated later.
const bars=[];

// Creates a single 3D bar and adds it to the scene.
function createBar(height,color,x,info){
    // Define the size of the bar.
const geometry=new THREE.BoxGeometry(2,height,2);
// Create the material that gives the bar its colour.
const material=new THREE.MeshStandardMaterial({
color
});

// Combine the geometry and material into a 3D mesh.
const cube=new THREE.Mesh(
geometry,
material
);

cube.userData = info;

cube.castShadow = true;
cube.receiveShadow = true;

// Position the bar in the scene.
cube.position.x=x;
cube.position.y=height/2;
// Add the bar to the scene and save a reference to it.
scene.add(cube);
bars.push(cube);
}

//Create the retail goods bar
createBar(
data.markets["Retail Goods"].item_count,
0xff9900,
-4,
{
name:"Retail Goods",
items:data.markets["Retail Goods"].item_count,
price:data.markets["Retail Goods"].avg_price
}
);

// Create the Digital Assets bar.
createBar(
data.markets["Digital Assets"].item_count,
0x00aaff,
0,
{
name:"Digital Assets",
items:data.markets["Digital Assets"].item_count,
price:data.markets["Digital Assets"].avg_price
}
);

// Create the Total Items bar.
createBar(
data.total_items,
0x00ff88,
4,
{
name:"Total Items",
items:data.total_items,
price:null
}
);

// Continuously render the scene for smooth animations.
function animate(){
    // Request the next animation frame.
requestAnimationFrame(animate);
controls.update();
// Draw the latest frame to the screen.
renderer.render(scene,camera);
}

// Start the animation loop.
animate();

window.addEventListener("resize",()=>{

camera.aspect=

container.clientWidth/

container.clientHeight;

camera.updateProjectionMatrix();

renderer.setSize(

container.clientWidth,

container.clientHeight

);

});

// Expose methods that Vue can call.
return{

updateBars(newData){
// Update the height of each bar when new statistics arrive.
bars[0].scale.y=
newData.markets["Retail Goods"].item_count;

bars[1].scale.y=
newData.markets["Digital Assets"].item_count;

bars[2].scale.y=
newData.total_items;
},

// Clean up the renderer when the component is destroyed.
destroy(){
renderer.dispose();
container.removeChild(renderer.domElement);
}
};
}