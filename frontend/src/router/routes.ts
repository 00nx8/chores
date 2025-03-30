import type { RouteRecordRaw } from 'vue-router';
import { Cookies } from 'quasar';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    beforeEnter: (to, from, next) => {
      const username = Cookies.get('token')

      if (username) {
        next()
      } else {
        next( {name: 'login'} )
      }
    },

    children: [
      { path: '',
        component: () => import('pages/IndexPage.vue')
      },
      {
        name: 'household',
        path: '/household',
        component: () => import('pages/HouseholdPage.vue')
      }
    ],
  },
  {
    name: 'login',
    path: '/login',
    component: () => import('pages/LoginPage.vue')
  },
  {
    name: 'register',
    path: '/register',
    component: () => import('pages/RegisterPage.vue')
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
