<template>
  <div class="three-chart-wrapper">
    <div class="chart-header">
      <div class="header-left">
        <h3>📊 Price Comparison by Market</h3>
        <span class="chart-subtitle">USD values grouped by Digital Assets and Retail Goods</span>
      </div>
      <div class="legend">
        <div class="legend-item">
          <span class="legend-color digital"></span>
          <span class="legend-label">Digital Assets</span>
        </div>
        <div class="legend-item">
          <span class="legend-color retail"></span>
          <span class="legend-label">Retail Goods</span>
        </div>
      </div>
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
let resizeObserver = null

// ✅ Get data from store
const chartData = computed(() => {
  const items = itemsStore.items ?? []
  
  // Filter and format items
  return items
    .filter(item => {
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
    .slice(0, 16) // Show top 16 items
})

// ✅ Group by market
const groupedData = computed(() => {
  const retail = chartData.value.filter(item => 
    item.market === 'Retail Goods' || item.market === 'Retail'
  )
  const digital = chartData.value.filter(item => 
    item.market === 'Digital Assets' || item.market === 'Digital'
  )
  return { retail, digital }
})

// ✅ Get max price for scaling
const maxPrice = computed(() => {
  const allPrices = chartData.value.map(d => d.price)
  if (allPrices.length === 0) return 100
  const max = Math.max(...allPrices)
  return max * 1.25 // 25% padding
})

// ✅ Colors
const COLORS = {
  digital: 0x4A8C8C,
  digitalLight: '#4A8C8C',
  retail: 0xD4914A,
  retailLight: '#D4914A',
  digitalBg: '#E8F4F4',
  retailBg: '#F5EDE4'
}

const getColorByMarket = (market) => {
  if (market === 'Digital Assets' || market === 'Digital') {
    return COLORS.digital
  }
  return COLORS.retail
}

const getColorLight = (market) => {
  if (market === 'Digital Assets' || market === 'Digital') {
    return COLORS.digitalLight
  }
  return COLORS.retailLight
}

// ✅ Init scene
const initScene = () => {
  if (!chartContainer.value) return

  const container = chartContainer.value
  const width = container.clientWidth || 900
  const height = 450

  // Scene
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xFBF9F7)

  // Camera
  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000)
  camera.position.set(10, 7, 12)
  camera.lookAt(0, 1.5, 0)

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  renderer.toneMapping = THREE.ACESFilmicToneMapping
  renderer.toneMappingExposure = 1.2
  container.appendChild(renderer.domElement)

  // Label Renderer
  labelRenderer = new CSS2DRenderer()
  labelRenderer.setSize(width, height)
  labelRenderer.domElement.style.position = 'absolute'
  labelRenderer.domElement.style.top = '0'
  labelRenderer.domElement.style.pointerEvents = 'none'
  container.appendChild(labelRenderer.domElement)

  // Controls
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.08
  controls.autoRotate = true
  controls.autoRotateSpeed = 0.8
  controls.maxPolarAngle = Math.PI / 2.3
  controls.minDistance = 5
  controls.maxDistance = 25
  controls.target.set(0, 1.5, 0)

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  scene.add(ambientLight)

  const mainLight = new THREE.DirectionalLight(0xffffff, 1.2)
  mainLight.position.set(8, 12, 10)
  mainLight.castShadow = true
  scene.add(mainLight)

  const fillLight = new THREE.DirectionalLight(0xffffff, 0.4)
  fillLight.position.set(-6, 4, 8)
  scene.add(fillLight)

  const rimLight = new THREE.DirectionalLight(0xffffff, 0.3)
  rimLight.position.set(0, -2, -10)
  scene.add(rimLight)

  // Ground
  const groundGeometry = new THREE.PlaneGeometry(30, 20)
  const groundMaterial = new THREE.MeshStandardMaterial({
    color: 0xF0EDEA,
    roughness: 0.8,
    metalness: 0.1,
    transparent: true,
    opacity: 0.6
  })
  const ground = new THREE.Mesh(groundGeometry, groundMaterial)
  ground.rotation.x = -Math.PI / 2
  ground.position.y = -0.05
  ground.receiveShadow = true
  scene.add(ground)

  // Grid
  const gridHelper = new THREE.GridHelper(22, 12, 0xDDD8D2, 0xDDD8D2)
  gridHelper.position.y = 0
  scene.add(gridHelper)

  // Resize observer
  resizeObserver = new ResizeObserver(() => {
    const newWidth = container.clientWidth || 900
    const newHeight = 450
    if (camera) {
      camera.aspect = newWidth / newHeight
      camera.updateProjectionMatrix()
    }
    renderer?.setSize(newWidth, newHeight)
    labelRenderer?.setSize(newWidth, newHeight)
  })
  resizeObserver.observe(container)

  return resizeObserver
}

// ✅ Create bars grouped by market
const createBars = () => {
  // Clear old bars
  bars.forEach(bar => {
    scene.remove(bar.group)
    bar.group.children.forEach(child => {
      if (child.geometry) child.geometry.dispose()
      if (child.material) child.material.dispose()
    })
  })
  bars = []

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

  const retailItems = groupedData.value.retail || []
  const digitalItems = groupedData.value.digital || []

  // Combine with market labels
  const allItems = [
    ...retailItems.map(item => ({ ...item, _marketGroup: 'Retail' })),
    ...digitalItems.map(item => ({ ...item, _marketGroup: 'Digital' }))
  ]

  if (allItems.length === 0) {
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

  const barWidth = 0.55
  const spacing = 1.1
  const totalWidth = allItems.length * spacing
  const startX = -totalWidth / 2 + spacing / 2
  const maxVal = maxPrice.value

  allItems.forEach((item, index) => {
    const x = startX + index * spacing
    const height = Math.max((item.price / maxVal) * 4.5, 0.08)
    const color = getColorByMarket(item._marketGroup)
    const colorHex = getColorLight(item._marketGroup)

    // Group
    const group = new THREE.Group()

    // Main bar with slight rounded edges (BoxGeometry with bevel-like effect)
    const geometry = new THREE.BoxGeometry(barWidth, height, barWidth)
    const material = new THREE.MeshStandardMaterial({
      color: color,
      roughness: 0.35,
      metalness: 0.05,
      transparent: true,
      opacity: 0.92,
      emissive: color,
      emissiveIntensity: 0.05
    })
    const bar = new THREE.Mesh(geometry, material)
    bar.castShadow = true
    bar.position.y = height / 2
    group.add(bar)

    // Top highlight
    const topGeo = new THREE.BoxGeometry(barWidth * 0.85, 0.04, barWidth * 0.85)
    const topMat = new THREE.MeshStandardMaterial({
      color: 0xFFFFFF,
      roughness: 0.2,
      metalness: 0.1,
      transparent: true,
      opacity: 0.25
    })
    const topHighlight = new THREE.Mesh(topGeo, topMat)
    topHighlight.position.y = height + 0.02
    group.add(topHighlight)

    // Price label
    const priceDiv = document.createElement('div')
    priceDiv.textContent = `$${item.price.toFixed(2)}`
    priceDiv.style.color = '#2D2A3E'
    priceDiv.style.fontSize = '11px'
    priceDiv.style.fontWeight = '700'
    priceDiv.style.fontFamily = 'Inter, sans-serif'
    priceDiv.style.background = 'rgba(255,255,255,0.92)'
    priceDiv.style.padding = '2px 10px'
    priceDiv.style.borderRadius = '6px'
    priceDiv.style.border = '1px solid #E5E2DD'
    priceDiv.style.boxShadow = '0 2px 6px rgba(0,0,0,0.06)'
    
    const priceLabel = new CSS2DObject(priceDiv)
    priceLabel.position.set(0, height + 0.45, 0)
    group.add(priceLabel)

    // Name label
    const nameDiv = document.createElement('div')
    const displayName = item.name.length > 16 ? item.name.substring(0, 14) + '…' : item.name
    nameDiv.textContent = displayName
    nameDiv.style.color = '#5C5A6B'
    nameDiv.style.fontSize = '9px'
    nameDiv.style.fontWeight = '500'
    nameDiv.style.fontFamily = 'Inter, sans-serif'
    nameDiv.style.textAlign = 'center'
    nameDiv.style.maxWidth = '70px'
    nameDiv.style.background = 'rgba(255,255,255,0.7)'
    nameDiv.style.padding = '2px 4px'
    nameDiv.style.borderRadius = '4px'
    nameDiv.style.wordWrap = 'break-word'
    nameDiv.style.lineHeight = '1.2'
    
    const nameLabel = new CSS2DObject(nameDiv)
    nameLabel.position.set(0, -0.3, 0)
    group.add(nameLabel)

    group.position.set(x, 0, 0)
    scene.add(group)

    bars.push({ group, data: item })
  })

  // ✅ Add market group labels
  const midRetail = retailItems.length > 0 ? (retailItems.length / 2) * spacing - spacing / 2 - totalWidth / 2 : 0
  const midDigital = digitalItems.length > 0 ? (digitalItems.length / 2) * spacing - spacing / 2 + (retailItems.length * spacing) - totalWidth / 2 : 0

  if (retailItems.length > 0) {
    const retailLabelDiv = document.createElement('div')
    retailLabelDiv.textContent = '🛒 Retail Goods'
    retailLabelDiv.style.color = '#D4914A'
    retailLabelDiv.style.fontSize = '13px'
    retailLabelDiv.style.fontWeight = '700'
    retailLabelDiv.style.fontFamily = 'Inter, sans-serif'
    retailLabelDiv.style.background = 'rgba(255,255,255,0.9)'
    retailLabelDiv.style.padding = '4px 14px'
    retailLabelDiv.style.borderRadius = '20px'
    retailLabelDiv.style.border = '1px solid #D4914A'
    retailLabelDiv.style.boxShadow = '0 2px 8px rgba(212, 145, 74, 0.15)'
    
    const retailLabel = new CSS2DObject(retailLabelDiv)
    retailLabel.position.set(midRetail, -0.9, 0)
    scene.add(retailLabel)
  }

  if (digitalItems.length > 0) {
    const digitalLabelDiv = document.createElement('div')
    digitalLabelDiv.textContent = '₿ Digital Assets'
    digitalLabelDiv.style.color = '#4A8C8C'
    digitalLabelDiv.style.fontSize = '13px'
    digitalLabelDiv.style.fontWeight = '700'
    digitalLabelDiv.style.fontFamily = 'Inter, sans-serif'
    digitalLabelDiv.style.background = 'rgba(255,255,255,0.9)'
    digitalLabelDiv.style.padding = '4px 14px'
    digitalLabelDiv.style.borderRadius = '20px'
    digitalLabelDiv.style.border = '1px solid #4A8C8C'
    digitalLabelDiv.style.boxShadow = '0 2px 8px rgba(74, 140, 140, 0.15)'
    
    const digitalLabel = new CSS2DObject(digitalLabelDiv)
    digitalLabel.position.set(midDigital, -0.9, 0)
    scene.add(digitalLabel)
  }
}

// ✅ Animation loop
const animate = () => {
  animationId = requestAnimationFrame(animate)
  controls.update()
  renderer.render(scene, camera)
  labelRenderer.render(scene, camera)
}

// ✅ Resize handler
const resizeRenderer = () => {
  if (!chartContainer.value) return
  const width = chartContainer.value.clientWidth || 900
  const height = 450
  if (camera) {
    camera.aspect = width / height
    camera.updateProjectionMatrix()
  }
  renderer?.setSize(width, height)
  labelRenderer?.setSize(width, height)
}

// ✅ Watch for data changes
watch([chartData, groupedData], () => {
  createBars()
}, { deep: true })

// ✅ Lifecycle
onMounted(() => {
  initScene()
  setTimeout(createBars, 100)
  animate()

  window.addEventListener('resize', resizeRenderer)

  // Stop auto-rotation on user interaction
  const container = chartContainer.value
  if (container) {
    container.addEventListener('pointerdown', () => {
      if (controls) controls.autoRotate = false
    })
    container.addEventListener('pointerup', () => {
      setTimeout(() => {
        if (controls) controls.autoRotate = true
      }, 3000)
    })
  }

  return () => {
    if (resizeObserver) resizeObserver.disconnect()
    window.removeEventListener('resize', resizeRenderer)
    if (animationId) cancelAnimationFrame(animationId)
    if (renderer) renderer.dispose()
    if (labelRenderer) {
      labelRenderer.domElement?.remove()
    }
    if (controls) controls.dispose()
  }
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  if (renderer) renderer.dispose()
  if (labelRenderer) {
    labelRenderer.domElement?.remove()
  }
  if (controls) controls.dispose()
})
</script>

<style scoped>
.three-chart-wrapper {
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  padding: 20px 24px 16px 24px;
  margin-bottom: 32px;
  min-height: 500px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 8px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.chart-header h3 {
  color: #2D2A3E;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.chart-subtitle {
  color: #9E9BB0;
  font-size: 12px;
  font-weight: 400;
}

.legend {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-color {
  width: 14px;
  height: 14px;
  border-radius: 4px;
}

.legend-color.digital {
  background: #4A8C8C;
}

.legend-color.retail {
  background: #D4914A;
}

.legend-label {
  font-size: 12px;
  color: #5C5A6B;
  font-weight: 500;
}

.chart-container {
  width: 100%;
  height: 440px;
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
    min-height: 380px;
  }
  .chart-container {
    height: 320px;
  }
  .chart-header h3 {
    font-size: 14px;
  }
  .chart-subtitle {
    font-size: 11px;
  }
  .legend-label {
    font-size: 11px;
  }
}

@media (max-width: 375px) {
  .three-chart-wrapper {
    padding: 12px;
    min-height: 320px;
  }
  .chart-container {
    height: 260px;
  }
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .legend {
    gap: 10px;
  }
}
</style>