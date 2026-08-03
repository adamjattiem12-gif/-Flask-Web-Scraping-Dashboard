<template>
  <div class="three-chart-wrapper">
    <div class="chart-header">
      <h3>📊 Price Comparison</h3>
      <span class="chart-subtitle">USD values across all items</span>
    </div>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { CSS2DRenderer, CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer.js'
import { useItemsStore } from '@/stores/itemsStore'

const itemsStore = useItemsStore()
const chartContainer = ref(null)
let scene, camera, renderer, labelRenderer, controls
let animationId = null
let bars = []

const chartData = computed(() => {
  const items = itemsStore.items ?? []
  
  // ✅ Take top items by price and ensure they have valid USD values
  return items
    .filter(item => {
      // Filter out items with invalid prices
      const price = typeof item.price === 'number' ? item.price : parseFloat(item.price)
      return !isNaN(price) && price > 0
    })
    .map(item => ({
      name: item.name,
      price: typeof item.price === 'number' ? item.price : parseFloat(item.price),
      market: item.market || 'Unknown',
      source: item.source || 'Unknown'
    }))
    .sort((a, b) => b.price - a.price)
    .slice(0, 12) // Show top 12 items
})

// ✅ Get the max price for scaling (with padding)
const maxPrice = computed(() => {
  if (chartData.value.length === 0) return 100
  const max = Math.max(...chartData.value.map(d => d.price))
  // Add 20% padding to the top
  return max * 1.2
})

// ✅ Colors for different markets
const getColorByMarket = (market) => {
  if (market === 'Digital Assets' || market === 'Digital') {
    return '#4A8C8C'  // Digital teal
  }
  return '#D4914A'    // Retail orange
}

const getColorHex = (market) => {
  if (market === 'Digital Assets' || market === 'Digital') {
    return 0x4A8C8C
  }
  return 0xD4914A
}

const initScene = () => {
  if (!chartContainer.value) return

  const container = chartContainer.value
  const width = container.clientWidth || 800
  const height = 400

  // ✅ Scene
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xF7F5F2)

  // ✅ Camera
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000)
  camera.position.set(8, 6, 10)
  camera.lookAt(0, 0, 0)

  // ✅ WebGL Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  container.appendChild(renderer.domElement)

  // ✅ CSS2D Renderer for labels
  labelRenderer = new CSS2DRenderer()
  labelRenderer.setSize(width, height)
  labelRenderer.domElement.style.position = 'absolute'
  labelRenderer.domElement.style.top = '0'
  labelRenderer.domElement.style.pointerEvents = 'none'
  container.appendChild(labelRenderer.domElement)

  // ✅ Controls
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.08
  controls.autoRotate = true
  controls.autoRotateSpeed = 1.0
  controls.maxPolarAngle = Math.PI / 2.2
  controls.target.set(0, 2, 0)

  // ✅ Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  scene.add(ambientLight)

  const dirLight = new THREE.DirectionalLight(0xffffff, 1)
  dirLight.position.set(5, 10, 7)
  dirLight.castShadow = true
  scene.add(dirLight)

  const fillLight = new THREE.DirectionalLight(0xffffff, 0.3)
  fillLight.position.set(-5, 2, 5)
  scene.add(fillLight)

  // ✅ Grid Helper
  const gridHelper = new THREE.GridHelper(20, 10, 0xCCCCCC, 0xCCCCCC)
  gridHelper.position.y = 0
  scene.add(gridHelper)

  // Resize handler
  const resizeObserver = new ResizeObserver(() => {
    const newWidth = container.clientWidth || 800
    const newHeight = 400
    if (camera) {
      camera.aspect = newWidth / newHeight
      camera.updateProjectionMatrix()
      renderer?.setSize(newWidth, newHeight)
      labelRenderer?.setSize(newWidth, newHeight)
    }
  })
  resizeObserver.observe(container)

  return resizeObserver
}

const createBars = () => {
  // Clear old bars
  bars.forEach(bar => {
    scene.remove(bar.group)
    // Dispose geometries and materials
    bar.group.children.forEach(child => {
      if (child.geometry) child.geometry.dispose()
      if (child.material) child.material.dispose()
    })
  })
  bars = []

  const data = chartData.value
  if (data.length === 0) {
    // Show empty state
    const emptyDiv = document.createElement('div')
    emptyDiv.textContent = 'No price data available'
    emptyDiv.style.color = '#9E9BB0'
    emptyDiv.style.fontSize = '16px'
    emptyDiv.style.fontWeight = '500'
    emptyDiv.style.padding = '20px'
    emptyDiv.style.textAlign = 'center'
    const emptyLabel = new CSS2DObject(emptyDiv)
    emptyLabel.position.set(0, 3, 0)
    scene.add(emptyLabel)
    return
  }

  const barWidth = 0.6
  const spacing = 1.2
  const totalWidth = data.length * spacing
  const startX = -totalWidth / 2 + spacing / 2
  const maxVal = maxPrice.value

  data.forEach((item, index) => {
    const x = startX + index * spacing
    const height = Math.max((item.price / maxVal) * 4, 0.05)
    const color = getColorHex(item.market)

    // ✅ Bar Group
    const group = new THREE.Group()

    // ✅ Bar (BoxGeometry with rounded edges via Cylinder)
    const geometry = new THREE.BoxGeometry(barWidth, height, barWidth)
    const material = new THREE.MeshStandardMaterial({
      color: color,
      roughness: 0.3,
      metalness: 0.1,
      transparent: true,
      opacity: 0.9
    })
    const bar = new THREE.Mesh(geometry, material)
    bar.castShadow = true
    bar.position.y = height / 2
    group.add(bar)

    // ✅ Price Label (on top of bar)
    const priceDiv = document.createElement('div')
    priceDiv.textContent = `$${item.price.toFixed(2)}`
    priceDiv.style.color = '#2D2A3E'
    priceDiv.style.fontSize = '12px'
    priceDiv.style.fontWeight = '700'
    priceDiv.style.fontFamily = 'Inter, sans-serif'
    priceDiv.style.background = 'rgba(255,255,255,0.9)'
    priceDiv.style.padding = '2px 8px'
    priceDiv.style.borderRadius = '4px'
    priceDiv.style.border = '1px solid #E5E2DD'
    priceDiv.style.boxShadow = '0 2px 4px rgba(0,0,0,0.08)'
    
    const priceLabel = new CSS2DObject(priceDiv)
    priceLabel.position.set(0, height + 0.3, 0)
    group.add(priceLabel)

    // ✅ Name Label (below bar)
    const nameDiv = document.createElement('div')
    // Truncate long names
    const displayName = item.name.length > 15 ? item.name.substring(0, 12) + '...' : item.name
    nameDiv.textContent = displayName
    nameDiv.style.color = '#5C5A6B'
    nameDiv.style.fontSize = '10px'
    nameDiv.style.fontWeight = '500'
    nameDiv.style.fontFamily = 'Inter, sans-serif'
    nameDiv.style.textAlign = 'center'
    nameDiv.style.maxWidth = '80px'
    nameDiv.style.background = 'rgba(255,255,255,0.7)'
    nameDiv.style.padding = '2px 4px'
    nameDiv.style.borderRadius = '4px'
    nameDiv.style.wordWrap = 'break-word'
    
    const nameLabel = new CSS2DObject(nameDiv)
    nameLabel.position.set(0, -0.3, 0)
    group.add(nameLabel)

    // ✅ Market badge (color indicator)
    const badgeDiv = document.createElement('div')
    badgeDiv.textContent = item.market === 'Digital Assets' ? '₿' : '🛒'
    badgeDiv.style.fontSize = '14px'
    badgeDiv.style.textAlign = 'center'
    badgeDiv.style.width = '24px'
    badgeDiv.style.height = '24px'
    badgeDiv.style.borderRadius = '50%'
    badgeDiv.style.background = item.market === 'Digital Assets' ? '#E8F4F4' : '#F5EDE4'
    badgeDiv.style.display = 'flex'
    badgeDiv.style.alignItems = 'center'
    badgeDiv.style.justifyContent = 'center'
    
    const badgeLabel = new CSS2DObject(badgeDiv)
    badgeLabel.position.set(0, -0.7, 0)
    group.add(badgeLabel)

    group.position.set(x, 0, 0)
    scene.add(group)

    bars.push({ group, data: item })
  })
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  controls.update()
  renderer.render(scene, camera)
  labelRenderer.render(scene, camera)
}

const resizeRenderer = () => {
  if (!chartContainer.value) return
  const width = chartContainer.value.clientWidth || 800
  const height = 400
  if (camera) {
    camera.aspect = width / height
    camera.updateProjectionMatrix()
  }
  renderer?.setSize(width, height)
  labelRenderer?.setSize(width, height)
}

// ✅ Watch for data changes and update chart
watch(chartData, () => {
  // Clear old labels
  const toRemove = []
  scene?.children.forEach(child => {
    if (child.isCSS2DObject) {
      toRemove.push(child)
    }
  })
  toRemove.forEach(child => {
    scene.remove(child)
    if (child.element && child.element.parentNode) {
      child.element.parentNode.removeChild(child.element)
    }
  })
  createBars()
}, { deep: true })

onMounted(() => {
  const resizeObserver = initScene()
  createBars()
  animate()

  // Handle window resize
  window.addEventListener('resize', resizeRenderer)

  // Cleanup
  return () => {
    if (resizeObserver) {
      resizeObserver.disconnect()
    }
    window.removeEventListener('resize', resizeRenderer)
    if (animationId) {
      cancelAnimationFrame(animationId)
    }
    if (renderer) {
      renderer.dispose()
    }
    if (labelRenderer) {
      labelRenderer.domElement.remove()
    }
    if (controls) {
      controls.dispose()
    }
  }
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (renderer) {
    renderer.dispose()
  }
  if (labelRenderer) {
    labelRenderer.domElement?.remove()
  }
  if (controls) {
    controls.dispose()
  }
})
</script>

<style scoped>
.three-chart-wrapper {
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 32px;
  min-height: 450px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}

.chart-header h3 {
  color: #2D2A3E;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.chart-subtitle {
  color: #9E9BB0;
  font-size: 13px;
  font-weight: 400;
}

.chart-container {
  width: 100%;
  height: 400px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
}

.chart-container :deep(.css2d-renderer) {
  pointer-events: none;
}

@media (max-width: 768px) {
  .three-chart-wrapper {
    padding: 16px;
    min-height: 350px;
  }
  .chart-container {
    height: 300px;
  }
  .chart-header h3 {
    font-size: 14px;
  }
  .chart-subtitle {
    font-size: 12px;
  }
}

@media (max-width: 375px) {
  .three-chart-wrapper {
    padding: 12px;
    min-height: 300px;
  }
  .chart-container {
    height: 250px;
  }
}
</style>