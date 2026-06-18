<template>
  <div class="detect-page">
    <el-row :gutter="20">
      <el-col :xs="24" :lg="8">
        <el-card shadow="never" class="control-card">
          <template #header>
            <span>检测配置</span>
          </template>

          <el-form label-position="top">
            <el-form-item label="上传图片">
              <UploadBox v-model="file" @change="handleFileChange" />
            </el-form-item>

            <el-form-item label="选择模型">
              <ModelSelector v-model="model" />
            </el-form-item>

            <el-form-item label="雾浓度 beta（可选）">
              <el-slider v-model="beta" :min="0" :max="3" :step="0.1" show-stops />
              <div class="beta-hint">β = {{ beta }}，设为 0 表示不加雾</div>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                :disabled="!file || !model"
                @click="handleDetect"
                style="width: 100%"
              >
                开始检测
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="16">
        <ResultCard
          title="检测结果"
          :image-url="resultUrl"
          :model-name="resultModelName"
          :metrics="metrics"
          :detections="detections"
          :loading="loading"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import UploadBox from '@/components/UploadBox.vue'
import ModelSelector from '@/components/ModelSelector.vue'
import ResultCard from '@/components/ResultCard.vue'
import { detectImage } from '@/api/detect'
import { useAppStore } from '@/stores/app'

const store = useAppStore()

const file = ref<File | null>(null)
const model = ref('baseline')
const beta = ref(0)
const loading = ref(false)

const resultUrl = ref('')
const resultModelName = ref('')
const metrics = ref<any>(null)
const detections = ref<any[]>([])

function handleFileChange(f: File | null) {
  file.value = f
  resultUrl.value = ''
  metrics.value = null
  detections.value = []
}

async function handleDetect() {
  if (!file.value || !model.value) return

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('model', model.value)
  if (beta.value > 0) {
    formData.append('beta', String(beta.value))
  }

  loading.value = true
  try {
    const res: any = await detectImage(formData)
    resultUrl.value = res.result_url
    resultModelName.value = store.availableModels.find((m) => m.key === model.value)?.name || model.value
    metrics.value = res.metrics
    detections.value = res.detections || []
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.detect-page {
  .control-card {
    margin-bottom: 20px;
  }

  .beta-hint {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 4px;
  }
}
</style>
