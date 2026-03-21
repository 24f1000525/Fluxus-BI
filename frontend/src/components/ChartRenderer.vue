<template>
  <div class="w-full h-full absolute inset-0" ref="chartContainer">
    <div v-if="error" class="absolute inset-0 flex items-center justify-center text-red-500 bg-red-50 rounded-lg text-sm p-4 text-center border-dashed border border-red-200">
      <div class="flex flex-col items-center">
        <svg class="w-8 h-8 opacity-50 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        <span>Invalid Chart Configuration.<br>Please adjust your prompt.</span>
      </div>
    </div>
    <v-chart v-else ref="chartRef" class="w-full h-full absolute inset-0" :option="mergedConfig" autoresize />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import {
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  CustomChart // Include custom in case the LLM proposes it
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  ToolboxComponent,
  DataZoomComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// Register all necessary ECharts modules manually to minimize bundle size
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  CustomChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  ToolboxComponent,
  DataZoomComponent
])

const props = defineProps({
  config: {
    type: Object,
    required: true
  }
})

const error = ref(false)
const chartRef = ref(null)

// We want to ensure the configuration is sturdy and aesthetically pleasing.
const mergedConfig = computed(() => {
  error.value = false;
  try {
    // Basic validation
    if (!props.config) return {}
    
    // Inject nice defaults to whatever the LLM returns for a premium look
    return {
      color: [
        '#3b82f6', '#8b5cf6', '#ec4899', '#10b981', 
        '#f59e0b', '#6366f1', '#14b8a6', '#f43f5e',
        '#0ea5e9', '#84cc16', '#a855f7'
      ],
      tooltip: {
        trigger: 'item', // good default; axis trigger commonly added by AI
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e7eb',
        borderWidth: 1,
        textStyle: { color: '#374151' },
        ...props.config.tooltip
      },
      grid: {
        top: 30,
        right: 20,
        bottom: 30,
        left: 40,
        containLabel: true,
        ...props.config.grid
      },
      ...props.config,
      backgroundColor: 'transparent'
    }
  } catch (e) {
    console.error("Chart config mapping error", e)
    error.value = true
    return {}
  }
})

// Deep watch on config changes for edge case errors
watch(() => props.config, (newVal) => {
  if (newVal === null || typeof newVal !== 'object') {
    error.value = true;
  }
}, { deep: true, immediate: true })
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
  min-height: 150px;
}
</style>
