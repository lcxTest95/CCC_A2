import Vue from 'vue'
import VueRouter from 'vue-router'
import meau from '../views/meau.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: () => import('../views/welcome.vue')
  },
  {
    path: '/meau',
    name: 'meau',
    component: meau,
    meta: {
      requireAuth: true
    },
    children: [
      {
        path: '/map',
        name: 'map',
        component: () => import('../views/map.vue')
      },
      {
        path: '/graphs',
        name: 'graphs',
        component: () => import('../views/graphs.vue')
      }, {
        path: '/report',
        name: 'report',
        component: () => import('../views/report.vue')
      }
    ]
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
