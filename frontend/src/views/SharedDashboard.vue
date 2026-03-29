<template>
  <div class="h-screen bg-gray-50 text-gray-900 font-sans flex flex-col overflow-hidden">
    <!-- Header -->
    <header class="bg-white shadow-sm px-6 py-4 flex justify-between items-center z-10 w-full shrink-0">
      <div class="flex items-center space-x-3 shrink-0 mr-4">
        <div class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-md">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
        </div>
        <h1 class="text-2xl font-black tracking-wide text-gray-800 whitespace-nowrap">Fluxus Bi</h1>
        <span class="ml-3 px-2.5 py-1 bg-gradient-to-br from-indigo-50 to-blue-50 text-indigo-500 text-xs font-bold rounded-lg tracking-wider uppercase border border-indigo-100/50 shadow-sm">Shared Link</span>
      </div>
      <div class="flex-1"></div>
      <button @click="router.push('/login')" class="px-4 py-2 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 rounded-lg font-medium transition shadow-sm border border-indigo-100">
        Create Your Own
      </button>
    </header>

    <!-- Main Area -->
    <main class="flex-1 overflow-auto p-6" v-if="!loading && !error">
      <div style="min-height: 100%; padding-bottom: 2rem;" class="bg-gray-50">
        <div v-if="dashboardTitle && layout.length > 0" class="w-full text-center flex flex-col items-center justify-center pt-2 pb-6 px-4">
          <h2 class="text-4xl font-extrabold text-gray-800 tracking-tight text-center">{{ dashboardTitle }}</h2>
          <div class="w-24 h-1.5 bg-indigo-500 mt-4 rounded-full mx-auto"></div>
        </div>
        <grid-layout
          v-if="layout.length > 0"
          v-model:layout="layout"
          :col-num="12"
          :row-height="30"
          :is-draggable="false"
          :is-resizable="false"
          :vertical-compact="true"
          :margin="[20, 20]"
          :use-css-transforms="false"
          class="w-full"
        >
          <grid-item
            v-for="item in layout"
            :key="item.i"
            :x="item.x"
            :y="item.y"
            :w="item.w"
            :h="item.h"
            :i="item.i"
            class="bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col transition-shadow hover:shadow-md"
          >
            <!-- Card Header -->
            <div class="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
              <h3 class="font-semibold text-gray-700 text-sm break-words pr-2 capitalize flex-1">{{ item.title || 'Chart ' + item.i }}</h3>
            </div>
            
            <!-- Chart Container -->
            <div class="flex-1 p-3 w-full h-full relative min-h-0">
              <div class="absolute inset-3 overflow-visible">
                <div v-if="item.config?.is_metric" class="flex flex-col items-center justify-center w-full h-full bg-gradient-to-br from-indigo-50/50 to-blue-50/50 rounded-xl border border-indigo-100/50 text-center px-4 shadow-inner" style="min-height: 120px;">
                  <h4 class="text-sm font-bold text-indigo-500 uppercase tracking-wider mb-2">{{ item.config.title }}</h4>
                  <span class="text-4xl md:text-5xl font-black text-slate-800 tracking-tight" style="line-height: 1.2;">{{ item.config.value }}</span>
                </div>
                <ChartRenderer v-else :config="item.config" />
              </div>
            </div>
          </grid-item>
        </grid-layout>
      </div>
    </main>
    
    <div v-if="loading" class="flex-1 flex flex-col items-center justify-center space-y-4">
      <div class="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
      <p class="text-gray-500 font-medium tracking-wide animate-pulse">Loading dashboard...</p>
    </div>
    
    <div v-if="error" class="flex-1 flex flex-col items-center justify-center space-y-4 text-center px-6">
      <div class="w-20 h-20 bg-red-50 text-red-500 rounded-full flex items-center justify-center mb-4">
         <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
      </div>
      <h2 class="text-2xl font-bold text-gray-800">Dashboard Not Found</h2>
      <p class="text-gray-500 max-w-md">This dashboard link is invalid or has expired.</p>
      <button @click="router.push('/login')" class="mt-6 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg shadow hover:bg-blue-700 transition">Go to Home</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { GridLayout, GridItem } from 'vue3-grid-layout'
import ChartRenderer from '../components/ChartRenderer.vue'

const route = useRoute()
const router = useRouter()
const layout = ref([])
const dashboardTitle = ref('')
const loading = ref(true)
const error = ref(false)

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

onMounted(async () => {
  const shareId = route.params.id
  if (!shareId) {
    error.value = true
    loading.value = false
    return
  }
  
  try {
    const res = await axios.get(`${API_BASE}/dashboard/${shareId}`)
    layout.value = res.data.layout
    dashboardTitle.value = res.data.title || 'Fluxus Bi Dashboard'
  } catch (err) {
    console.error(err)
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style>
.vue-grid-item:not(.vue-grid-placeholder) {
  background: white;
  border-radius: 0.75rem;
}
</style>
