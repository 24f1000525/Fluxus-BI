<template>
  <div class="w-full h-full absolute inset-0" ref="chartContainer">
    <div v-if="error" class="absolute inset-0 flex items-center justify-center text-red-500 bg-red-50 rounded-lg text-sm p-4 text-center border-dashed border border-red-200">
      <div class="flex flex-col items-center">
        <svg class="w-8 h-8 opacity-50 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        <span>Invalid Chart Configuration.<br>Please adjust your prompt.</span>
      </div>
    </div>
    <v-chart v-else ref="chartRef" class="w-full h-full absolute inset-0" :option="mergedConfig" autoresize />

    <!-- Sleek HTML-based Fullscreen Modal overlay spanning the entire browser window -->
    <Teleport to="body">
      <div v-if="isFullScreen" class="fixed inset-0 z-[9999] bg-white/95 backdrop-blur-md flex flex-col p-6 sm:p-10 transition-opacity duration-300">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold text-gray-800 tracking-tight">{{ props.config?.title?.text || 'Interactive Chart View' }}</h2>
          <button @click="isFullScreen = false" class="p-2.5 bg-gray-100 hover:bg-red-50 hover:text-red-600 text-gray-700 rounded-full transition shadow-sm border border-gray-200">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        <div class="flex-1 w-full h-full relative bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden p-4">
          <v-chart class="absolute inset-0 w-full h-full" :option="fullScreenConfig" autoresize />
        </div>
      </div>
    </Teleport>
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
  },
  isExporting: {
    type: Boolean,
    default: false
  }
})

const error = ref(false)
const chartRef = ref(null)
const isFullScreen = ref(false)

// We want to ensure the configuration is sturdy and aesthetically pleasing.
const mergedConfig = computed(() => {
  error.value = false;
  try {
    if (!props.config) return {}
    
    // Deep clone config to allow intercepting and modifying dataset structures safely
    const chartConfig = JSON.parse(JSON.stringify(props.config));
    
    // Automatically intercept Pie charts and aggregate their data by category to avoid split slices
    if (chartConfig.series && chartConfig.dataset && Array.isArray(chartConfig.dataset.source)) {
      chartConfig.series.forEach(serie => {
        if (serie.type === 'pie' && serie.encode && serie.encode.itemName && serie.encode.value) {
          const catCol = Array.isArray(serie.encode.itemName) ? serie.encode.itemName[0] : serie.encode.itemName;
          const valCol = Array.isArray(serie.encode.value) ? serie.encode.value[0] : serie.encode.value;
          
          if (catCol && valCol) {
            const aggregated = {};
            chartConfig.dataset.source.forEach(row => {
              const cat = row[catCol] !== undefined ? String(row[catCol]) : 'Unknown';
              const val = parseFloat(row[valCol]) || 0;
              if (!aggregated[cat]) {
                aggregated[cat] = { ...row, [catCol]: cat, [valCol]: 0 };
              }
              aggregated[cat][valCol] += val;
            });
            chartConfig.dataset.source = Object.values(aggregated);
          }
        }
      });
    }

    const isCartesian = chartConfig.xAxis || chartConfig.yAxis;

    // Provide fullscreen capability universally to all charts, 
    // and zoom exclusively to dimension-based charts.
    const customToolbox = props.isExporting ? { show: false } : {
      show: true,
      itemSize: 14,
      right: 15,
      top: 0,
      feature: {
        myFullScreen: {
          show: true,
          title: 'Full Screen',
          icon: 'path://M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z',
          onclick: () => {
            isFullScreen.value = true
          }
        },
        ...(isCartesian ? {
          dataZoom: { yAxisIndex: 'none', title: { zoom: 'Area Zoom', back: 'Restore Zoom' } },
          restore: { title: 'Reset View' }
        } : {})
      }
    };

    const zoomConfig = isCartesian ? {
      dataZoom: [
        { type: 'inside' },
        { type: 'slider', height: 20, bottom: 5 }
      ]
    } : {};
    
    // Inject nice defaults to whatever the LLM returns for a premium look
    return {
      animation: false, // Strongly recommended for bug-free html2canvas PDF exports
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
        ...chartConfig.tooltip
      },
      grid: {
        top: 30,
        right: 20,
        bottom: isCartesian ? 35 : 30, // Need extra space if the slider is present at the bottom
        left: 40,
        containLabel: true,
        ...chartConfig.grid
      },
      toolbox: customToolbox,
      ...zoomConfig,
      ...chartConfig,
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

const fullScreenConfig = computed(() => {
  if (!mergedConfig.value) return {}
  const clone = JSON.parse(JSON.stringify(mergedConfig.value))
  // Deactivate the "Full Screen" button when already in full screen
  if (clone.toolbox && clone.toolbox.feature && clone.toolbox.feature.myFullScreen) {
    clone.toolbox.feature.myFullScreen.show = false
  }
  return clone
})
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
  min-height: 150px;
}
</style>
