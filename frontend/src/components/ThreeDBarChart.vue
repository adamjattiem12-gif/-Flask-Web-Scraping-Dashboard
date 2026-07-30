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
    width: 100%;
    height: 420px;
    margin-bottom: 30px;
    border-radius: 12px;
    overflow: hidden;
    background: #ffffff;
}
</style>