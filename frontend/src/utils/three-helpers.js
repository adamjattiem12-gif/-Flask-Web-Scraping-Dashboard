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

  // ✅ Position the camera so all bars are visible (moved back for better view)
  camera.position.set(10, 8, 18);
  camera.lookAt(0, 4, 0);

  // Create the WebGL renderer that draws the scene.
  const renderer = new THREE.WebGLRenderer({
    antialias: true
  });

  // ✅ Set background color to match dashboard
  renderer.setClearColor(0xF7F5F2);

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
  
  // ✅ Add a directional light to illuminate the bars (brighter)
  const light = new THREE.DirectionalLight(0xffffff, 2.5);
  light.position.set(10, 20, 20);
  light.castShadow = true;
  scene.add(light);
  
  // ✅ Ambient light softens shadows and brightens the scene (brighter)
  scene.add(new THREE.AmbientLight(0xffffff, 1.5));

  // ✅ Add a second light from the front
  const frontLight = new THREE.DirectionalLight(0xffffff, 0.5);
  frontLight.position.set(0, 10, 10);
  scene.add(frontLight);

  // ✅ Floor with better shadow
  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(25, 25),
    new THREE.ShadowMaterial({
      opacity: 0.25
    })
  );
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.1;
  floor.receiveShadow = true;
  scene.add(floor);

  // ✅ Grid helper for reference (optional)
  const gridHelper = new THREE.GridHelper(20, 20, 0x888888, 0xdddddd);
  gridHelper.position.y = -0.05;
  scene.add(gridHelper);

  // Store references to all bars so they can be updated later.
  const bars = [];

  // Creates a single 3D bar and adds it to the scene.
  function createBar(height, color, x, info) {
    // Define the size of the bar.
    const barHeight = Math.max(height, 0.5);
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
    cube.userData = info;
    cube.castShadow = true;
    cube.receiveShadow = true;

    // Position the bar in the scene.
    cube.position.x = x;
    cube.position.y = barHeight / 2;
    
    // Add the bar to the scene and save a reference to it.
    scene.add(cube);
    bars.push(cube);

    // ✅ Add a colored border/outline to the bar
    const edges = new THREE.EdgesGeometry(geometry);
    const lineMaterial = new THREE.LineBasicMaterial({ 
      color: 0x000000, 
      opacity: 0.15, 
      transparent: true 
    });
    const wireframe = new THREE.LineSegments(edges, lineMaterial);
    wireframe.position.copy(cube.position);
    scene.add(wireframe);
    bars.push(wireframe);
  }

  // ✅ Create the Retail Goods bar
  createBar(
    chartData.markets["Retail Goods"]?.item_count || 0,
    0xff9900,
    -8,
    {
      name: "Retail Goods",
      items: chartData.markets["Retail Goods"]?.item_count || 0,
      price: chartData.markets["Retail Goods"]?.avg_price || 0
    }
  );

  // ✅ Create the Digital Assets bar
  createBar(
    chartData.markets["Digital Assets"]?.item_count || 0,
    0x00aaff,
    0,
    {
      name: "Digital Assets",
      items: chartData.markets["Digital Assets"]?.item_count || 0,
      price: chartData.markets["Digital Assets"]?.avg_price || 0
    }
  );

  // ✅ Create the Total Items bar
  createBar(
    chartData.total_items || 0,
    0x00ff88,
    8,
    {
      name: "Total Items",
      items: chartData.total_items || 0,
      price: null
    }
  );

  // ✅ Create a floating tooltip for bar information.
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

  container.style.position = "relative";
  container.appendChild(tooltip);

  // ✅ Create the raycaster used to detect mouse interaction.
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  renderer.domElement.addEventListener("mousemove", (event) => {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);

    const intersects = raycaster.intersectObjects(bars);

    if (intersects.length > 0) {
      const hoveredBar = intersects[0].object;
      const info = hoveredBar.userData;

      tooltip.style.display = "block";
      tooltip.style.left = (event.clientX - rect.left + 15) + "px";
      tooltip.style.top = (event.clientY - rect.top + 15) + "px";

      tooltip.innerHTML = `
        <strong style="font-size:15px;">${info.name}</strong><br>
        <span style="color:#ccc;">Items:</span> ${info.items}<br>
        ${info.price ? `<span style="color:#ccc;">Average Price:</span> R${info.price.toFixed(2)}` : ''}
      `;
    } else {
      tooltip.style.display = "none";
    }
  });

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
      // Bars are stored in order: Retail, wireframe, Digital, wireframe, Total, wireframe
      if (bars.length >= 6) {
        // Retail bar (index 0) 
        const retailItems = updateData.markets["Retail Goods"]?.item_count || 0;
        bars[0].scale.y = Math.max(retailItems, 0.5);
        bars[0].position.y = Math.max(retailItems, 0.5) / 2;
        // Update userData
        bars[0].userData.items = retailItems;
        bars[0].userData.price = updateData.markets["Retail Goods"]?.avg_price || 0;
        
        // Digital bar (index 2)
        const digitalItems = updateData.markets["Digital Assets"]?.item_count || 0;
        bars[2].scale.y = Math.max(digitalItems, 0.5);
        bars[2].position.y = Math.max(digitalItems, 0.5) / 2;
        bars[2].userData.items = digitalItems;
        bars[2].userData.price = updateData.markets["Digital Assets"]?.avg_price || 0;
        
        // Total bar (index 4)
        const totalItems = updateData.total_items || 0;
        bars[4].scale.y = Math.max(totalItems, 0.5);
        bars[4].position.y = Math.max(totalItems, 0.5) / 2;
        bars[4].userData.items = totalItems;
        bars[4].userData.price = null;
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
      if (container.contains(tooltip)) {
        container.removeChild(tooltip);
      }
    }
  };
}