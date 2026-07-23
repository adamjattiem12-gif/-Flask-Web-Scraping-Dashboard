<template>
  <div class="dashboard-page">
    <!-- WHITE BACKGROUND CONTAINER - CONNECTS TO SIDEBAR -->
    <div class="dashboard-content">
      <!-- HEADER -->
      <div class="dashboard-header">
        <h1>Dashboard</h1>
      </div>

      <!-- STAT CARDS -->
      <div class="stats-grid">
        <StatCard
          icon="📦"
          label="Total Items"
          :value="stats.totalItems"
          subtitle="across 2 markets"
        />
        <StatCard
          icon="🌐"
          label="Active Sources"
          :value="stats.activeSources"
          subtitle="WebScraper.io · CoinGecko"
        />
        <StatCard
          icon="✅"
          label="Success Rate"
          :value="stats.successRate"
          subtitle="last 7 days"
        />
        <StatCard
          icon="🕐"
          label="Last Scrape"
          :value="stats.lastScrape"
          subtitle="Jul 20, 2026"
        />
      </div>

      <!-- PRICE SNAPSHOT SECTION -->
      <div class="section-header">
        <h2>Price Snapshot</h2>
        <span class="section-subtitle">Market Overview · Updated from your latest scrape</span>
      </div>

      <!-- MARKET OVERVIEW -->
      <div class="markets-grid">
        <MarketOverviewCard
          title="Retail Goods"
          accent-color="#D4914A"
          :avg-price="473.99"
          :items-count="12"
          :recent-items="retailRecentItems"
        />
        <MarketOverviewCard
          title="Digital Assets"
          accent-color="#4A8C8C"
          :avg-price="5942.24"
          :items-count="12"
          :recent-items="cryptoRecentItems"
        />
      </div>

      <!-- TOP MOVERS & WATCHLIST ROW -->
      <div class="row-2col">
        <div class="placeholder-card">
          <h3>Top Movers</h3>
          <p style="color: #9E9BB0; font-size: 14px;">Waiting for Rushin's component</p>
        </div>
        <div class="placeholder-card">
          <h3>Watchlist</h3>
          <p style="color: #9E9BB0; font-size: 14px;">Waiting for Chad's component</p>
        </div>
      </div>

      <!-- SCRAPE BUTTON -->
      <div class="action-bar">
        <div class="source-badge">
          <span class="badge-dot"></span>
          WebScraper.io · CoinGecko
        </div>
        <button class="scrape-btn">⚡ Scrape Now</button>
      </div>

      <!-- RECENT ITEMS TABLE -->
      <div class="placeholder-table">
        <h3>Recent Items</h3>
        <p style="color: #9E9BB0; font-size: 14px;">Waiting for Rushin's DataTable component</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StatCard from '@/components/StatCard.vue'
import MarketOverviewCard from '@/components/MarketOverviewCard.vue'

// Mock Data
const stats = ref({
  totalItems: 24,
  activeSources: 2,
  successRate: '96.5%',
  lastScrape: '02:33 PM'
})

const retailRecentItems = [
  { name: 'HP Pavilion 15.6" FHD Laptop', change: -5.1 },
  { name: 'Bose QuietComfort 45 Wireless', change: -4.2 },
  { name: 'Asus VivoBook X441NA-GA190', change: -3.8 }
]

const cryptoRecentItems = [
  { name: 'SOL - Solana', change: 8.7 },
  { name: 'DOGE - Dogecoin', change: 7.2 },
  { name: 'AVAX - Avalanche', change: -6.3 }
]
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: #F7F5F2;
  padding: 0;
}

/* WHITE BACKGROUND CONTAINER - CONNECTS TO SIDEBAR */
.dashboard-content {
  background: #FFFFFF;
  min-height: 100vh;
  padding: 32px 40px 40px 40px;
  margin: 0;
  /* NO margin-left - connects directly to sidebar */
}

/* HEADER */
.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-header h1 {
  color: #2D2A3E;
  font-size: 28px;
  font-weight: 600;
}

/* SECTION HEADER */
.section-header {
  margin-bottom: 20px;
  margin-top: 8px;
}

.section-header h2 {
  color: #2D2A3E;
  font-size: 20px;
  font-weight: 600;
}

.section-subtitle {
  color: #9E9BB0;
  font-size: 14px;
  display: block;
  margin-top: 4px;
}

/* STAT CARDS */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

/* MARKET CARDS */
.markets-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

/* ROW 2 COL */
.row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

/* PLACEHOLDERS */
.placeholder-card {
  background: #F7F5F2;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  padding: 20px 24px;
  min-height: 200px;
}

.placeholder-card h3 {
  color: #2D2A3E;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

/* ACTION BAR */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  margin-bottom: 32px;
  border-top: 1px solid #E5E2DD;
  border-bottom: 1px solid #E5E2DD;
}

.source-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #5C5A6B;
  font-size: 14px;
  font-weight: 500;
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #5B8C5A;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.scrape-btn {
  padding: 12px 32px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  background: #5B8C5A;
  color: white;
  transition: all 0.2s;
}

.scrape-btn:hover {
  background: #4A7349;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(91, 140, 90, 0.3);
}

/* RECENT ITEMS TABLE */
.placeholder-table {
  background: #F7F5F2;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  padding: 20px 24px;
  min-height: 300px;
}

.placeholder-table h3 {
  color: #2D2A3E;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

/* RESPONSIVE */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 992px) {
  .markets-grid {
    grid-template-columns: 1fr;
  }
  .row-2col {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    padding: 20px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  
  .dashboard-header h1 {
    font-size: 24px;
  }
  
  .action-bar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .scrape-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 375px) {
  .dashboard-content {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header h1 {
    font-size: 20px;
  }
}
</style>
