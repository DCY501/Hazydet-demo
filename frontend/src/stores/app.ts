import { defineStore } from 'pinia'
import { ref } from 'vue'
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

  async function fetchModels() {
    try {
      const res: any = await getModels()
      availableModels.value = res.models || []
    } catch (error) {
      console.error('获取模型列表失败', error)
      availableModels.value = []
    }
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return {
    availableModels,
    loading,
    sidebarCollapsed,
    fetchModels,
    toggleSidebar,
  }
})
