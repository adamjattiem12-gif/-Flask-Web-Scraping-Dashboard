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
    await statsStore.fetchStats();

chart = createThreeChart(
    canvasContainer.value,
    statsStore.stats
);
});
    // Watcher
watch(

() => statsStore.stats,

(newStats)=>{

    if(chart){

        chart.updateBars(newStats);

    }

},

{deep:true}

);

onUnmounted(()=>{
    chart.destroy();
});
</script>

<style scoped>
    .chart {
    width: 70%;
    height: 420px;
    margin: 0 auto 30px auto;
    border-radius: 12px;
    overflow: hidden;
    background: #F7F5F2;
    border: 1px solid #E5E2DD;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
</style>