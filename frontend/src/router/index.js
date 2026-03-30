import { createRouter, createWebHistory } from 'vue-router'
// Assuming Dashboard was placed in components
import Dashboard from '../components/Dashboard.vue'
import Login from '../views/Login.vue'
import SharedDashboard from '../views/SharedDashboard.vue'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { requiresAuth: false }
    },
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }
    },
    {
        path: '/share/:id',
        name: 'SharedDashboard',
        component: SharedDashboard,
        meta: { requiresAuth: false }
    },
    {
        path: '/share',
        name: 'SharedDashboardQuery',
        component: SharedDashboard,
        meta: { requiresAuth: false }
    },
    {
        path: '/s',
        name: 'SharedDashboardShort',
        component: SharedDashboard,
        meta: { requiresAuth: false }
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
    } else {
        next()
    }
})

export default router
