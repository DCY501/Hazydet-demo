<template>
  <div class="video-page">
    <el-row :gutter="20">
      <!-- 左侧：上传与配置 -->
      <el-col :xs="24" :lg="8">
        <el-card shadow="never" class="control-card">
          <template #header>
            <span>视频检测配置</span>
          </template>

          <el-form label-position="top">
            <el-form-item label="上传视频">
              <div v-if="!file" class="video-upload">
                <el-upload
                  drag
                  action="#"
                  :auto-upload="false"
                  :show-file-list="false"
                  :on-change="handleChange"
                  accept="video/mp4,video/avi,video/mov"
                >
                  <el-icon class="upload-icon"><VideoCamera /></el-icon>
                  <div class="upload-text">
                    <span>点击或拖拽视频到此处</span>
                    <p>支持 MP4 / AVI / MOV</p>
                  </div>
                </el-upload>
              </div>

              <div v-else class="video-preview-card">
                <video :src="previewUrl" controls class="preview-video"></video>
                <div class="preview-info">
                  <span class="file-name">{{ file.name }}</span>
                  <el-button type="primary" :icon="RefreshRight" size="small" @click="handleReupload">重新上传</el-button>
                </div>
              </div>
            </el-form-item>

            <el-form-item label="选择模型">
              <ModelSelector v-model="model" />
            </el-form-item>

            <el-form-item label="跳帧间隔（每 N 帧检测一次）">
              <el-slider v-model="detectInterval" :min="1" :max="5" :step="1" show-stops />
              <div class="hint-text">
                间隔 = {{ detectInterval }}，数值越大速度越快，但框的位置更新越慢
              </div>
            </el-form-item>

            <el-form-item label="GPU Batch 加速">
              <el-switch v-model="useBatch" active-text="开启" inactive-text="关闭" />
              <div class="hint-text" v-if="useBatch">
                开启后会将多帧图片一起送入 GPU 推理，速度更快
              </div>
            </el-form-item>

            <el-form-item label="Batch 大小" v-if="useBatch">
              <el-radio-group v-model="batchSize">
                <el-radio-button :label="2">2</el-radio-button>
                <el-radio-button :label="4">4</el-radio-button>
                <el-radio-button :label="8">8</el-radio-button>
              </el-radio-group>
              <div class="hint-text">
                8GB 显存推荐选 4，速度更快但显存占用更多
              </div>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                :disabled="!file || !model"
                @click="handleVideoDetect"
                style="width: 100%"
              >
                开始视频检测
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 进度条 -->
          <div v-if="loading" class="progress-area">
            <el-progress
              :percentage="progressPercent"
              :status="progressStatus"
              :stroke-width="12"
              striped
              striped-flow
            />
            <p class="progress-text">{{ progressText }}</p>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：处理结果 -->
      <el-col :xs="24" :lg="16">
        <el-card shadow="never" v-loading="loading && !result">
          <template #header>
            <span>处理结果</span>
          </template>

          <el-empty description="请先上传视频并提交" v-if="!result">
            <template #image>
              <el-icon :size="60"><VideoCamera /></el-icon>
            </template>
          </el-empty>

          <div v-else-if="result.success" class="video-result">
            <video :src="result.video_url" controls class="result-video"></video>

            <el-descriptions :column="2" border class="video-metrics">
              <el-descriptions-item label="输出文件">{{ result.filename }}</el-descriptions-item>
              <el-descriptions-item label="总帧数">{{ result.total_frames }}</el-descriptions-item>
              <el-descriptions-item label="FPS">{{ result.fps }}</el-descriptions-item>
              <el-descriptions-item label="分辨率">{{ result.width }} x {{ result.height }}</el-descriptions-item>
              <el-descriptions-item label="跳帧间隔">{{ result.detect_interval }}</el-descriptions-item>
              <el-descriptions-item label="Batch 大小">{{ result.batch_size }}</el-descriptions-item>
              <el-descriptions-item label="处理耗时">{{ result.process_time?.toFixed(2) }}s</el-descriptions-item>
              <el-descriptions-item label="使用模型">{{ result.model }}</el-descriptions-item>
            </el-descriptions>

            <div class="result-actions">
              <el-button type="primary" :icon="Download" @click="downloadResult">下载结果视频</el-button>
            </div>
          </div>

          <div v-else class="error-result">
            <el-alert
              :title="'处理失败: ' + (result.error || '未知错误')"
              type="error"
              :closable="false"
              show-icon
            />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { VideoCamera, RefreshRight, Download } from '@element-plus/icons-vue'
import type { UploadFile } from 'element-plus'
import ModelSelector from '@/components/ModelSelector.vue'

const file = ref<File | null>(null)
const model = ref('baseline')
const detectInterval = ref(2)
const useBatch = ref(false)
const batchSize = ref(4)
const loading = ref(false)
const result = ref<any>(null)
const progressPercent = ref(0)
const progressCurrent = ref(0)
const progressTotal = ref(0)

const previewUrl = computed(() => {
  if (!file.value) return ''
  return URL.createObjectURL(file.value)
})

const progressStatus = computed(() => {
  if (progressPercent.value >= 100) return 'success'
  return ''
})

const progressText = computed(() => {
  if (progressPercent.value <= 0) return '正在初始化...'
  if (progressPercent.value >= 100) return '处理完成，正在保存...'
  return `正在处理第 ${progressCurrent.value}/${progressTotal.value} 帧 (${progressPercent.value}%)`
})

function handleChange(uploadFile: UploadFile) {
  const raw = uploadFile.raw
  if (raw) {
    file.value = raw
    result.value = null
    resetProgress()
  }
}

function handleReupload() {
  file.value = null
  result.value = null
  resetProgress()
}

function resetProgress() {
  progressPercent.value = 0
  progressCurrent.value = 0
  progressTotal.value = 0
}

function getBaseUrl() {
  // 开发环境通过 Vite 代理，生产环境直接访问后端
  return import.meta.env.DEV ? '' : 'http://localhost:8000'
}

async function handleVideoDetect() {
  if (!file.value || !model.value) return

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('model', model.value)
  formData.append('detect_interval', String(detectInterval.value))
  formData.append('use_batch', String(useBatch.value))
  formData.append('batch_size', String(batchSize.value))

  loading.value = true
  resetProgress()
  result.value = null

  try {
    await startVideoStream(formData)
  } catch (error: any) {
    result.value = {
      success: false,
      error: error.message || '请求失败',
    }
    loading.value = false
  }
}

async function startVideoStream(formData: FormData) {
  const response = await fetch(`${getBaseUrl()}/api/video`, {
    method: 'POST',
    body: formData,
  })

  if (!response.body) {
    throw new Error('无法获取响应流')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      const dataLine = line.trim()
      if (!dataLine.startsWith('data:')) continue

      const jsonStr = dataLine.slice(5).trim()
      if (!jsonStr) continue

      try {
        const event = JSON.parse(jsonStr)
        handleStreamEvent(event)
      } catch (e) {
        console.error('解析 SSE 消息失败:', jsonStr)
      }
    }
  }

  // 处理最后可能剩余的数据
  if (buffer.trim()) {
    const dataLine = buffer.trim()
    if (dataLine.startsWith('data:')) {
      const jsonStr = dataLine.slice(5).trim()
      if (jsonStr) {
        try {
          const event = JSON.parse(jsonStr)
          handleStreamEvent(event)
        } catch (e) {
          console.error('解析 SSE 消息失败:', jsonStr)
        }
      }
    }
  }
}

function handleStreamEvent(event: any) {
  if (event.type === 'progress') {
    progressPercent.value = event.percent
    progressCurrent.value = event.current
    progressTotal.value = event.total
  } else if (event.type === 'complete') {
    result.value = { success: true, ...event.result }
    progressPercent.value = 100
    loading.value = false
  } else if (event.type === 'error') {
    result.value = { success: false, error: event.error }
    loading.value = false
  }
}

function downloadResult() {
  if (!result.value?.video_url) return
  const link = document.createElement('a')
  link.href = result.value.video_url
  link.download = result.value.filename || 'result.mp4'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<style scoped lang="scss">
.video-page {
  .control-card {
    margin-bottom: 20px;
  }

  .video-upload {
    width: 100%;

    :deep(.el-upload-dragger) {
      padding: 30px 20px;
      background: #f1f5f9;
      border: 2px dashed #cbd5e1;
      border-radius: 12px;
      transition: all 0.3s;

      &:hover {
        border-color: #38bdf8;
        background: #e0f2fe;
      }
    }
  }

  .upload-icon {
    font-size: 40px;
    color: #64748b;
    margin-bottom: 8px;
  }

  .upload-text {
    span {
      font-size: 15px;
      color: #1e293b;
    }

    p {
      margin-top: 6px;
      font-size: 12px;
      color: #94a3b8;
    }
  }

  .video-preview-card {
    display: flex;
    flex-direction: column;
    gap: 12px;

    .preview-video {
      width: 100%;
      max-height: 240px;
      border-radius: 8px;
      background: #000;
    }

    .preview-info {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;

      .file-name {
        font-size: 13px;
        color: #1e293b;
        word-break: break-all;
      }
    }
  }

  .hint-text {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 4px;
  }

  .progress-area {
    margin-top: 16px;

    .progress-text {
      margin-top: 8px;
      font-size: 13px;
      color: #64748b;
      text-align: center;
    }
  }

  .video-result {
    .result-video {
      width: 100%;
      height: auto;
      max-height: 60vh;
      border-radius: 8px;
      background: #000;
      display: block;
    }

    .video-metrics {
      margin-top: 16px;
    }

    .result-actions {
      margin-top: 16px;
      display: flex;
      justify-content: center;
    }
  }

  .error-result {
    padding: 20px 0;
  }
}
</style>
