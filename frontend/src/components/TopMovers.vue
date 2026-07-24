<template>
    <template>
  <div class="top-movers">
    <h3 class="section-title">Top Movers</h3>
    <div class="movers-list">
      <div v-for="item in items" :key="item.rank" class="mover-item">
        <span class="mover-rank">#{{ item.rank }}</span>
        <span class="mover-name">{{ item.symbol || item.name }}</span>
        <span class="mover-price">${{ item.price.toFixed(2) }}</span>
        <span class="mover-change" :class="item.change >= 0 ? 'positive' : 'negative'">
          {{ item.change >= 0 ? '+' : '' }}{{ item.change }}%
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, required: true }
})
</script>

<style scoped>
.top-movers {
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  padding: 20px 24px;
}

.section-title {
  color: #2D2A3E;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.movers-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mover-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  background: #F7F5F2;
  font-size: 14px;
}

.mover-rank {
  color: #9E9BB0;
  font-weight: 600;
  width: 28px;
}

.mover-name {
  flex: 1;
  font-weight: 500;
  color: #2D2A3E;
}

.mover-price {
  color: #5C5A6B;
  font-weight: 500;
}

.mover-change {
  font-weight: 600;
  min-width: 60px;
  text-align: right;
}

.mover-change.positive {
  color: #5B8C5A;
}

.mover-change.negative {
  color: #C1666B;
}
</style>
</template>