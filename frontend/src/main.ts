import { createApp } from 'vue'
import { createPinia } from 'pinia'
import VueECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  ToolboxComponent,
  DataZoomComponent,
} from 'echarts/components'
import App from './App.vue'
import router from './router'

import '@/assets/styles/main.scss'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  ToolboxComponent,
  DataZoomComponent,
])

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.component('VChart', VueECharts)
app.mount('#app')
