<template>
  <div class="top-movers">
    <h3 class="section-title">Top Movers</h3>
    <div v-if="!items || items.length === 0" class="empty-state">
      <p>No movers to display</p>
    </div>
    <div v-else class="movers-list">
      <div v-for="item in items" :key="item.rank" class="mover-item">
        <span class="mover-rank">#{{ item.rank }}</span>
        <span class="mover-name">{{ item.symbol || item.name }}</span>
        <span class="mover-price">${{ item.price.toFixed(2) }}</span>
        <span class="mover-change" :class="item.change >= 0 ? 'positive' : 'negative'">
          {{ item.change >= 0 ? '+' : '' }}{{ Number(item.change ?? 0).toFixed(2) }}%
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    default: () => []
  }
})
</script>

<style scoped>
.top-movers {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 20px 24px;
}

.section-title {
  color: var(--color-text);
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
  background: var(--color-bg);
  font-size: 14px;
}

.mover-rank {
  color: var(--color-text-muted);
  font-weight: 600;
  width: 28px;
}

.mover-name {
  flex: 1;
  font-weight: 500;
  color: var(--color-text);
}

.mover-price {
  color: var(--color-text-secondary);
  font-weight: 500;
}

.mover-change {
  font-weight: 600;
  min-width: 60px;
  text-align: right;
}

.mover-change.positive {
  color: var(--color-success);
}

.mover-change.negative {
  color: var(--color-danger);
}

.empty-state {
  text-align: center;
  padding: 20px 0;
  color: var(--color-text-muted);
  font-size: 14px;
}
</style>
