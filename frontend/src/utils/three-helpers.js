// ============================================================
// FILE: frontend/src/utils/three-helpers.js
// ============================================================
// No fallback data — shows 0 bars when no data exists
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
const THEME_COLORS = {
light: { bg: 0xf7f5f2, gridMain: 0x888888, gridSub: 0xdddddd },
dark: { bg: 0x15131f, gridMain: 0x6f6d85, gridSub: 0x35334a },
};
function getCurrentTheme() {
return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
}
export function createThreeChart(container, data) {
// No fallback — use real data or empty
const chartData = data && data.total_items ? data : {
total_items: 0,
markets: {
"Retail Goods": { item_count: 0, avg_price: 0 },
"Digital Assets": { item_count: 0, avg_price: 0 }
}
};
console.log(' Rendering 3D chart with:', chartData);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
60,
container.clientWidth / container.clientHeight,
0.1,
1000
);
camera.position.set(12, 8, 21);
camera.lookAt(0, 4, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
let currentTheme = getCurrentTheme();
renderer.setClearColor(THEME_COLORS[currentTheme].bg);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enablePan = true;
controls.minDistance = 8;
controls.maxDistance = 42;
controls.maxPolarAngle = Math.PI / 2.2;
controls.minPolarAngle = Math.PI / 6;
controls.target.set(0, 4, 0);
controls.autoRotate = false;
const light = new THREE.DirectionalLight(0xffffff,2.5);
light.position.set(10, 20, 20);
light.castShadow = true;
scene.add(light);
scene.add(new THREE.AmbientLight(0xffffff, 1.5));
const frontLight = new THREE.DirectionalLight(0xffffff,0.5);
frontLight.position.set(0, 10, 10);
scene.add(frontLight);
const floor = new THREE.Mesh(
new THREE.PlaneGeometry(25, 25),
new THREE.ShadowMaterial({ opacity: 0.25 })
);
floor.rotation.x= -Math.PI / 2;
floor.position.y= -0.1;
floor.receiveShadow= true;
scene.add(floor);
let gridHelper = new THREE.GridHelper(20, 20, THEME_COLORS[currentTheme].gridMain,
THEME_COLORS[currentTheme].gridSub);
gridHelper.position.y= -0.05;
scene.add(gridHelper);
const bars = [];
const barSets = {};
function createBar(key, height, color, x, info) {
const barHeight = Math.max(height, 0.5);
const geometry = new THREE.BoxGeometry(2, barHeight, 2);
const material = new THREE.MeshStandardMaterial({
color: color,
roughness: 0.3,
metalness: 0.1,
emissive: new THREE.Color(color).multiplyScalar(0.1)
});
const cube = new THREE.Mesh(geometry, material);
cube.userData = info;
cube.userData.baseHeight = barHeight;
cube.userData.targetHeight = barHeight;
cube.userData.baseColor = new THREE.Color(color);
cube.userData.highlightColor = new THREE.Color(0xffffff);
cube.userData.colorPulse = 0;
cube.castShadow = true;
cube.receiveShadow = true;
cube.scale.y = 0;
cube.position.x = x;
cube.position.y = barHeight / 2;
scene.add(cube);
bars.push(cube);
const edges = new THREE.EdgesGeometry(geometry);
const lineMaterial = new THREE.LineBasicMaterial({
color: 0x000000,
opacity: 0.15,
transparent: true
});
const wireframe = new THREE.LineSegments(edges, lineMaterial);
wireframe.userData = cube.userData;
wireframe.position.copy(cube.position);
wireframe.scale.y = 0;
scene.add(wireframe);
bars.push(wireframe);
barSets[key] = { bar: cube, outline: wireframe };
}
createBar('retail',
chartData.markets["Retail Goods"]?.item_count || 0,
0xff9900,
-7,
{
name: "Retail Goods",
items: chartData.markets["Retail Goods"]?.item_count || 0,
price: chartData.markets["Retail Goods"]?.avg_price || 0
}
);
createBar('digital',
chartData.markets["Digital Assets"]?.item_count || 0,
0x00aaff,
0,
{
name: "Digital Assets",
items: chartData.markets["Digital Assets"]?.item_count || 0,
price: chartData.markets["Digital Assets"]?.avg_price || 0
}
);
createBar('total',
chartData.total_items || 0,
0x00ff88,
7,
{
name: "Total Items",
items: chartData.total_items || 0,
price: null
}
);
const tooltip = document.createElement("div");
tooltip.style.position = "absolute";
tooltip.style.padding = "10px 14px";
tooltip.style.background = "rgba(0,0,0,0.85)";
tooltip.style.color = "white";
tooltip.style.borderRadius = "8px";
tooltip.style.fontSize = "13px";
tooltip.style.pointerEvents = "none";
tooltip.style.display = "none";
tooltip.style.boxShadow = "0 4px 12px rgba(0,0,0,0.3)";
tooltip.style.backdropFilter = "blur(4px)";
tooltip.style.border = "1px solid rgba(255,255,255,0.1)";
tooltip.style.zIndex = "10";
container.style.position= "relative";
container.appendChild(tooltip);
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
renderer.domElement.addEventListener("mousemove", (event) => {
const rect = renderer.domElement.getBoundingClientRect();
mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
raycaster.setFromCamera(mouse, camera);
const intersects = raycaster.intersectObjects(bars).filter(({object }) =>
object.userData?.name);
if (intersects.length > 0) {
const hoveredBar = intersects[0].object;
const info = hoveredBar.userData;
tooltip.style.display = "block";
const tooltipWidth = 220;
const tooltipHeight = 90;
const left = Math.min(event.clientX - rect.left + 15, rect.width - tooltipWidth - 8);
const top = Math.min(event.clientY - rect.top + 15, rect.height - tooltipHeight - 8);
tooltip.style.left = Math.max(8, left) + "px";
tooltip.style.top = Math.max(8, top) + "px";
tooltip.innerHTML = `
<strong style="font-size:15px;">${info.name}</strong><br>
<span style="color:#ccc;">Items:</span> ${info.items}<br>
${Number.isFinite(Number(info.price)) && Number(info.price) > 0 ? `<span
style="color:#ccc;">Average Price:</span>
$${Number(info.price).toLocaleString(undefined, {minimumFractionDigits: 2,
maximumFractionDigits: 2})}` : ''}
`;
} else {
tooltip.style.display = "none";
}
});
let animationFrameId = null;
function animate() {
animationFrameId = requestAnimationFrame(animate);
controls.update();
for (let i = 0; i < bars.length; i += 2) {
const bar = bars[i];
const outline = bars[i + 1];
const targetHeight = bar.userData.targetHeight;
const targetScale = targetHeight / bar.userData.baseHeight;
bar.scale.y += (targetScale - bar.scale.y) * 0.08;
bar.userData.colorPulse *= 0.94;
bar.material.color.lerpColors(
bar.userData.baseColor,
bar.userData.highlightColor,
bar.userData.colorPulse
);
outline.scale.y = bar.scale.y;
bar.position.y= (bar.userData.baseHeight * bar.scale.y) / 2;
outline.position.y = bar.position.y;
}
renderer.render(scene, camera);
}
animate();
const handleResize = () => {
camera.aspect = container.clientWidth / container.clientHeight;
camera.updateProjectionMatrix();
renderer.setSize(container.clientWidth, container.clientHeight);
};
window.addEventListener("resize", handleResize);
return {
updateTheme() {
currentTheme = getCurrentTheme();
const colors = THEME_COLORS[currentTheme];
renderer.setClearColor(colors.bg);
scene.remove(gridHelper);
gridHelper.geometry.dispose();
gridHelper.material.dispose();
gridHelper = new THREE.GridHelper(20, 20, colors.gridMain, colors.gridSub);
gridHelper.position.y= -0.05;
scene.add(gridHelper);
},
updateBars(newData) {
const updateData = newData && newData.total_items ? newData : {
total_items: 0,
markets: {
"Retail Goods": { item_count: 0, avg_price: 0 },
"Digital Assets": { item_count: 0, avg_price: 0 }
}
};
console.log(' Updating 3D chart with:', updateData);
if (barSets.retail && barSets.digital && barSets.total) {
const retailItems = updateData.markets["Retail Goods"]?.item_count || 0;
barSets.retail.bar.userData.targetHeight = Math.max(retailItems, 0.5);
barSets.retail.bar.userData.items = retailItems;
barSets.retail.bar.userData.price = updateData.markets["Retail Goods"]?.avg_price || 0;
const digitalItems = updateData.markets["Digital Assets"]?.item_count || 0;
barSets.digital.bar.userData.targetHeight = Math.max(digitalItems, 0.5);
barSets.digital.bar.userData.items = digitalItems;
barSets.digital.bar.userData.price = updateData.markets["Digital Assets"]?.avg_price || 0;
const totalItems = updateData.total_items || 0;
barSets.total.bar.userData.targetHeight = Math.max(totalItems, 0.5);
barSets.total.bar.userData.items = totalItems;
barSets.total.bar.userData.price = null;
}
},
reset(newData) {
bars.forEach((mesh) => {
if (mesh.userData?.name) mesh.scale.y = 0;
});
this.updateBars(newData);
},
destroy() {
if (animationFrameId !== null) {
cancelAnimationFrame(animationFrameId);
animationFrameId = null;
}
window.removeEventListener("resize", handleResize);
bars.forEach(bar => {
if (bar.geometry) bar.geometry.dispose();
if (bar.material) bar.material.dispose();
});
renderer.dispose();
if (container.contains(renderer.domElement)) {
container.removeChild(renderer.domElement);
}
if (container.contains(tooltip)){
container.removeChild(tooltip);
}
}
};
}
