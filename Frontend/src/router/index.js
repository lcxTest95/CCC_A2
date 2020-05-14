import Vue from 'vue'
import VueRouter from 'vue-router'
import meau from '../views/meau.vue'

Vue.use(VueRouter)

  const routes = [
    {
      path: '/',
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
          path: '/secondPage',
          name: 'secondPage',
          component: () => import('../views/secondPage.vue')
        },{
          path: '/third',
          name: 'third',
          component: () => import('../views/third.vue')
        }
        ,{
          path: '/fourth',
          name: 'fourth',
          component: () => import('../views/fourth.vue')
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
