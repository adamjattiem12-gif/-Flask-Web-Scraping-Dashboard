<template>
  <div class="chart-wrapper">
    <span v-if="isDemoData" class="demo-badge" title="No live statistics yet — showing placeholder data">
      🧪 Demo data
    </span>
    <div ref="canvasContainer" class="chart"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useStatsStore } from "@/stores/statsStore";
import { useItemsStore } from "@/stores/itemsStore";
import { useThemeStore } from "@/stores/themeStore";
import { createThreeChart } from "@/utils/three-helpers";

const canvasContainer = ref(null);
const statsStore = useStatsStore();
const itemsStore = useItemsStore();
const themeStore = useThemeStore();
let chart = null;

// True whenever we don't have real backend stats yet, so the fallback
// numbers baked into three-helpers.js are being shown instead. Surfaced
// as a visible badge so nobody mistakes placeholder bars for live data
// during a demo.
const isDemoData = computed(() => {
  const stats = statsStore.stats || {};
  return !stats.total_items;
});

// ✅ Build chart data from stats store with fallback
const getChartData = () => {
  const stats = statsStore.stats || {};
  
  const chartData = {
    total_items: stats.total_items || itemsStore.items?.length || 24,
    markets: {
      "Retail Goods": {
        item_count: stats.markets?.['Retail Goods']?.item_count || itemsStore.getRetailItems?.length || 12,
        avg_price: stats.markets?.['Retail Goods']?.avg_price || 473.99
      },
      "Digital Assets": {
        item_count: stats.markets?.['Digital Assets']?.item_count || itemsStore.getCryptoItems?.length || 12,
        avg_price: stats.markets?.['Digital Assets']?.avg_price || 5942.24
      }
    }
  };
  
  console.log('📊 Chart data:', chartData);
  return chartData;

};

// ✅ Render the chart with container checks
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

// ✅ Watch items changes
watch(
  () => itemsStore.items,
  () => {
    console.log('📊 Items updated, refreshing chart');
    renderChart();
  },
  { deep: true }
);

// ✅ Watch theme changes - CSS variables don't reach the WebGL canvas, so
// the chart needs to be told explicitly to re-color itself.
watch(
  () => themeStore.theme,
  () => {
    if (chart) {
      chart.updateTheme();
    }
  }
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
.chart-wrapper {
  position: relative;
}

.demo-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 5;
  background: rgba(45, 42, 62, 0.85);
  color: var(--color-warning-strong);
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 12px;
  pointer-events: none;
}

.chart {
  width: 100%;
  height: 360px;
  margin: 0;
  border-radius: 12px;
  overflow: hidden;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 12px var(--color-shadow);
}

/* ✅ Responsive - full width on smaller screens */
@media (max-width: 992px) {
  .chart {
    width: 85%;
  }
}

@media (max-width: 768px) {
  .chart {
    width: 95%;
    height: 350px;
  }
}

@media (max-width: 480px) {
  .chart {
    width: 100%;
    height: 300px;
    margin: 0 0 20px 0;
    border-radius: 8px;
  }
}
</style>
