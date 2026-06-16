import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/home'
      },
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'pets',
        name: 'Pets',
        component: () => import('@/views/Pets.vue'),
        meta: { title: '宠物档案' }
      },
      {
        path: 'pets/:id',
        name: 'PetDetail',
        component: () => import('@/views/PetDetail.vue'),
        meta: { title: '宠物详情' }
      },
      {
        path: 'posts',
        name: 'Posts',
        component: () => import('@/views/Posts.vue'),
        meta: { title: '动态广场' }
      },
      {
        path: 'matches',
        name: 'Matches',
        component: () => import('@/views/Matches.vue'),
        meta: { title: '智能配对' }
      },
      {
        path: 'encyclopedia',
        name: 'Encyclopedia',
        component: () => import('@/views/Encyclopedia.vue'),
        meta: { title: '宠物百科' }
      },
      {
        path: 'encyclopedia/breed/:id',
        name: 'BreedDetail',
        component: () => import('@/views/BreedDetail.vue'),
        meta: { title: '品种详情' }
      },
      {
        path: 'encyclopedia/disease/:id',
        name: 'DiseaseDetail',
        component: () => import('@/views/DiseaseDetail.vue'),
        meta: { title: '疾病详情' }
      },
      {
        path: 'nearby',
        name: 'Nearby',
        component: () => import('@/views/Nearby.vue'),
        meta: { title: '附近宠物' }
      },
      {
        path: 'services',
        name: 'Services',
        component: () => import('@/views/Services.vue'),
        meta: { title: '服务导航' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/Profile.vue'),
        meta: { title: '个人中心' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && userStore.isLoggedIn) {
    next('/home')
  } else {
    next()
  }
})

export default router
