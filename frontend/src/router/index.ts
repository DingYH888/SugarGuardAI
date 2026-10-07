import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
    { path: '/blood-sugar', name: 'BloodSugar', component: () => import('../views/BloodSugar.vue') },
    { path: '/diet', name: 'DietManage', component: () => import('../views/DietManage.vue') },
    { path: '/medication', name: 'Medication', component: () => import('../views/Medication.vue') },
    { path: '/exercise', name: 'Exercise', component: () => import('../views/Exercise.vue') },
    { path: '/reports', name: 'HealthReport', component: () => import('../views/HealthReport.vue') },
    { path: '/chat', name: 'AIChat', component: () => import('../views/AIChat.vue') },
    { path: '/patients', name: 'PatientManage', component: () => import('../views/PatientManage.vue') },
  ],
})

export default router
