<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans flex overflow-hidden">
    <!-- Main Content -->
    <div class="flex-1 flex flex-col h-screen transition-all duration-300" :class="botOpen ? 'mr-80' : ''">
      <!-- Header -->
      <header class="bg-white shadow-sm px-6 py-4 flex justify-between items-center z-10 w-full relative">
        <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent truncate flex-1">Smart BI Dashboard</h1>
        
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

          <button @click="toggleBot" class="ml-4 p-2 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-full transition" title="Toggle Q&A Bot">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
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
      <main class="flex-1 overflow-auto p-6" ref="dashboardRef">
        <div v-if="!docId && layout.length === 0" class="h-full flex flex-col items-center justify-center text-gray-400 space-y-4">
          <svg class="w-16 h-16 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          <p class="text-lg">Upload a CSV file to get started</p>
        </div>
        
        <grid-layout
          v-if="layout.length > 0"
          v-model:layout="layout"
          :col-num="12"
          :row-height="30"
          :is-draggable="true"
          :is-resizable="true"
          :vertical-compact="true"
          :margin="[20, 20]"
          :use-css-transforms="true"
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
            class="bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col transition-shadow hover:shadow-md overflow-hidden group"
            drag-allow-from=".drag-handle"
            drag-ignore-from=".no-drag"
          >
            <!-- Card Header -->
            <div class="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-gray-50/50 drag-handle cursor-move">
              <h3 class="font-semibold text-gray-700 text-sm truncate pr-2 capitalize flex-1">{{ item.title || 'Chart ' + item.i }}</h3>
              
              <!-- Settings Toggle -->
              <div class="flex items-center space-x-2 no-drag opacity-0 group-hover:opacity-100 transition-opacity">
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
            <div class="flex-1 p-3 w-full h-full relative no-drag min-h-0 overflow-hidden">
              <div class="absolute inset-3">
                
                <!-- Metric Card UI -->
                <div v-if="item.config?.is_metric" class="flex flex-col items-center justify-center w-full h-full bg-gradient-to-br from-indigo-50/50 to-blue-50/50 rounded-xl border border-indigo-100/50 text-center px-4 shadow-inner">
                  <h4 class="text-sm font-bold text-indigo-500 uppercase tracking-wider mb-2">{{ item.config.title }}</h4>
                  <span class="text-5xl lg:text-7xl font-extrabold text-slate-800 tracking-tighter truncate w-full">{{ item.config.value }}</span>
                </div>
                
                <!-- standard Echarts -->
                <ChartRenderer v-else :config="item.config" />
              </div>
            </div>
          </grid-item>
        </grid-layout>
      </main>
    </div>

    <!-- Data Q&A Sidebar -->
    <aside 
      class="fixed right-0 top-0 w-80 h-full bg-white shadow-[-4px_0_15px_rgba(0,0,0,0.05)] border-l border-gray-200 flex flex-col z-50 transform transition-transform duration-300 ease-in-out"
      :class="botOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      <div class="px-5 py-4 bg-gray-900 text-white flex justify-between items-center border-b border-gray-800">
        <div class="flex items-center space-x-2">
          <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
          <h3 class="font-bold text-sm tracking-wide">Data Q&A Bot</h3>
        </div>
        <button @click="toggleBot" class="text-gray-400 hover:text-white transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
      
      <!-- Chat Area -->
      <div class="flex-1 overflow-y-auto p-5 space-y-4 bg-gray-50 flex flex-col" ref="chatContainer">
        <div v-if="chatMessages.length === 0" class="text-center text-gray-400 mt-10 text-sm">
          Ask me anything about your uploaded data.
        </div>
        
        <div v-for="(msg, i) in chatMessages" :key="i" class="flex flex-col" :class="msg.role === 'user' ? 'items-end' : 'items-start'">
          <span class="text-xs text-gray-400 mb-1 px-1">{{ msg.role === 'user' ? 'You' : 'Grok' }}</span>
          <div 
            :class="msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white border text-gray-800 shadow-sm'" 
            class="inline-block px-4 py-2.5 rounded-2xl max-w-[85%] text-sm"
            style="line-height: 1.5;"
          >
            {{ msg.content }}
          </div>
        </div>
        
        <div v-if="botLoading" class="flex flex-col items-start">
          <span class="text-xs text-gray-400 mb-1 px-1">Grok</span>
          <div class="bg-white border text-gray-800 shadow-sm inline-block px-4 py-3 rounded-2xl">
            <div class="flex space-x-1.5">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Input Area -->
      <div class="p-4 border-t border-gray-200 bg-white shadow-sm">
        <div class="relative">
          <input 
            v-model="botInput" 
            @keyup.enter="askBot" 
            :disabled="!docId || botLoading" 
            type="text" 
            placeholder="Ask about your data..." 
            class="w-full pl-4 pr-10 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition disabled:bg-gray-100 disabled:cursor-not-allowed" 
          />
          <button 
            @click="askBot" 
            :disabled="!docId || botLoading || !botInput.trim()"
            class="absolute right-2 top-2 text-blue-600 hover:text-blue-700 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
          </button>
        </div>
        <p v-if="!docId" class="text-xs text-red-500 mt-2 ml-1">Please upload a CSV file first.</p>
      </div>
    </aside>
  </div>
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
const docId = ref(null)
const layout = ref([])
const promptInput = ref('')
const loadingChart = ref(false)
const dashboardRef = ref(null)
const botOpen = ref(false)
const botInput = ref('')
const botLoading = ref(false)
const chatMessages = ref([])
const chatContainer = ref(null)

const API_BASE = 'http://localhost:5000'
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
        const h = chartConfig.grid_h || 9;

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
      title: currentPrompt.substring(0, 30) + (currentPrompt.length > 30 ? '...' : ''),
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

// Allows user to dynamically change chart type from the card UI
const updateChartType = (item) => {
  if (item.config && item.config.series) {
    const newConfig = JSON.parse(JSON.stringify(item.config))
    newConfig.series.forEach(s => s.type = item.chartType)
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
    // Generate an image from the dashboard element
    const canvas = await html2canvas(dashboardRef.value, { scale: 2, useCORS: true })
    const imgData = canvas.toDataURL('image/png')
    
    const pdf = new jsPDF({
      orientation: 'landscape',
      unit: 'px',
      format: [canvas.width, canvas.height]
    })
    
    pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height)
    pdf.save('Smart-BI-Dashboard.pdf')
  } catch (e) {
    console.error("Failed to export PDF", e)
    alert("Failed to capture dashboard.")
  }
}

const publishDashboard = () => {
  if (layout.value.length === 0) {
    alert("Add charts before publishing!")
    return
  }
  
  // Simulate publishing by generating a unique URL
  const uniqueId = Math.random().toString(36).substr(2, 9)
  const fakeUrl = `${window.location.origin}/share/${uniqueId}`
  
  alert(`Dashboard Published Successfully!\n\nShare URL:\n${fakeUrl}\n\n(This is a simulated publish flow as per requirements)`)
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
</style>
