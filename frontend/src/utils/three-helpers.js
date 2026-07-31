// Import the Three.js library used to create the 3D scene.
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

// ✅ FALLBACK DATA - Used when real data isn't available
const FALLBACK_DATA = {
  total_items: 24,
  markets: {
    "Retail Goods": {
      item_count: 12,
      avg_price: 473.99
    },
    "Digital Assets": {
      item_count: 12,
      avg_price: 5942.24
    }
  }
};

// Creates the entire Three.js scene and returns methods that allow Vue to update or destroy the chart.
export function createThreeChart(container, data) {
  // ✅ Use real data or fallback if empty/missing
  const chartData = data && data.total_items ? data : FALLBACK_DATA;
  
  console.log('📊 Rendering 3D chart with:', chartData);

  // Create a new 3D scene where all objects will be placed.
  const scene = new THREE.Scene();

  // Create a perspective camera so the chart appears in 3D.
  const camera = new THREE.PerspectiveCamera(
    60,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );

  // Position the camera so all bars are visible.
  camera.position.set(8, 10, 18);
  camera.lookAt(0, 4, 0);

  // Create the WebGL renderer that draws the scene.
  const renderer = new THREE.WebGLRenderer({
    antialias: true
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
  controls.target.set(0, 4, 0);
  
  // Add a directional light to illuminate the bars.
  const light = new THREE.DirectionalLight(0xffffff, 2);
  light.position.set(10, 20, 20);
  light.castShadow = true;
  scene.add(light);
  
  // Ambient light softens shadows and brightens the scene.
  scene.add(new THREE.AmbientLight(0xffffff, 1));

  // ✅ Add a second light from the front
  const frontLight = new THREE.DirectionalLight(0xffffff, 0.5);
  frontLight.position.set(0, 10, 10);
  scene.add(frontLight);

  // ✅ Floor with better shadow
  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(25, 25),
    new THREE.ShadowMaterial({
      opacity: 0.3,
      color: 0x000000
    })
  );
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.1;
  floor.receiveShadow = true;
  scene.add(floor);

  // ✅ Grid helper for reference (optional)
  const gridHelper = new THREE.GridHelper(20, 20, 0x888888, 0x444444);
  gridHelper.position.y = -0.05;
  scene.add(gridHelper);

  // Store references to all bars so they can be updated later.
  const bars = [];

  // ✅ Creates a single 3D bar with labels and adds it to the scene.
  function createBar(height, color, x, label, market) {
    // Define the size of the bar.
    const barHeight = Math.max(height * 1.5, 0.5); // Scale height for better visibility
    const geometry = new THREE.BoxGeometry(2, barHeight, 2);
    
    // Create the material that gives the bar its colour.
    const material = new THREE.MeshStandardMaterial({
      color: color,
      roughness: 0.3,
      metalness: 0.1,
      emissive: new THREE.Color(color).multiplyScalar(0.1)
    });

    // Combine the geometry and material into a 3D mesh.
    const cube = new THREE.Mesh(geometry, material);
    cube.castShadow = true;
    cube.receiveShadow = true;

    // Position the bar in the scene.
    cube.position.x = x;
    cube.position.y = barHeight / 2;
    
    // ✅ Store extra data on the mesh for updates
    cube.userData = { originalHeight: height, label, market };
    
    // Add the bar to the scene and save a reference to it.
    scene.add(cube);
    bars.push(cube);

    // ✅ Add a colored border/outline to the bar
    const edges = new THREE.EdgesGeometry(geometry);
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x000000, opacity: 0.2, transparent: true });
    const wireframe = new THREE.LineSegments(edges, lineMaterial);
    wireframe.position.copy(cube.position);
    scene.add(wireframe);
    bars.push(wireframe); // Store with bars for cleanup
  }

  // ✅ Create the Retail Goods bar
  createBar(
    chartData.markets["Retail Goods"]?.item_count || 0,
    0xFF9900, // Orange
    -4,
    "Retail Goods",
    "retail"
  );

  // ✅ Create the Digital Assets bar
  createBar(
    chartData.markets["Digital Assets"]?.item_count || 0,
    0x00AAFF, // Blue
    0,
    "Digital Assets",
    "crypto"
  );

  // ✅ Create the Total Items bar
  createBar(
    chartData.total_items || 0,
    0x00FF88, // Green
    4,
    "Total Items",
    "total"
  );

  // ✅ Continuously render the scene for smooth animations.
  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }

  // Start the animation loop.
  animate();

  // ✅ Handle window resize
  window.addEventListener("resize", () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });

  // ✅ Expose methods that Vue can call.
  return {
    updateBars(newData) {
      // Use new data or fallback
      const updateData = newData && newData.total_items ? newData : FALLBACK_DATA;
      
      console.log('🔄 Updating 3D chart with:', updateData);
      
      // Update the height of each bar when new statistics arrive.
      // Bars are stored in order: Retail, Digital, Total
      if (bars.length >= 6) {
        // Retail bar (index 0) and its wireframe (index 1)
        const retailHeight = Math.max((updateData.markets["Retail Goods"]?.item_count || 0) * 1.5, 0.5);
        bars[0].scale.y = retailHeight / (bars[0].userData.originalHeight * 1.5 || 1);
        bars[0].position.y = retailHeight / 2;
        bars[1].position.y = retailHeight / 2; // wireframe
        
        // Digital bar (index 2) and its wireframe (index 3)
        const digitalHeight = Math.max((updateData.markets["Digital Assets"]?.item_count || 0) * 1.5, 0.5);
        bars[2].scale.y = digitalHeight / (bars[2].userData.originalHeight * 1.5 || 1);
        bars[2].position.y = digitalHeight / 2;
        bars[3].position.y = digitalHeight / 2; // wireframe
        
        // Total bar (index 4) and its wireframe (index 5)
        const totalHeight = Math.max((updateData.total_items || 0) * 1.5, 0.5);
        bars[4].scale.y = totalHeight / (bars[4].userData.originalHeight * 1.5 || 1);
        bars[4].position.y = totalHeight / 2;
        bars[5].position.y = totalHeight / 2; // wireframe
      }
    },

    // Clean up the renderer when the component is destroyed.
    destroy() {
      // Dispose of geometries and materials
      bars.forEach(bar => {
        if (bar.geometry) bar.geometry.dispose();
        if (bar.material) bar.material.dispose();
      });
      
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    }
  };
}