<template>
  <div class="intermediate-page">
    <el-row :gutter="20">
      <el-col :xs="24" :lg="6">
        <el-card shadow="never" class="control-card">
          <template #header>
            <span>中间结果可视化</span>
          </template>

          <el-form label-position="top">
            <el-form-item label="上传图片">
              <UploadBox v-model="file" @change="handleFileChange" />
            </el-form-item>

            <el-form-item label="选择模型">
              <el-select v-model="model" placeholder="请选择" style="width: 100%">
                <el-option label="方案一：AOD-Net 前置去雾" value="phase1" />
                <el-option label="方案二：AFFM + RSM 多任务" value="phase2" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                :disabled="!file"
                @click="handleIntermediate"
                style="width: 100%"
              >
                获取中间结果
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="18">
        <el-card shadow="never" v-loading="loading">
          <template #header>
            <span>可视化结果</span>
          </template>

          <el-empty description="请先上传图片并选择模型" v-if="!intermediateData" />

          <div v-else>
            <ImageCompare :items="compareItems" />

            <div class="intermediate-notes" v-if="model === 'phase2'">
              <el-divider content-position="left">说明</el-divider>
              <el-descriptions :column="1" border>
                <el-descriptions-item label="Ĵ">清晰图像估计（去雾结果）</el-descriptions-item>
                <el-descriptions-item label="t">透射率图</el-descriptions-item>
                <el-descriptions-item label="A">大气光估计</el-descriptions-item>
                <el-descriptions-item label="Reconstruction">重构图</el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import UploadBox from '@/components/UploadBox.vue'
import ImageCompare from '@/components/ImageCompare.vue'
import { getIntermediate } from '@/api/detect'

const file = ref<File | null>(null)
const model = ref('phase2')
const loading = ref(false)
const intermediateData = ref<any>(null)

function handleFileChange(f: File | null) {
  file.value = f
  intermediateData.value = null
}

async function handleIntermediate() {
  if (!file.value) return

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('model', model.value)

  loading.value = true
  try {
    const res: any = await getIntermediate(formData)
    intermediateData.value = res
  } finally {
    loading.value = false
  }
}

const compareItems = computed(() => {
  if (!intermediateData.value) return []
  const d = intermediateData.value
  const inter = d.intermediate || d

  if (model.value === 'phase1') {
    return [
      { label: '原图', url: d.original_url },
      { label: '去雾增强图', url: inter.dehazed_url || inter.dehazed },
      { label: '检测结果', url: d.result_url },
    ].filter((item) => item.url)
  }

  return [
    { label: '原图', url: d.original_url },
    { label: 'Ĵ 清晰图估计', url: inter.jhat_url || inter.jhat || inter.clear_url || inter.clear },
    { label: '透射率 t', url: inter.transmission_url || inter.transmission },
    { label: '大气光 A', url: inter.atmosphere_url || inter.atmosphere },
    { label: '重构图', url: inter.reconstruction_url || inter.reconstruction },
    { label: '检测结果', url: d.result_url },
  ].filter((item) => item.url)
})
</script>

<style scoped lang="scss">
.intermediate-page {
  .control-card {
    margin-bottom: 20px;
  }

  .intermediate-notes {
    margin-top: 24px;
  }
}
</style>
