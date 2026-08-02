<template>
  <div class="table-container">
    <div class="table-header">
      <h3 class="table-title">Recent Items</h3>
    </div>
    
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Change</th>
            <th>Market</th>
            <th>Rating</th>
            <th>Scraped</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>
              <div class="item-name">
                <span class="name-main">{{ item.name }}</span>
                <span class="name-source">{{ item.source }}</span>
              </div>
            </td>
            <td class="price-cell">${{ item.price.toFixed(2) }}</td>
            <td>
              <span class="change-badge" :class="item.change >= 0 ? 'positive' : 'negative'">
                {{ item.change >= 0 ? '+' : '' }}{{ Number(item.change ?? 0).toFixed(2) }}%
              </span>
            </td>
            <td>
              <span class="market-badge" :class="item.market.toLowerCase()">
                {{ item.market }}
              </span>
            </td>
            <td>
              <span v-if="item.rating" class="rating">
                ★ {{ item.rating }}
              </span>
              <span v-else class="no-rating">—</span>
            </td>
            <td class="scraped-cell">{{ item.scrapedAt }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, required: true }
})
</script>

<style scoped>
.table-container {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
}

.table-title {
  color: var(--color-text);
  font-size: 18px;
  font-weight: 600;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

thead {
  background: var(--color-bg);
}

th {
  text-align: left;
  padding: 12px 16px;
  color: var(--color-text-secondary);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-border-subtle);
  color: var(--color-text);
}

tr:last-child td {
  border-bottom: none;
}

.item-name {
  display: flex;
  flex-direction: column;
}

.name-main {
  font-weight: 500;
}

.name-source {
  color: var(--color-text-muted);
  font-size: 12px;
}

.price-cell {
  font-weight: 600;
}

.change-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
}

.change-badge.positive {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.change-badge.negative {
  background: var(--color-danger-bg);
  color: var(--color-danger);
}

.market-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.market-badge.digital {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.market-badge.retail {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.rating {
  color: var(--color-warning);
  font-weight: 600;
}

.no-rating {
  color: var(--color-text-muted);
}

.scraped-cell {
  color: var(--color-text-muted);
  font-size: 13px;
}

@media (max-width: 768px) {
  .table-header {
    padding: 16px;
  }
  td, th {
    padding: 10px 12px;
    font-size: 13px;
  }
}
</style>
