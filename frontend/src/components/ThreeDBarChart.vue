<template>
  <div ref="canvasContainer" class="chart"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useStatsStore } from "@/stores/statsStore";
import { createThreeChart } from "@/utils/three-helpers";

const canvasContainer = ref(null);
const statsStore = useStatsStore();
let chart;

onMounted(async () => {
    await statsStore.fetchStatistics();
    chart = createThreeChart(
        canvasContainer.value,
        statsStore.statistics
    );
});

watch(
() => statsStore.statistics,

(newStats)=>{
    chart.updateBars(newStats);
},

{ deep:true }
);

onUnmounted(()=>{
    chart.destroy();
});
</script>

<style scoped>
    .chart{
    height:450px;
    width:100%;
    border-radius:12px;
    overflow:hidden;
    }
</style>