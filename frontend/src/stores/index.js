import { defineStore } from 'pinia'

// 主应用状态管理
export const useAppStore = defineStore('app', {
  state: () => ({
    loading: false,
    sidebarCollapsed: false,
    theme: 'light'
  }),
  
  getters: {
    isLoading: (state) => state.loading,
    isSidebarCollapsed: (state) => state.sidebarCollapsed,
    currentTheme: (state) => state.theme
  },
  
  actions: {
    setLoading(status) {
      this.loading = status
    },
    
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    
    setTheme(theme) {
      this.theme = theme
    }
  }
})

// 数据导入状态管理
export const useDataImportStore = defineStore('dataImport', {
  state: () => ({
    files: [],
    uploadProgress: 0,
    importHistory: []
  }),
  
  actions: {
    addFile(file) {
      this.files.push(file)
    },
    
    removeFile(index) {
      this.files.splice(index, 1)
    },
    
    setUploadProgress(progress) {
      this.uploadProgress = progress
    },
    
    addToHistory(record) {
      this.importHistory.unshift(record)
    }
  }
})
