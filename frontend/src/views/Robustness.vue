<template>
  <div class="robustness-page">
    <el-card shadow="never" class="control-card">
      <template #header>
        <span>浓度鲁棒性分析</span>
      </template>

      <el-row :gutter="20" align="middle">
        <el-col :xs="24" :md="10">
          <UploadBox v-model="file" @change="handleFileChange" />
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
import { ref, computed } from 'vue'
import UploadBox from '@/components/UploadBox.vue'
import ModelSelector from '@/components/ModelSelector.vue'
import ResultCard from '@/components/ResultCard.vue'
import { detectImage } from '@/api/detect'

const file = ref<File | null>(null)
const model = ref('baseline')
const betaRange = ref([0, 2])
const betaStep = ref(0.5)
const loading = ref(false)
const robustnessResults = ref<any[]>([])

function handleFileChange(f: File | null) {
  file.value = f
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
</script>

<style scoped lang="scss">
.robustness-page {
  .control-card,
  .table-card {
    margin-bottom: 20px;
  }

  .result-row {
    .el-col {
      margin-bottom: 20px;
    }
  }
}
</style>
