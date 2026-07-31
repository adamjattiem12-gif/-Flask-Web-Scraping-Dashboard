<template>
  <div ref="canvasContainer" class="chart"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useStatsStore } from "@/stores/statsStore";
import { createThreeChart } from "@/utils/three-helpers";

const canvasContainer = ref(null);
const statsStore = useStatsStore();
let chart = null;

// ✅ Build chart data from stats store
const getChartData = () => {
  const stats = statsStore.stats || {};
  
  const chartData = {
    total_items: stats.total_items || 24,
    markets: {
      "Retail Goods": {
        item_count: stats.markets?.['Retail Goods']?.item_count || 12,
        avg_price: stats.markets?.['Retail Goods']?.avg_price || 473.99
      },
      "Digital Assets": {
        item_count: stats.markets?.['Digital Assets']?.item_count || 12,
        avg_price: stats.markets?.['Digital Assets']?.avg_price || 5942.24
      }
    }
  };
  
  console.log('📊 Chart data:', chartData);
  return chartData;
};

// ✅ Render the chart
const renderChart = () => {
  if (!canvasContainer.value) {
    console.warn('❌ Container not ready');
    return;
  }
  
  // Check if container has size
  const rect = canvasContainer.value.getBoundingClientRect();
  if (rect.width === 0 || rect.height === 0) {
    console.warn('⚠️ Container has zero size, retrying...');
    setTimeout(renderChart, 100);
    return;
  }
  
  const chartData = getChartData();
  
  if (chart) {
    console.log('🔄 Updating existing chart');
    chart.updateBars(chartData);
  } else {
    console.log('🆕 Creating new chart');
    chart = createThreeChart(canvasContainer.value, chartData);
  }
};

// ✅ Mount
onMounted(async () => {
  console.log('✅ ThreeDBarChart mounted');
  
  // Fetch stats (will use fallback if API fails)
  await statsStore.fetchStats();
  
  // Small delay to ensure container is rendered
  setTimeout(renderChart, 200);
});

// ✅ Watch stats changes
watch(
  () => statsStore.stats,
  (newStats) => {
    console.log('📊 Stats updated:', newStats);
    if (chart) {
      const chartData = getChartData();
      chart.updateBars(chartData);
    } else {
      renderChart();
    }
  },
  { deep: true }
);

// ✅ Cleanup
onUnmounted(() => {
  console.log('🗑️ Destroying chart');
  if (chart) {
    chart.destroy();
    chart = null;
  }
});
</script>

<style scoped>
.chart {
  width: 100%;
  height: 420px;
  margin-bottom: 30px;
  border-radius: 12px;
  overflow: hidden;
  background: #fafafa;
  border: 1px solid #E5E2DD;
}
</style>