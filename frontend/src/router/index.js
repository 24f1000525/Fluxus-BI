import { createRouter, createWebHistory } from 'vue-router'
// Assuming Dashboard was placed in components
import Dashboard from '../components/Dashboard.vue'
import Login from '../views/Login.vue'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { requiresAuth: false }
    },
    {
        path: '/',
        redirect: '/dashboard'
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Simple authentication guard
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('auth_token')

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else if (to.path === '/login' && isAuthenticated) {
        next('/dashboard')
    } else {
        next()
    }
})

export default router
