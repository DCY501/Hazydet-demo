<template>
  <div class="compare-page">
    <el-card shadow="never" class="control-card">
      <template #header>
        <span>三模型对比配置</span>
      </template>

      <el-row :gutter="20" align="middle">
        <el-col :xs="24" :md="12">
          <UploadBox v-model="file" @change="handleFileChange" />
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import UploadBox from '@/components/UploadBox.vue'
import ResultCard from '@/components/ResultCard.vue'
import { compareModels } from '@/api/detect'

const file = ref<File | null>(null)
const beta = ref(0)
const loading = ref(false)
const compareResults = ref<Record<string, any>>({})

function handleFileChange(f: File | null) {
  file.value = f
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
</script>

<style scoped lang="scss">
.compare-page {
  .control-card {
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

  .result-row {
    .el-col {
      margin-bottom: 20px;
    }
  }
}
</style>
