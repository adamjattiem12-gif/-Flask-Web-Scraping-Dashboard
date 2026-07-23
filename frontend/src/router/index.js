// Application route definitions will live here.
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/retail-goods',
    name: 'RetailGoods',
    component: () => import('@/views/RetailGoods.vue')
  },
  {
    path: '/digital-assets',
    name: 'DigitalAssets',
    component: () => import('@/views/DigitalAssets.vue')
  },
  {
    path: '/watchlist',
    name: 'Watchlist',
    component: () => import('@/views/WatchlistView.vue')
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue')
  },
  {
    path: '/websites',
    name: 'Websites',
    component: () => import('@/views/WebsitesManager.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router