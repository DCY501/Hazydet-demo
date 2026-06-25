<template>
  <div class="intermediate-page">
    <el-row :gutter="20">
      <!-- 左侧：上传与原图 -->
      <el-col :xs="24" :lg="6">
        <el-card shadow="never" class="control-card">
          <template #header>
            <span>上传图片</span>
          </template>

          <UploadBox v-model="file" @change="handleFileChange" @clear="handleClear" />
        </el-card>

        <el-card shadow="never" class="original-card" v-if="previewUrl">
          <template #header>
            <span>原图</span>
          </template>
          <el-image :src="previewUrl" fit="contain" class="original-image" />
        </el-card>
      </el-col>

      <!-- 右侧：方案 Tab -->
      <el-col :xs="24" :lg="18">
        <el-card shadow="never" v-loading="loading">
          <template #header>
            <span>中间结果可视化</span>
          </template>

          <el-tabs v-model="activeTab" type="border-card" @tab-change="handleTabChange">
            <el-tab-pane label="方案一：AOD-Net 前置去雾" name="phase1">
              <el-empty description="请先上传图片" v-if="!previewUrl" />
              <div v-else-if="!phase1Data && !loading" class="empty-action">
                <el-button type="primary" @click="loadIntermediate('phase1')">加载方案一中间结果</el-button>
              </div>
              <ImageCompare v-else :items="phase1Items" />
            </el-tab-pane>

            <el-tab-pane label="方案二：AFFM + RSM 多任务" name="phase2">
              <el-empty description="请先上传图片" v-if="!previewUrl" />
              <div v-else-if="!phase2Data && !loading" class="empty-action">
                <el-button type="primary" @click="loadIntermediate('phase2')">加载方案二中间结果</el-button>
              </div>
              <ImageCompare v-else :items="phase2Items" />

              <div class="intermediate-notes" v-if="phase2Data">
                <el-divider content-position="left">说明</el-divider>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="Ĵ">清晰图像估计（去雾结果）</el-descriptions-item>
                  <el-descriptions-item label="t">透射率图</el-descriptions-item>
                  <el-descriptions-item label="A">大气光估计</el-descriptions-item>
                  <el-descriptions-item label="Reconstruction">重构图</el-descriptions-item>
                </el-descriptions>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import UploadBox from '@/components/UploadBox.vue'
import ImageCompare from '@/components/ImageCompare.vue'
import { getIntermediate } from '@/api/detect'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const store = useAppStore()

const file = ref<File | null>(null)
const loading = ref(false)
const activeTab = ref('phase2')
const phase1Data = ref<any>(null)
const phase2Data = ref<any>(null)
const previewUrl = ref('')

function updatePreviewUrl(f: File | null) {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  previewUrl.value = f ? URL.createObjectURL(f) : ''
}

onMounted(() => {
  if (route.query.model && ['phase1', 'phase2'].includes(String(route.query.model))) {
    activeTab.value = String(route.query.model)
  }

  if (store.currentFile) {
    file.value = store.currentFile
    updatePreviewUrl(store.currentFile)
    loadIntermediate(activeTab.value as 'phase1' | 'phase2')
  }
})

function handleFileChange(f: File | null) {
  file.value = f
  updatePreviewUrl(f)
  phase1Data.value = null
  phase2Data.value = null
  if (f) {
    store.setCurrentFile(f)
    loadIntermediate(activeTab.value as 'phase1' | 'phase2')
  }
}

function handleClear() {
  file.value = null
  updatePreviewUrl(null)
  store.clearCurrentFile()
  phase1Data.value = null
  phase2Data.value = null
}

function handleTabChange(tabName: any) {
  if (!file.value) return
  const model = String(tabName) as 'phase1' | 'phase2'
  if (model === 'phase1' && !phase1Data.value) {
    loadIntermediate(model)
  } else if (model === 'phase2' && !phase2Data.value) {
    loadIntermediate(model)
  }
}

async function loadIntermediate(model: 'phase1' | 'phase2') {
  if (!file.value) return

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('model', model)

  loading.value = true
  try {
    const res: any = await getIntermediate(formData)
    if (model === 'phase1') {
      phase1Data.value = res
    } else {
      phase2Data.value = res
    }
  } finally {
    loading.value = false
  }
}

const phase1Items = computed(() => {
  if (!phase1Data.value) return []
  const d = phase1Data.value
  const inter = d.intermediate || d
  return [
    { label: '原图', url: previewUrl.value },
    { label: '去雾增强图', url: inter.dehazed_url || inter.dehazed },
    { label: '检测结果', url: d.result_url },
  ].filter((item) => item.url)
})

const phase2Items = computed(() => {
  if (!phase2Data.value) return []
  const d = phase2Data.value
  const inter = d.intermediate || d
  return [
    { label: '原图', url: previewUrl.value },
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
  .control-card,
  .original-card {
    margin-bottom: 20px;
  }

  .original-image {
    width: 100%;
    min-height: 160px;
    max-height: 320px;
    background: #f8fafc;
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;

    :deep(img) {
      max-width: 100%;
      max-height: 320px;
      height: auto;
      object-fit: contain;
      display: block;
    }
  }

  .empty-action {
    display: flex;
    justify-content: center;
    padding: 40px 0;
  }

  .intermediate-notes {
    margin-top: 24px;
  }
}
</style>
