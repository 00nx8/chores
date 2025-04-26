import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Cookies from 'universal-cookie';
import { createWebHistory, createRouter } from 'vue-router';

const cookies = new Cookies()

const routes = [
  {
    path: '/',
    name: "household",
    component: () => import('./pages/HousePage.vue'),
    beforeEnter: (to, from, next) => {
      if (!cookies.get('token')) {
        next( {name: 'login'} )
      } else {
        next()
      }
    },
  }, {
    path: '/login',
    name: 'login',
    component: () => import('./pages/LoginPage.vue')
  }, {
    path:'/register',
    name:'register',
    component: () => import('./pages/RegisterPage.vue')
  }, {
    path: '/chore/create',
    name: 'createChore',
    component: () => import('./pages/CreateChore.vue')
  }, {
    name: 'profile',
    path: '/profile',
    component: () => import('./pages/ProfilePage.vue'),
    beforeEnter: (to, from, next) => {
      if (!cookies.get('token')) {
        next( {name: 'login'} )
      } else {
        next()
      }
    },
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})



createApp(App)
    .use(router)
    .mount('#app')
 