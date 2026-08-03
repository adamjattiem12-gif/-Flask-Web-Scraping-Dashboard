<template>
  <div class="three-chart-wrapper">
    <div class="chart-heading">
      <h3>3D Market Summary</h3>
      <span>Hover a bar for details · drag to rotate</span>
    </div>
    <div ref="canvasContainer" class="chart"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useStatsStore } from '@/stores/statsStore'
import { useThemeStore } from '@/stores/themeStore'
import { createThreeChart } from '@/utils/three-helpers'

const canvasContainer = ref(null)
const statsStore = useStatsStore()
const themeStore = useThemeStore()
let chart

onMounted(async () => {
  // Render immediately with the helper's fallback data; network data can
  // arrive afterward without leaving a blank chart during the request.
  chart = createThreeChart(canvasContainer.value, statsStore.stats)
  try {
    await statsStore.fetchStats()
    chart?.updateBars(statsStore.stats)
  } catch (error) {
    console.warn('Chart stats unavailable; showing fallback data.', error)
  }
})

watch(() => statsStore.stats, (stats) => chart?.reset(stats), { deep: true })
watch(() => themeStore.theme, () => chart?.updateTheme())

const reset = () => chart?.reset(statsStore.stats)
defineExpose({ reset })

onUnmounted(() => chart?.destroy())
</script>

<style scoped>
.three-chart-wrapper {
  margin: 32px auto;
  padding: 20px 24px;
  max-width: 1100px;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-surface);
  box-shadow: 0 4px 12px var(--color-shadow);
}
.chart-heading { margin-bottom: 12px; }
.chart-heading h3 { margin: 0 0 4px; color: var(--color-text); font-size: 18px; }
.chart-heading span { color: var(--color-text-muted); font-size: 12px; }
.chart {
  width: 100%;
  height: 420px;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  background: var(--color-bg);
}
@media (max-width: 768px) { .three-chart-wrapper { padding: 16px; } .chart { height: 340px; } }
</style>
