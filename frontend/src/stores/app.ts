import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getModels } from '@/api/models'

export interface ModelInfo {
  key: string
  name: string
  description: string
  available: boolean
}

export const useAppStore = defineStore('app', () => {
  const availableModels = ref<ModelInfo[]>([])
  const loading = ref(false)
  const sidebarCollapsed = ref(false)

  // 当前上传的图片，用于跨页面共享
  const currentFile = ref<File | null>(null)
  const currentImageUrl = ref<string>('')

  async function fetchModels(retryCount = 2) {
    for (let i = 0; i <= retryCount; i++) {
      try {
        const res: any = await getModels()
        const models = res.models || {}
        availableModels.value = Object.values(models)
        if (availableModels.value.length > 0) {
          return
        }
      } catch (error) {
        console.error(`获取模型列表失败 (尝试 ${i + 1}/${retryCount + 1})`, error)
        if (i === retryCount) {
          ElMessage.error('获取模型列表失败，请刷新页面重试')
        }
      }
    }
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setCurrentFile(file: File | null) {
    if (currentFile.value && currentImageUrl.value) {
      URL.revokeObjectURL(currentImageUrl.value)
    }
    currentFile.value = file
    currentImageUrl.value = file ? URL.createObjectURL(file) : ''
  }

  function clearCurrentFile() {
    if (currentImageUrl.value) {
      URL.revokeObjectURL(currentImageUrl.value)
    }
    currentFile.value = null
    currentImageUrl.value = ''
  }

  return {
    availableModels,
    loading,
    sidebarCollapsed,
    currentFile,
    currentImageUrl,
    fetchModels,
    toggleSidebar,
    setCurrentFile,
    clearCurrentFile,
  }
})
