import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      redirect: '/movies',
    },
    {
      path: '/movies',
      name: 'Movies',
      component: () => import('../views/Movies.vue'),
    },
    {
      path: '/movies/create',
      name: 'CreateMovie',
      component: () => import('../views/MovieForm.vue'),
    },
    {
      path: '/movies/:id/edit',
      name: 'EditMovie',
      component: () => import('../views/MovieForm.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../views/NotFound.vue')
    }
  ],
})

export default router
