import * as THREE from "three";
export function createThreeChart(container, data){
const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
60,

container.clientWidth/container.clientHeight,
0.1,
1000
);

camera.position.set(0,8,18);

const renderer = new THREE.WebGLRenderer({
antialias:true
});

renderer.setSize(
container.clientWidth,
container.clientHeight
);

container.appendChild(renderer.domElement);
const light = new THREE.DirectionalLight(0xffffff,2);

light.position.set(10,20,20);
scene.add(light);
scene.add(new THREE.AmbientLight(0xffffff,1));
const bars=[];

function createBar(height,color,x){
const geometry=new THREE.BoxGeometry(2,height,2);
const material=new THREE.MeshStandardMaterial({
color
});

const cube=new THREE.Mesh(
geometry,
material
);

cube.position.x=x;
cube.position.y=height/2;
scene.add(cube);
bars.push(cube);
}

createBar(
data.markets["Retail Goods"].item_count,
0xff9900,
-4
);

createBar(
data.markets["Digital Assets"].item_count,
0x00aaff,
0
);

createBar(
data.total_items,
0x00ff88,
4
);

function animate(){
requestAnimationFrame(animate);
renderer.render(scene,camera);
}

animate();

return{
updateBars(newData){

bars[0].scale.y=
newData.markets["Retail Goods"].item_count;

bars[1].scale.y=
newData.markets["Digital Assets"].item_count;

bars[2].scale.y=
newData.total_items;
},

destroy(){
renderer.dispose();
container.removeChild(renderer.domElement);
}
};
}