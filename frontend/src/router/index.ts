import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { title: '首页' },
    },
    {
      path: '/detect',
      name: 'detect',
      component: () => import('@/views/Detect.vue'),
      meta: { title: '单图检测' },
    },
    {
      path: '/compare',
      name: 'compare',
      component: () => import('@/views/Compare.vue'),
      meta: { title: '三模型对比' },
    },
    {
      path: '/robustness',
      name: 'robustness',
      component: () => import('@/views/Robustness.vue'),
      meta: { title: '浓度鲁棒性' },
    },
    {
      path: '/intermediate',
      name: 'intermediate',
      component: () => import('@/views/Intermediate.vue'),
      meta: { title: '中间结果' },
    },
    {
      path: '/video',
      name: 'video',
      component: () => import('@/views/Video.vue'),
      meta: { title: '视频检测' },
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/About.vue'),
      meta: { title: '关于' },
    },
  ],
})

router.afterEach((to) => {
  const baseTitle = 'Hazydet Demo'
  document.title = to.meta.title ? `${to.meta.title} | ${baseTitle}` : baseTitle
})

export default router
