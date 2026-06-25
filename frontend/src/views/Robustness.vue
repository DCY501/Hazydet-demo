<template>
  <div class="robustness-page">
    <el-card shadow="never" class="control-card">
      <template #header>
        <span>浓度鲁棒性分析</span>
      </template>

      <el-row :gutter="20" align="middle">
        <el-col :xs="24" :md="10">
          <UploadBox v-model="file" @change="handleFileChange" @clear="handleClear" />
        </el-col>
        <el-col :xs="24" :md="8">
          <el-form label-position="top">
            <el-form-item label="选择模型">
              <ModelSelector v-model="model" />
            </el-form-item>
            <el-form-item label="beta 范围">
              <el-slider v-model="betaRange" range :min="0" :max="3" :step="0.1" />
            </el-form-item>
            <el-form-item label="步长">
              <el-input-number v-model="betaStep" :min="0.1" :max="1" :step="0.1" />
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :xs="24" :md="6">
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            :disabled="!file || !model"
            @click="handleRobustness"
            style="width: 100%"
          >
            开始分析
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

    <!-- 目标数随 beta 变化曲线 -->
    <el-card shadow="never" class="chart-card" v-if="robustnessResults.length">
      <template #header>
        <span>目标数随雾浓度变化曲线</span>
      </template>
      <v-chart class="chart" :option="lineChartOption" autoresize />
    </el-card>

    <!-- 结果矩阵 -->
    <el-row :gutter="20" class="result-row">
      <el-col :xs="24" :md="12" v-for="item in robustnessResults" :key="item.beta">
        <ResultCard
          :title="`β = ${item.beta}`"
          :image-url="item.result_url"
          :metrics="item.metrics"
          :detections="item.detections"
          :loading="loading"
        />
      </el-col>
    </el-row>

    <!-- 指标汇总 -->
    <el-card shadow="never" class="table-card" v-if="robustnessResults.length">
      <template #header>
        <span>指标汇总</span>
      </template>
      <el-table :data="robustnessResults" border>
        <el-table-column prop="beta" label="Beta" width="100" />
        <el-table-column prop="metrics.count" label="检出数" />
        <el-table-column prop="metrics.avg_conf" label="平均置信度">
          <template #default="{ row }">
            {{ row.metrics?.avg_conf?.toFixed(4) ?? '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="metrics.inference_ms" label="推理耗时(ms)" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import UploadBox from '@/components/UploadBox.vue'
import ModelSelector from '@/components/ModelSelector.vue'
import ResultCard from '@/components/ResultCard.vue'
import { detectImage } from '@/api/detect'
import { useAppStore } from '@/stores/app'

const store = useAppStore()

const file = ref<File | null>(null)
const model = ref('baseline')
const betaRange = ref([0, 2])
const betaStep = ref(0.5)
const loading = ref(false)
const robustnessResults = ref<any[]>([])
const previewUrl = ref('')

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
  }
})

function handleFileChange(f: File | null) {
  file.value = f
  updatePreviewUrl(f)
  robustnessResults.value = []
  if (f) {
    store.setCurrentFile(f)
  }
}

function handleClear() {
  file.value = null
  updatePreviewUrl(null)
  store.clearCurrentFile()
  robustnessResults.value = []
}

const betaValues = computed(() => {
  const [min, max] = betaRange.value
  const values: number[] = []
  for (let v = min; v <= max + 1e-6; v += betaStep.value) {
    values.push(Math.round(v * 10) / 10)
  }
  return values
})

async function handleRobustness() {
  if (!file.value || !model.value) return

  loading.value = true
  robustnessResults.value = []

  try {
    const results = []
    for (const beta of betaValues.value) {
      const formData = new FormData()
      formData.append('file', file.value)
      formData.append('model', model.value)
      if (beta > 0) {
        formData.append('beta', String(beta))
      }
      const res: any = await detectImage(formData)
      results.push({ beta, ...res })
    }
    robustnessResults.value = results
  } finally {
    loading.value = false
  }
}

const lineChartOption = computed(() => {
  const data = robustnessResults.value
    .filter((item) => item.metrics)
    .map((item) => ({
      beta: item.beta,
      count: item.metrics.count ?? 0,
      confidence: (item.metrics.avg_conf ?? 0) * 100,
    }))

  return {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['检出目标数', '平均置信度 (%)'],
      bottom: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      name: 'Beta',
      data: data.map((item) => item.beta),
    },
    yAxis: [
      {
        type: 'value',
        name: '目标数',
        position: 'left',
      },
      {
        type: 'value',
        name: '置信度 (%)',
        position: 'right',
        min: 0,
        max: 100,
      },
    ],
    series: [
      {
        name: '检出目标数',
        type: 'line',
        data: data.map((item) => item.count),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { color: '#3b82f6', width: 3 },
        itemStyle: { color: '#3b82f6' },
        areaStyle: {
          color: 'rgba(59, 130, 246, 0.1)',
        },
      },
      {
        name: '平均置信度 (%)',
        type: 'line',
        yAxisIndex: 1,
        data: data.map((item) => item.confidence.toFixed(1)),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { color: '#10b981', width: 3 },
        itemStyle: { color: '#10b981' },
      },
    ],
  }
})
</script>

<style scoped lang="scss">
.robustness-page {
  .control-card,
  .original-card,
  .chart-card,
  .table-card {
    margin-bottom: 20px;
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

  .chart {
    width: 100%;
    height: 400px;
  }

  .result-row {
    .el-col {
      margin-bottom: 20px;
    }
  }
}
</style>
