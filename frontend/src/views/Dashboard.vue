<template>
  <PageLayout title="Dashboard">
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

    <!-- MARKET OVERVIEW -->
    <div class="section-heading">
      <div>
        <p>PRICE SNAPSHOT</p>
        <h2>Market Overview</h2>
      </div>
      <span>Updated from your latest scrape</span>
    </div>
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
      <TopMovers :items="topMovers" />
      <Watchlist :items="watchlistItems" />
    </div>

    <!-- SCRAPE BUTTON -->
    <div class="action-bar">
      <div class="source-badge">
        <span class="badge-dot"></span>
        WebScraper.io · CoinGecko
      </div>
      <ScrapeButton @scrape="handleScrape" />
    </div>

    <!-- RECENT ITEMS TABLE -->
    <RecentItemsTable :items="recentItems" />
  </PageLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import PageLayout from '@/components/PageLayout.vue'
import StatCard from '@/components/StatCard.vue'
import MarketOverviewCard from '@/components/MarketOverviewCard.vue'
import TopMovers from '@/components/TopMovers.vue'
import Watchlist from '@/components/Watchlist.vue'
import ScrapeButton from '@/components/ScrapeButton.vue'
import RecentItemsTable from '@/components/RecentItemsTable.vue'

// Mock Data - Replace with API calls
const stats = ref({
  totalItems: 24,
  activeSources: 2,
  successRate: '96.5%',
  lastScrape: '02:33 PM'
})

const recentItems = ref([
  {
    id: 1,
    name: 'BTC - Bitcoin',
    source: 'CoinGecko',
    price: 67234.50,
    change: 3.2,
    market: 'Digital',
    rating: null,
    scrapedAt: 'Jul 20, 02:30 PM'
  },
  {
    id: 2,
    name: 'ETH - Ethereum',
    source: 'CoinGecko',
    price: 3412.80,
    change: 2.4,
    market: 'Digital',
    rating: null,
    scrapedAt: 'Jul 20, 02:30 PM'
  },
  {
    id: 3,
    name: 'Samsung 65" Crystal 4K UHD TV',
    source: 'WebScraper.io',
    price: 897.99,
    change: 0.8,
    market: 'Retail',
    rating: 4.5,
    scrapedAt: 'Jul 20, 02:31 PM'
  },
  {
    id: 4,
    name: 'Samsung Galaxy Tab S8+',
    source: 'WebScraper.io',
    price: 699.99,
    change: 1.5,
    market: 'Retail',
    rating: 4.3,
    scrapedAt: 'Jul 20, 02:33 PM'
  },
  {
    id: 5,
    name: 'Canon EOS Rebel SL3 DSLR',
    source: 'WebScraper.io',
    price: 649.00,
    change: -0.5,
    market: 'Retail',
    rating: 4.7,
    scrapedAt: 'Jul 20, 02:32 PM'
  },
  {
    id: 6,
    name: 'iPad Air 10.9-inch (2022)',
    source: 'WebScraper.io',
    price: 599.00,
    change: 2.1,
    market: 'Retail',
    rating: 4.6,
    scrapedAt: 'Jul 20, 02:31 PM'
  }
])

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

const topMovers = ref([
  { rank: 1, symbol: 'SOL', change: 8.7, price: 178.45, market: 'Digital' },
  { rank: 2, symbol: 'DOGE', change: 7.2, price: 0.1600, market: 'Digital' },
  { rank: 3, symbol: 'AVAX', change: -6.3, price: 38.91, market: 'Digital' },
  { rank: 4, symbol: 'LINK', change: 5.6, price: 18.47, market: 'Digital' },
  { rank: 5, name: 'HP Pavilion 15.6" FHD Laptop', change: -5.1, price: 529.99, market: 'Retail' }
])

const watchlistItems = ref([
  { name: 'SOL', change: 8.7, price: 178.45 },
  { name: 'DOGE', change: 7.2, price: 0.1600 },
  { name: 'AVAX', change: -6.3, price: 38.91 },
  { name: 'LINK', change: 5.6, price: 18.47 },
  { name: 'HP Pavilion 15.6" FHD Laptop', change: -5.1, price: 529.99 }
])

const handleScrape = () => {
  console.log('Scraping started...')
  // Trigger scrape API call
}
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.markets-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
  margin: 0 0 14px;
}

.section-heading p {
  margin: 0 0 4px;
  color: #9E9BB0;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .08em;
}

.section-heading h2 {
  margin: 0;
  color: #2D2A3E;
  font-size: 22px;
}

.section-heading > span {
  color: #9E9BB0;
  font-size: 13px;
}

.row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

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

/* Responsive */
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
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  .action-bar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .section-heading {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 375px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
