<template>
  <div class="compare-page">
    <el-card shadow="never" class="control-card">
      <template #header>
        <span>三模型对比</span>
      </template>

      <el-row :gutter="20" align="middle">
        <el-col :xs="24" :md="12">
          <UploadBox v-model="file" @change="handleFileChange" @clear="handleClear" />
        </el-col>
        <el-col :xs="24" :md="6">
          <div class="beta-control">
            <label>雾浓度 beta</label>
            <el-slider v-model="beta" :min="0" :max="3" :step="0.1" show-stops />
            <span class="beta-value">β = {{ beta }}</span>
          </div>
        </el-col>
        <el-col :xs="24" :md="6">
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            :disabled="!file"
            @click="handleCompare"
            style="width: 100%"
          >
            开始对比
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 原图展示 -->
    <el-card shadow="never" class="original-card" v-if="previewUrl">
      <template #header>
        <span>原图</span>
      </template>
      <el-image :src="previewUrl" fit="contain" class="original-image" />
    </el-card>

    <!-- 三模型结果 -->
    <el-row :gutter="20" class="result-row">
      <el-col :xs="24" :md="8" v-for="item in compareResultList" :key="item.key">
        <ResultCard
          :title="item.name"
          :image-url="item.result_url"
          :model-name="item.name"
          :metrics="item.metrics"
          :detections="item.detections"
          :loading="loading"
        />
      </el-col>
    </el-row>

    <!-- 指标对比图表 -->
    <el-card shadow="never" class="chart-card" v-if="compareResultList.length">
      <template #header>
        <span>指标对比</span>
      </template>

      <el-tabs v-model="activeChartTab">
        <el-tab-pane label="目标数" name="count">
          <v-chart class="chart" :option="countChartOption" autoresize />
        </el-tab-pane>
        <el-tab-pane label="平均置信度" name="confidence">
          <v-chart class="chart" :option="confidenceChartOption" autoresize />
        </el-tab-pane>
        <el-tab-pane label="推理耗时" name="time">
          <v-chart class="chart" :option="timeChartOption" autoresize />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import UploadBox from '@/components/UploadBox.vue'
import ResultCard from '@/components/ResultCard.vue'
import { compareModels } from '@/api/detect'
import { useAppStore } from '@/stores/app'

const store = useAppStore()

const file = ref<File | null>(null)
const beta = ref(0)
const loading = ref(false)
const compareResults = ref<Record<string, any>>({})
const previewUrl = ref('')
const activeChartTab = ref('count')

function updatePreviewUrl(f: File | null) {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  previewUrl.value = f ? URL.createObjectURL(f) : ''
}

onMounted(() => {
  if (store.currentFile) {
    file.value = store.currentFile
    updatePreviewUrl(store.currentFile)
    handleCompare()
  }
})

function handleFileChange(f: File | null) {
  file.value = f
  updatePreviewUrl(f)
  if (f) {
    store.setCurrentFile(f)
  }
  compareResults.value = {}
}

function handleClear() {
  file.value = null
  updatePreviewUrl(null)
  store.clearCurrentFile()
  compareResults.value = {}
}

async function handleCompare() {
  if (!file.value) return

  const formData = new FormData()
  formData.append('file', file.value)
  if (beta.value > 0) {
    formData.append('beta', String(beta.value))
  }

  loading.value = true
  try {
    const res: any = await compareModels(formData)
    compareResults.value = res.results || res || {}
  } finally {
    loading.value = false
  }
}

const compareResultList = computed(() => {
  return Object.entries(compareResults.value).map(([key, value]) => ({
    key,
    ...value,
  }))
})

const chartData = computed(() => {
  const list = compareResultList.value.filter((item) => item.metrics && !item.error)
  return {
    names: list.map((item) => item.name),
    count: list.map((item) => item.metrics.count ?? 0),
    confidence: list.map((item) => ((item.metrics.avg_conf ?? 0) * 100).toFixed(1)),
    time: list.map((item) => item.metrics.inference_ms ?? 0),
  }
})

const baseChartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    type: 'category',
    data: chartData.value.names,
    axisLabel: {
      interval: 0,
      rotate: 15,
    },
  },
  yAxis: {
    type: 'value',
  },
  series: [],
}))

const countChartOption = computed(() => ({
  ...baseChartOption.value,
  title: {
    text: '检出目标数对比',
    left: 'center',
    textStyle: { fontSize: 14, color: '#1e293b' },
  },
  color: ['#3b82f6'],
  series: [
    {
      name: '目标数',
      type: 'bar',
      data: chartData.value.count,
      barWidth: '40%',
      label: {
        show: true,
        position: 'top',
      },
    },
  ],
}))

const confidenceChartOption = computed(() => ({
  ...baseChartOption.value,
  title: {
    text: '平均置信度对比 (%)',
    left: 'center',
    textStyle: { fontSize: 14, color: '#1e293b' },
  },
  color: ['#10b981'],
  series: [
    {
      name: '平均置信度',
      type: 'bar',
      data: chartData.value.confidence,
      barWidth: '40%',
      label: {
        show: true,
        position: 'top',
        formatter: '{c}%',
      },
    },
  ],
}))

const timeChartOption = computed(() => ({
  ...baseChartOption.value,
  title: {
    text: '推理耗时对比 (ms)',
    left: 'center',
    textStyle: { fontSize: 14, color: '#1e293b' },
  },
  color: ['#f59e0b'],
  series: [
    {
      name: '推理耗时',
      type: 'bar',
      data: chartData.value.time,
      barWidth: '40%',
      label: {
        show: true,
        position: 'top',
        formatter: '{c} ms',
      },
    },
  ],
}))
</script>

<style scoped lang="scss">
.compare-page {
  .control-card,
  .original-card,
  .chart-card {
    margin-bottom: 20px;
  }

  .beta-control {
    label {
      display: block;
      font-size: 14px;
      color: #475569;
      margin-bottom: 8px;
    }

    .beta-value {
      font-size: 13px;
      color: #64748b;
    }
  }

  .original-image {
    width: 100%;
    min-height: 200px;
    max-height: 400px;
    background: #f8fafc;
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;

    :deep(img) {
      max-width: 100%;
      max-height: 400px;
      height: auto;
      object-fit: contain;
      display: block;
    }
  }

  .result-row {
    .el-col {
      margin-bottom: 20px;
    }
  }

  .chart {
    width: 100%;
    height: 360px;
  }
}
</style>
