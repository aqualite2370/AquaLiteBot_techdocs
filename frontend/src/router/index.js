import { createRouter, createWebHistory } from 'vue-router'
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

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
