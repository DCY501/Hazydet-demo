<template>
  <div class="detect-page">
    <el-row :gutter="20">
      <!-- 左侧：上传与配置 -->
      <el-col :xs="24" :lg="8">
        <el-card shadow="never" class="control-card">
          <template #header>
            <span>上传图片</span>
          </template>

          <UploadBox v-model="file" @change="handleFileChange" @clear="handleClear" />
        </el-card>

        <el-card shadow="never" class="control-card" v-if="file">
          <template #header>
            <span>检测配置</span>
          </template>

          <el-form label-position="top">
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

      <!-- 右侧：结果展示 -->
      <el-col :xs="24" :lg="16">
        <!-- 原图与结果图并排 -->
        <el-card shadow="never" class="result-card" v-loading="loading">
          <template #header>
            <span>检测结果</span>
            <el-tag v-if="resultModelName" type="primary" size="small" effect="light">{{ resultModelName }}</el-tag>
          </template>

          <el-empty description="请先上传图片并开始检测" v-if="!resultUrl">
            <template #image>
              <el-icon :size="60"><Picture /></el-icon>
            </template>
          </el-empty>

          <div v-else class="image-comparison">
            <div class="image-block">
              <div class="image-label">原图</div>
              <el-image :src="previewUrl" fit="contain" class="result-image" :preview-src-list="[previewUrl, resultUrl]" />
            </div>
            <div class="image-block">
              <div class="image-label">检测结果</div>
              <el-image :src="resultUrl" fit="contain" class="result-image" :preview-src-list="[previewUrl, resultUrl]" />
            </div>
          </div>

          <div class="metrics" v-if="metrics">
            <el-descriptions :column="3" size="small" border>
              <el-descriptions-item label="检出目标">{{ metrics.count ?? 0 }}</el-descriptions-item>
              <el-descriptions-item label="平均置信度">{{ metrics.avg_conf?.toFixed(3) ?? '-' }}</el-descriptions-item>
              <el-descriptions-item label="推理耗时">{{ metrics.inference_ms ? `${metrics.inference_ms}ms` : '-' }}</el-descriptions-item>
            </el-descriptions>
          </div>

          <div class="detections" v-if="detections && detections.length">
            <el-divider content-position="left">检测详情</el-divider>
            <el-table :data="detections" size="small" max-height="200">
              <el-table-column prop="class_name" label="类别" width="120" />
              <el-table-column prop="confidence" label="置信度" width="120">
                <template #default="{ row }">
                  <el-progress :percentage="Math.round(row.confidence * 100)" :stroke-width="8" />
                </template>
              </el-table-column>
              <el-table-column prop="bbox" label="边界框" />
            </el-table>
          </div>
        </el-card>

        <!-- 功能跳转按钮 -->
        <el-card shadow="never" class="action-card" v-if="resultUrl">
          <template #header>
            <span>更多分析</span>
          </template>

          <el-row :gutter="12">
            <el-col :xs="24" :sm="12" :md="6">
              <el-button type="primary" size="large" plain style="width: 100%" @click="goCompare">
                <el-icon><Grid /></el-icon> 三模型对比
              </el-button>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <el-button type="success" size="large" plain style="width: 100%" @click="goIntermediate('phase1')">
                <el-icon><Share /></el-icon> 方案一中间结果
              </el-button>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <el-button type="warning" size="large" plain style="width: 100%" @click="goIntermediate('phase2')">
                <el-icon><Share /></el-icon> 方案二中间结果
              </el-button>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
              <el-button type="info" size="large" plain style="width: 100%" @click="goRobustness">
                <el-icon><Histogram /></el-icon> 浓度鲁棒性
              </el-button>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Picture, Grid, Share, Histogram } from '@element-plus/icons-vue'
import UploadBox from '@/components/UploadBox.vue'
import ModelSelector from '@/components/ModelSelector.vue'
import { detectImage } from '@/api/detect'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const store = useAppStore()

const file = ref<File | null>(store.currentFile)
const model = ref('baseline')
const beta = ref(0)
const loading = ref(false)

const resultUrl = ref('')
const resultModelName = ref('')
const metrics = ref<any>(null)
const detections = ref<any[]>([])
const previewUrl = ref('')

function updatePreviewUrl(f: File | null) {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  previewUrl.value = f ? URL.createObjectURL(f) : ''
}

// 同步 store 中的文件
watch(
  () => store.currentFile,
  (storeFile) => {
    if (storeFile && storeFile !== file.value) {
      file.value = storeFile
      updatePreviewUrl(storeFile)
    }
  },
  { immediate: true }
)

function handleFileChange(f: File | null) {
  file.value = f
  updatePreviewUrl(f)
  store.setCurrentFile(f)
  resultUrl.value = ''
  metrics.value = null
  detections.value = []
}

function handleClear() {
  file.value = null
  updatePreviewUrl(null)
  store.clearCurrentFile()
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

function goCompare() {
  if (file.value) {
    store.setCurrentFile(file.value)
  }
  router.push('/compare')
}

function goIntermediate(targetModel: string) {
  if (file.value) {
    store.setCurrentFile(file.value)
  }
  router.push({
    path: '/intermediate',
    query: { model: targetModel },
  })
}

function goRobustness() {
  if (file.value) {
    store.setCurrentFile(file.value)
  }
  router.push('/robustness')
}
</script>

<style scoped lang="scss">
.detect-page {
  .control-card,
  .result-card,
  .action-card {
    margin-bottom: 20px;
  }

  .beta-hint {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 4px;
  }

  .image-comparison {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;

    .image-block {
      flex: 1;
      min-width: 280px;
      display: flex;
      flex-direction: column;
      gap: 8px;

      .image-label {
        font-size: 14px;
        font-weight: 600;
        color: #334155;
        text-align: center;
      }

      .result-image {
        width: 100%;
        min-height: 200px;
        max-height: 480px;
        background: #f8fafc;
        border-radius: 8px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;

        :deep(img) {
          max-width: 100%;
          max-height: 480px;
          height: auto;
          object-fit: contain;
          display: block;
        }
      }
    }
  }

  .metrics {
    margin-top: 16px;
  }

  .detections {
    margin-top: 16px;
  }

  .action-card {
    .el-button {
      margin-bottom: 12px;
    }
  }
}
</style>
