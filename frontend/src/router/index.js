import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DocDetail from '../views/DocDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/doc/:id',
    name: 'DocDetail',
    component: DocDetail
  }
]

const useHashRouter = import.meta.env.VITE_USE_HASH_ROUTER === 'true'

const router = createRouter({
  history: useHashRouter
    ? createWebHashHistory(import.meta.env.BASE_URL)
    : createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
