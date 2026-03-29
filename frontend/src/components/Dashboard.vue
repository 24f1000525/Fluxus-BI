<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans flex overflow-hidden">
    <!-- Main Content -->
    <div class="flex-1 flex flex-col h-screen transition-all duration-300">
      <!-- Header -->
      <header class="bg-white shadow-sm px-6 py-4 flex justify-between items-center z-10 w-full relative">
        <div class="flex items-center space-x-3 shrink-0 mr-4">
          <div class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-md">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          </div>
          <h1 class="text-2xl font-black tracking-wide text-gray-800 whitespace-nowrap">Fluxus Bi</h1>
        </div>
        <div class="flex-1"></div>
        
        <div class="flex space-x-3 items-center ml-4 shrink-0">
          <input type="file" ref="fileInput" @change="handleFileUpload" accept=".csv" class="hidden" />
          <button @click="$refs.fileInput.click()" class="px-4 py-2 bg-blue-50 text-blue-600 hover:bg-blue-100 rounded-lg font-medium transition shadow-sm border border-blue-100 flex items-center space-x-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
            <span>Upload CSV</span>
          </button>
          
          <button @click="exportToPDF" class="px-4 py-2 bg-white text-gray-700 hover:bg-gray-50 rounded-lg font-medium transition shadow-sm border border-gray-200 flex items-center space-x-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            <span>Export PDF</span>
          </button>
          
          <button @click="publishDashboard" class="px-4 py-2 bg-indigo-600 text-white hover:bg-indigo-700 rounded-lg font-medium transition shadow-sm flex items-center space-x-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
            <span>Publish</span>
          </button>
          
          <button @click="handleLogout" class="px-4 py-2 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg font-medium transition shadow-sm border border-red-100 flex items-center space-x-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
            <span>Sign Out</span>
          </button>
        </div>
      </header>

      <!-- Prompt Input Area -->
      <div v-if="docId" class="p-6 pb-0">
        <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex space-x-4 items-center">
          <div class="flex-grow relative">
            <input 
              v-model="promptInput" 
              type="text" 
              placeholder="e.g. Show me a bar chart of sales by region..." 
              class="w-full pl-4 pr-12 py-3 bg-gray-50 border-none rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
              @keyup.enter="generateChart" 
            />
            <div class="absolute right-3 top-3 text-gray-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
          </div>
          <button 
            @click="generateChart" 
            :disabled="loadingChart || !promptInput.trim()" 
            class="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg shadow hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center min-w-[140px] justify-center"
          >
            <span v-if="loadingChart" class="flex items-center space-x-2">
              <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              <span>Generating...</span>
            </span>
            <span v-else>Generate Chart</span>
          </button>
        </div>
      </div>

      <!-- Main Dashboard Area -->
      <main class="flex-1 overflow-auto p-6">
        <div ref="dashboardRef" style="min-height: 100%; padding-bottom: 2rem;" class="bg-gray-50">
          <div v-if="dashboardTitle && layout.length > 0" class="w-full text-center flex flex-col items-center justify-center pt-2 pb-6 px-4">
            <h2 class="text-4xl font-extrabold text-gray-800 tracking-tight text-center">{{ dashboardTitle }}</h2>
            <div class="w-24 h-1.5 bg-indigo-500 mt-4 rounded-full mx-auto"></div>
          </div>
          
          <!-- Initial Skeleton Loading / Data Call-to-Action -->
          <div v-if="!docId && layout.length === 0" class="w-full relative px-2 py-8 m-auto max-w-7xl h-full min-h-[70vh] select-none pointer-events-none">
            <div class="grid grid-cols-12 gap-6 w-full opacity-60">
              <!-- Top Row KPIs -->
              <div v-for="i in 4" :key="'kpi'+i" class="col-span-12 sm:col-span-6 lg:col-span-3 h-36 bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col justify-center">
                 <div class="w-24 h-4 bg-gray-200 rounded-full animate-pulse mb-4"></div>
                 <div class="w-16 h-10 bg-gray-200 rounded-xl animate-pulse"></div>
              </div>
              
              <!-- Main Bar Chart Skeleton (Embedded Call-to-Action) -->
              <div class="col-span-12 lg:col-span-8 h-96 bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col relative justify-between overflow-hidden">
                <div class="w-40 h-5 bg-gray-200 rounded-full animate-pulse mb-8 z-0"></div>
                <div class="flex-1 flex items-end space-x-4 border-l-2 border-b-2 border-gray-100 p-4 pb-0 z-0">
                  <div class="w-full bg-blue-100 rounded-t-md animate-pulse h-[40%]"></div>
                  <div class="w-full bg-blue-200 rounded-t-md animate-pulse h-[70%] delay-75"></div>
                  <div class="w-full bg-blue-100 rounded-t-md animate-pulse h-[30%] delay-150"></div>
                  <div class="w-full bg-indigo-200 rounded-t-md animate-pulse h-[85%] delay-300"></div>
                  <div class="w-full bg-blue-100 rounded-t-md animate-pulse h-[50%] delay-100"></div>
                  <div class="w-full bg-indigo-100 rounded-t-md animate-pulse h-[60%] delay-200"></div>
                </div>
                
              </div>

              <!-- Radial Chart Skeleton -->
              <div class="col-span-12 lg:col-span-4 h-96 bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col items-center justify-center relative">
                <div class="w-32 h-4 bg-gray-200 rounded-full animate-pulse absolute top-6 left-6"></div>
                <div class="w-48 h-48 rounded-full border-[1.5rem] border-gray-100 animate-pulse border-t-indigo-200 border-r-blue-200 shadow-sm"></div>
              </div>

              <!-- Line Chart Skeletons -->
              <div v-for="i in 3" :key="'line'+i" class="col-span-12 lg:col-span-4 h-64 bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col relative overflow-hidden">
                <div class="w-28 h-4 bg-gray-200 rounded-full animate-pulse mb-6"></div>
                <svg class="w-full h-full text-indigo-100 animate-pulse" preserveAspectRatio="none" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="3">
                  <path d="M0,80 Q20,40 50,60 T100,20" stroke-linecap="round"></path>
                </svg>
              </div>
            </div>

            <!-- Global Centered Text Overlay -->
            <div class="absolute inset-0 flex flex-col items-center justify-center z-10">
              <div class="flex flex-col items-center justify-center space-y-4 bg-white/90 backdrop-blur-xl px-12 py-8 rounded-[2rem] shadow-xl border border-gray-100 animate-pulse">
                <div class="p-4 bg-blue-50 text-blue-600 rounded-[1rem] shadow-inner mb-2 border border-blue-100">
                  <svg class="w-14 h-14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path>
                    <path d="M14 2v4a2 2 0 0 0 2 2h4"></path>
                    <path d="M8 18v-2"></path>
                    <path d="M12 18v-4"></path>
                    <path d="M16 18v-6"></path>
                  </svg>
                </div>
                <div class="flex flex-col items-center text-center space-y-1">
                  <h2 class="text-2xl font-black text-gray-800 tracking-tight">Upload a CSV file</h2>
                  <p class="text-lg font-medium text-gray-500">to get started</p>
                </div>
              </div>
            </div>
          </div>
        
        <grid-layout
          v-if="layout.length > 0"
          v-model:layout="layout"
          :col-num="12"
          :row-height="30"
          :is-draggable="!isExporting"
          :is-resizable="!isExporting"
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
            class="bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col transition-shadow hover:shadow-md group"
            drag-allow-from=".drag-handle"
            drag-ignore-from=".no-drag"
          >
            <!-- Card Header -->
            <div class="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-gray-50/50 drag-handle cursor-move">
              <h3 class="font-semibold text-gray-700 text-sm break-words pr-2 capitalize flex-1">{{ item.title || 'Chart ' + item.i }}</h3>
              
              <!-- Settings Toggle -->
              <div v-if="!isExporting" data-html2canvas-ignore="true" class="flex items-center space-x-2 no-drag opacity-0 group-hover:opacity-100 transition-opacity">
                <div class="relative" v-if="!item.config?.is_metric">
                  <select 
                    v-model="item.chartType" 
                    @change="updateChartType(item)" 
                    class="appearance-none bg-white border border-gray-300 text-gray-700 text-xs rounded px-2 py-1 pr-6 focus:outline-none focus:ring-1 focus:ring-blue-500 cursor-pointer"
                  >
                    <option value="bar">Bar</option>
                    <option value="line">Line</option>
                    <option value="pie">Pie</option>
                    <option value="scatter">Scatter</option>
                  </select>
                  <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-1 text-gray-500">
                    <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                  </div>
                </div>
                <button @click="removeChart(item.i)" class="text-gray-400 hover:text-red-500 transition p-1 rounded-md hover:bg-red-50" title="Remove Chart">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </div>
            </div>
            
            <!-- Chart Container -->
            <div class="flex-1 p-3 w-full h-full relative no-drag min-h-0">
              <div class="absolute inset-3 overflow-visible">
                
                <!-- Metric Card UI -->
                <div v-if="item.config?.is_metric" class="flex flex-col items-center justify-center w-full h-full bg-gradient-to-br from-indigo-50/50 to-blue-50/50 rounded-xl border border-indigo-100/50 text-center px-4 shadow-inner" style="min-height: 120px;">
                  <h4 class="text-sm font-bold text-indigo-500 uppercase tracking-wider mb-2">{{ item.config.title }}</h4>
                  <span class="text-4xl md:text-5xl font-black text-slate-800 tracking-tight" style="line-height: 1.2;">{{ item.config.value }}</span>
                </div>
                
                <!-- standard Echarts -->
                <ChartRenderer v-else :config="item.config" :is-exporting="isExporting" />
              </div>
            </div>
          </grid-item>
        </grid-layout>
        </div>
      </main>
    </div>

  <!-- Floating Q&A Chatbot (Bottom-Right FAB) -->
  <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end space-y-3">

    <!-- Chat Popup Window -->
    <transition name="chat-slide">
      <div
        v-if="botOpen"
        class="w-[360px] bg-white rounded-2xl shadow-2xl border border-gray-100 flex flex-col overflow-hidden"
        style="max-height: 520px;"
      >
        <!-- Header -->
        <div class="px-5 py-3.5 bg-gradient-to-r from-gray-900 to-indigo-900 text-white flex justify-between items-center">
          <div class="flex items-center space-x-2.5">
            <div class="w-7 h-7 rounded-full bg-indigo-500/30 flex items-center justify-center">
              <svg class="w-4 h-4 text-indigo-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
            </div>
            <div>
              <h3 class="font-bold text-sm tracking-wide">Data Q&A Bot</h3>
              <p class="text-xs text-indigo-300">Ask anything about your data</p>
            </div>
          </div>
          <button @click="toggleBot" class="text-gray-400 hover:text-white transition rounded-lg p-1 hover:bg-white/10">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <!-- Chat Messages -->
        <div class="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50" ref="chatContainer" style="max-height: 340px; min-height: 180px;">
          <div v-if="chatMessages.length === 0" class="flex flex-col items-center justify-center text-center py-10">
            <div class="w-12 h-12 rounded-full bg-indigo-50 text-indigo-400 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
            </div>
            <p class="text-sm text-gray-500 font-medium">Ask me anything about your uploaded data.</p>
          </div>

          <div v-for="(msg, i) in chatMessages" :key="i" class="flex flex-col" :class="msg.role === 'user' ? 'items-end' : 'items-start'">
            <span class="text-xs text-gray-400 mb-1 px-1">{{ msg.role === 'user' ? 'You' : 'AI' }}</span>
            <div
              :class="msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white border border-gray-200 text-gray-800 shadow-sm'"
              class="inline-block px-4 py-2.5 rounded-2xl max-w-[85%] text-sm leading-relaxed"
            >{{ msg.content }}</div>
          </div>

          <div v-if="botLoading" class="flex flex-col items-start">
            <span class="text-xs text-gray-400 mb-1 px-1">AI</span>
            <div class="bg-white border border-gray-200 shadow-sm inline-block px-4 py-3 rounded-2xl">
              <div class="flex space-x-1.5">
                <div class="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style="animation-delay:0.1s"></div>
                <div class="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style="animation-delay:0.2s"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="p-3 border-t border-gray-100 bg-white">
          <div class="relative">
            <input
              v-model="botInput"
              @keyup.enter="askBot"
              :disabled="!docId || botLoading"
              type="text"
              placeholder="Ask about your data..."
              class="w-full pl-4 pr-10 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-sm transition disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
            <button
              @click="askBot"
              :disabled="!docId || botLoading || !botInput.trim()"
              class="absolute right-2 top-2 text-indigo-600 hover:text-indigo-700 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
            </button>
          </div>
          <p v-if="!docId" class="text-xs text-amber-500 mt-1.5 ml-1">Upload a CSV to start chatting.</p>
        </div>
      </div>
    </transition>

    <!-- FAB Toggle Button -->
    <button
      @click="toggleBot"
      class="w-14 h-14 bg-gradient-to-br from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white rounded-full shadow-2xl flex items-center justify-center transition-all duration-200 hover:scale-110 active:scale-95"
      :title="botOpen ? 'Close Chat' : 'Open Q&A Bot'"
    >
      <svg v-if="!botOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
      <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
    </button>
  </div><!-- end FAB wrapper -->
</div><!-- end root wrapper -->
</template>



<script setup>
import { ref, reactive, nextTick, shallowRef } from 'vue'
import { useRouter } from 'vue-router'
import { GridLayout, GridItem } from 'vue3-grid-layout'
import ChartRenderer from './ChartRenderer.vue'
import { jsPDF } from 'jspdf'
import html2canvas from 'html2canvas'
import axios from 'axios'

// State
const router = useRouter()
const isExporting = ref(false)
const docId = ref(null)
const layout = ref([])
const dashboardTitle = ref('')
const promptInput = ref('')
const loadingChart = ref(false)
const dashboardRef = ref(null)
const botOpen = ref(false)
const botInput = ref('')
const botLoading = ref(false)
const chatMessages = ref([])
const chatContainer = ref(null)

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
let fileSchema = null
let chartCounter = 0

// Actions
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await axios.post(`${API_BASE}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    docId.value = res.data.doc_id
    fileSchema = res.data.schema
    dashboardTitle.value = res.data.dashboard_title || 'Smart BI Dashboard'
    layout.value = [] // Reset the dashboard layout
    chartCounter = 0

    // Auto-generate initial charts from backend templates
    if (res.data.auto_charts && res.data.dataset_subset) {
      let currentX = 0;
      let currentY = 0;

      res.data.auto_charts.forEach((chartConfig, idx) => {
        chartConfig.dataset = { source: res.data.dataset_subset }
        const chartTitle = chartConfig.title?.text || chartConfig.title || `Insight ${idx + 1}`
        
        // Don't double-render the title inside the ECharts canvas since Vue handles it
        if (chartConfig.title && typeof chartConfig.title === 'object') {
          delete chartConfig.title 
        }
        
        const w = chartConfig.grid_w || 6;
        const h = chartConfig.is_metric ? 5 : (chartConfig.grid_h || 12);

        if (currentX + w > 12) {
          currentX = 0;
          currentY += 12; // push down for a new row
        }
        
        layout.value.push({
          x: currentX,
          y: currentY,
          w: w,
          h: h,
          i: String(++chartCounter),
          title: chartTitle,
          chartType: chartConfig.is_metric ? 'metric' : detectChartType(chartConfig),
          config: chartConfig
        })
        
        currentX += w;
      })
    }
    
    // Add system message
    chatMessages.value.push({
      role: 'system',
      content: `I've analyzed your file. It has ${fileSchema.columns.length} columns. What would you like to know?`
    })
    
    event.target.value = null // reset
  } catch (error) {
    console.error(error)
    alert(error.response?.data?.error || 'Upload failed')
  }
}

const generateChart = async () => {
  if (!promptInput.value.trim() || !docId.value) return
  
  loadingChart.value = true
  const currentPrompt = promptInput.value
  
  try {
    const res = await axios.post(`${API_BASE}/generate-chart`, {
      doc_id: docId.value,
      prompt: currentPrompt
    })
    
    let config = res.data.config
    // Parse if string
    if (typeof config === 'string') {
      try { config = JSON.parse(config) } catch (e) { console.warn("Could not parse config JSON string"); }
    }
    
    // Determine chartType for dropdown depending on if it's a metric
    const chartType = config.is_metric ? 'metric' : detectChartType(config)
    
    const currentY = layout.value.reduce((acc, item) => Math.max(acc, item.y + item.h), 0)
    
    // We add to the layout
    layout.value.push({
      x: (layout.value.length * 6) % 12,
      y: currentY, // place at bottom safely
      w: 6,
      h: 9, // Minimum height for charts
      i: String(++chartCounter),
      title: deriveGeneratedChartTitle(currentPrompt, config, chartType),
      chartType: chartType,
      config: config
    })
    
    promptInput.value = ''
  } catch (error) {
    console.error(error)
    alert(error.response?.data?.error || 'Failed to generate chart')
  } finally {
    loadingChart.value = false
  }
}

// Determines the chart type based on ECharts series config
const detectChartType = (config) => {
  if (config?.series && Array.isArray(config.series) && config.series.length > 0) {
    return config.series[0].type || 'bar'
  }
  return 'bar'
}

const prettifyTitle = (value) => {
  const acronyms = new Set(['api', 'llm', 'ai', 'sql', 'kpi', 'id'])
  return String(value || '')
    .replace(/[_-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .split(' ')
    .filter(Boolean)
    .map(word => {
      const lower = word.toLowerCase()
      if (acronyms.has(lower)) return lower.toUpperCase()
      if (/^[A-Z0-9]{2,}$/.test(word)) return word
      return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    })
    .join(' ')
}

const deriveGeneratedChartTitle = (prompt, config, chartType) => {
  const configTitle = typeof config?.title === 'string'
    ? config.title
    : (typeof config?.title?.text === 'string' ? config.title.text : '')

  if (configTitle && configTitle.trim()) {
    return prettifyTitle(configTitle)
  }

  const cleanedPrompt = String(prompt || '')
    .replace(/[_-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/^(show|give|create|generate|draw|plot|build|display|make)\s+(me\s+)?/i, '')
    .replace(/^(a|an|the)\s+/i, '')
    .replace(/^(pie|bar|line|scatter)\s+(chart|graph|plot)\s*(of|for)?\s*/i, '')
    .replace(/^(chart|graph|plot)\s*(of|for)?\s*/i, '')
    .trim()

  if (cleanedPrompt) {
    return prettifyTitle(cleanedPrompt)
  }

  const chartLabel = chartType ? `${String(chartType).charAt(0).toUpperCase()}${String(chartType).slice(1)}` : 'Chart'
  return `${chartLabel} Insight`
}

const firstNumericColumn = (rows, excluded = new Set()) => {
  if (!Array.isArray(rows) || rows.length === 0) return null
  const sample = rows.find(r => r && typeof r === 'object') || {}
  const keys = Object.keys(sample)
  for (const key of keys) {
    if (excluded.has(key)) continue
    const hasNumeric = rows.some(row => {
      const val = row?.[key]
      return val !== null && val !== undefined && val !== '' && Number.isFinite(Number(val))
    })
    if (hasNumeric) return key
  }
  return null
}

const firstCategoricalColumn = (rows) => {
  if (!Array.isArray(rows) || rows.length === 0) return null
  const sample = rows.find(r => r && typeof r === 'object') || {}
  const keys = Object.keys(sample)
  for (const key of keys) {
    const hasText = rows.some(row => typeof row?.[key] === 'string' && String(row[key]).trim() !== '')
    if (hasText) return key
  }
  return keys[0] || null
}

const inferEncode = (config) => {
  const series = Array.isArray(config?.series) ? config.series : []
  const firstSeries = series[0] || {}
  const encode = firstSeries.encode || {}

  const x = Array.isArray(encode.x) ? encode.x[0] : (encode.x || encode.itemName)
  const y = Array.isArray(encode.y) ? encode.y[0] : (encode.y || encode.value)

  if (x && y) return { x, y }

  const rows = config?.dataset?.source
  if (Array.isArray(rows) && rows.length > 0) {
    const inferredX = x || firstCategoricalColumn(rows)
    const inferredY = y || firstNumericColumn(rows, new Set(inferredX ? [inferredX] : []))
    if (inferredX && inferredY) return { x: inferredX, y: inferredY }
  }

  // If chart currently uses explicit pie data [{name, value}], create a temporary mapping.
  if (Array.isArray(firstSeries?.data) && firstSeries.data.length > 0) {
    const pieRows = firstSeries.data
      .filter(d => d && typeof d === 'object')
      .map((d, idx) => ({ category: d.name ?? `Item ${idx + 1}`, value: Number(d.value) || 0 }))

    if (pieRows.length > 0) {
      config.dataset = { source: pieRows }
      series.forEach(s => { delete s.data })
      return { x: 'category', y: 'value' }
    }
  }

  return { x: null, y: null }
}

const applyChartTypeShape = (config, chartType) => {
  const next = config
  const series = Array.isArray(next.series) ? next.series : []
  const { x, y } = inferEncode(next)

  if (chartType === 'pie') {
    delete next.xAxis
    delete next.yAxis
    delete next.dataZoom
    next.tooltip = { ...(next.tooltip || {}), trigger: 'item' }

    series.forEach(s => {
      s.type = 'pie'
      if (!s.encode && x && y) {
        s.encode = { itemName: x, value: y }
      } else if (s.encode) {
        s.encode = {
          itemName: Array.isArray(s.encode.x) ? s.encode.x[0] : (s.encode.x || s.encode.itemName || x),
          value: Array.isArray(s.encode.y) ? s.encode.y[0] : (s.encode.y || s.encode.value || y)
        }
      }
    })
    return next
  }

  // Cartesian chart shape (bar, line, scatter)
  const xAxisType = chartType === 'scatter' ? 'value' : 'category'
  next.xAxis = { ...(typeof next.xAxis === 'object' ? next.xAxis : {}), type: xAxisType }
  next.yAxis = { ...(typeof next.yAxis === 'object' ? next.yAxis : {}), type: 'value' }
  next.tooltip = { ...(next.tooltip || {}), trigger: chartType === 'scatter' ? 'item' : 'axis' }

  series.forEach(s => {
    s.type = chartType
    if (x && y) {
      s.encode = { x, y }
    }
  })

  return next
}

// Allows user to dynamically change chart type from the card UI
const updateChartType = (item) => {
  if (item.config && item.config.series) {
    const newConfig = JSON.parse(JSON.stringify(item.config))
    applyChartTypeShape(newConfig, item.chartType)
    item.config = newConfig // trigger reactivity
  }
}

const removeChart = (id) => {
  layout.value = layout.value.filter(item => item.i !== id)
}

const toggleBot = () => {
  botOpen.value = !botOpen.value
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const askBot = async () => {
  if (!botInput.value.trim() || !docId.value || botLoading.value) return
  
  const question = botInput.value
  chatMessages.value.push({ role: 'user', content: question })
  botInput.value = ''
  botLoading.value = true
  await scrollToBottom()
  
  try {
    const res = await axios.post(`${API_BASE}/query`, {
      doc_id: docId.value,
      question: question
    })
    
    chatMessages.value.push({ role: 'bot', content: res.data.answer })
  } catch (error) {
    console.error(error)
    chatMessages.value.push({ role: 'bot', content: 'Sorry, I encountered an error processing your request.' })
  } finally {
    botLoading.value = false
    await scrollToBottom()
  }
}

const exportToPDF = async () => {
  if (!dashboardRef.value || layout.value.length === 0) {
    alert("Add some charts to the dashboard first!")
    return
  }
  
  try {
    isExporting.value = true;
    await nextTick();
    await new Promise(r => setTimeout(r, 100)); // ensure layout nodes are stripped
    const el = dashboardRef.value
    
    // Very important: if the container is scrolled globally, html2canvas will aggressively miss it.
    // Reset scroll of the parent container to top
    const mainEl = el.parentElement;
    const oldScroll = mainEl ? mainEl.scrollTop : 0;
    if (mainEl) mainEl.scrollTop = 0;
    
    // Generate an image from the dashboard element
    const canvas = await html2canvas(el, { 
      scale: 1.5, 
      useCORS: true,
      backgroundColor: '#f8fafc', // Force light background so it's not transparent/black
      width: el.scrollWidth,
      height: el.scrollHeight,
      windowWidth: el.scrollWidth,
      windowHeight: el.scrollHeight,
      x: 0,
      y: 0
    })
    
    // Restore scroll after capture
    if (mainEl) mainEl.scrollTop = oldScroll;
    
    isExporting.value = false;
    
    const imgData = canvas.toDataURL('image/png')
    
    // Use actual DOM dimensions for the PDF page size, 
    // but give it a high-res (scale 1.5) image.
    const pdfWidth = canvas.width / 1.5
    const pdfHeight = canvas.height / 1.5
    
    const pdf = new jsPDF({
      orientation: pdfWidth > pdfHeight ? 'landscape' : 'portrait',
      unit: 'px',
      format: [pdfWidth, pdfHeight]
    })
    
    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight)
    pdf.save(`${dashboardTitle.value || 'Fluxus-Bi-Dashboard'}.pdf`)
  } catch (e) {
    console.error("Failed to export PDF", e)
    alert("Failed to capture dashboard.")
  }
}

const publishDashboard = async () => {
  if (layout.value.length === 0) {
    alert("Please add at least one chart before publishing!")
    return
  }
  
  try {
    const res = await axios.post(`${API_BASE}/publish`, {
      layout: layout.value,
      title: dashboardTitle.value
    })
    
    const uniqueId = res.data.share_id
    const shareUrl = `${window.location.origin}/share/${uniqueId}`
    
    try {
      await navigator.clipboard.writeText(shareUrl)
      alert(`🎉 Dashboard Published Successfully!\n\nThe shareable link has been automatically copied to your clipboard:\n${shareUrl}`)
    } catch (err) {
      alert(`🎉 Dashboard Published Successfully!\n\nShare URL:\n${shareUrl}`)
    }
  } catch (error) {
    console.error("Publish error:", error)
    alert("Failed to publish dashboard. Please check your connection.")
  }
}

const handleLogout = () => {
  localStorage.removeItem('auth_token')
  router.push('/login')
}
</script>

<style>
/* Vue Grid Layout global overrides */
.vue-grid-item:not(.vue-grid-placeholder) {
  background: white;
  border-radius: 0.75rem;
}
.vue-grid-item.resizing {
  opacity: 0.9;
}
.vue-grid-item.vue-grid-placeholder {
  background: rgba(59, 130, 246, 0.1) !important;
  border: 2px dashed rgba(59, 130, 246, 0.5) !important;
  border-radius: 0.75rem;
  opacity: 1 !important;
  transition-duration: 100ms;
}
/* Ensure the inner drag handle acts correctly inside the grid */
.vue-grid-item > .vue-resizable-handle {
  z-index: 20;
}
/* Floating chat popup slide animation */
.chat-slide-enter-active,
.chat-slide-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.chat-slide-enter-from,
.chat-slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.97);
}
</style>
