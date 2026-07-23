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
                {{ item.change >= 0 ? '+' : '' }}{{ item.change }}%
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
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  padding: 20px 24px;
  border-bottom: 1px solid #E5E2DD;
}

.table-title {
  color: #2D2A3E;
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
  background: #F7F5F2;
}

th {
  text-align: left;
  padding: 12px 16px;
  color: #5C5A6B;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

td {
  padding: 14px 16px;
  border-bottom: 1px solid #F0EDEA;
  color: #2D2A3E;
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
  color: #9E9BB0;
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
  background: #E8F5E8;
  color: #5B8C5A;
}

.change-badge.negative {
  background: #FDE8E9;
  color: #C1666B;
}

.market-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.market-badge.digital {
  background: #E8F4F4;
  color: #4A8C8C;
}

.market-badge.retail {
  background: #F5EDE4;
  color: #D4914A;
}

.rating {
  color: #D4914A;
  font-weight: 600;
}

.no-rating {
  color: #C5C5D0;
}

.scraped-cell {
  color: #9E9BB0;
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