<template>
  <div class="upload-box-wrapper">
    <div v-if="!currentFile" class="upload-area">
      <el-upload
        class="upload-box"
        drag
        action="#"
        :auto-upload="false"
        :show-file-list="false"
        :on-change="handleChange"
        accept="image/*,video/*"
      >
        <el-icon class="upload-icon"><Upload /></el-icon>
        <div class="upload-text">
          <span class="primary">点击或拖拽文件到此处上传</span>
          <p class="secondary">支持图片（JPG / PNG）或视频（MP4）</p>
        </div>
      </el-upload>
    </div>

    <div v-else class="preview-area">
      <el-image
        v-if="isImage"
        :src="previewUrl"
        fit="contain"
        class="preview-image"
        :preview-src-list="[previewUrl]"
      />
      <div v-else class="video-preview">
        <el-icon :size="48"><VideoCamera /></el-icon>
        <span class="file-name">{{ currentFile.name }}</span>
      </div>
      <div class="preview-actions">
        <el-button type="primary" :icon="RefreshRight" @click="handleReupload">
          重新上传
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Upload, VideoCamera, RefreshRight } from '@element-plus/icons-vue'
import type { UploadFile } from 'element-plus'

const props = defineProps<{
  modelValue?: File | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', file: File | null): void
  (e: 'change', file: File | null): void
  (e: 'clear'): void
}>()

const currentFile = computed({
  get: () => props.modelValue || null,
  set: (val: File | null) => emit('update:modelValue', val),
})

const isImage = computed(() => {
  if (!currentFile.value) return false
  return currentFile.value.type.startsWith('image/')
})

const previewUrl = computed(() => {
  if (!currentFile.value) return ''
  return URL.createObjectURL(currentFile.value)
})

function handleChange(uploadFile: UploadFile) {
  const raw = uploadFile.raw
  if (raw) {
    currentFile.value = raw
    emit('change', raw)
  }
}

function handleReupload() {
  currentFile.value = null
  emit('clear')
}
</script>

<style scoped lang="scss">
.upload-box-wrapper {
  width: 100%;
}

.upload-area {
  width: 100%;
}

.upload-box {
  width: 100%;

  :deep(.el-upload-dragger) {
    padding: 40px 20px;
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
  font-size: 48px;
  color: #64748b;
  margin-bottom: 12px;
}

.upload-text {
  .primary {
    font-size: 16px;
    color: #1e293b;
    font-weight: 500;
  }

  .secondary {
    margin: 8px 0 0;
    font-size: 13px;
    color: #94a3b8;
  }
}

.preview-area {
  position: relative;
  width: 100%;
  min-height: 240px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.preview-image {
  width: 100%;
  max-height: 360px;
  height: auto;
  border-radius: 8px;
  object-fit: contain;
  display: block;
}

.video-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #64748b;
  padding: 40px 20px;

  .file-name {
    font-size: 14px;
    color: #1e293b;
    word-break: break-all;
    text-align: center;
  }
}

.preview-actions {
  margin-top: 16px;
}
</style>
