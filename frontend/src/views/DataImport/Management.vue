<template>
  <div class="data-import-management">
    <div class="page-title">数据导入内容管理</div>
    
    <!-- 搜索和操作栏 -->
    <div class="toolbar">
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索文件名"
          :prefix-icon="Search"
          style="width: 300px"
          @input="handleSearch"
        />
        <el-select
          v-model="filterType"
          placeholder="文件类型"
          style="width: 150px; margin-left: 10px"
          @change="handleFilter"
        >
          <el-option label="全部" value="" />
          <el-option label="Excel" value="excel" />
          <el-option label="TXT" value="txt" />
          <el-option label="Markdown" value="markdown" />
          <el-option label="PDF" value="pdf" />
          <el-option label="Word" value="word" />
        </el-select>
      </div>
      <div class="actions">
        <el-button @click="refreshList" :icon="Refresh">刷新</el-button>
        <el-button 
          type="danger" 
          :disabled="selectedFiles.length === 0"
          @click="handleBatchDelete"
        >
          批量删除 ({{ selectedFiles.length }})
        </el-button>
      </div>
    </div>

    <!-- 文件列表表格 -->
    <el-table
      :data="filteredFileList"
      v-loading="loading"
      @selection-change="handleSelectionChange"
      class="data-table"
    >
      <el-table-column type="selection" width="55" />
      
      <el-table-column prop="name" label="文件名称" min-width="200">
        <template #default="{ row }">
          <div class="file-info">
            <el-icon style="margin-right: 8px"><component :is="getFileIcon(row.type)" /></el-icon>
            <span>{{ row.name }}</span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="size" label="文件大小" width="120">
        <template #default="{ row }">
          {{ formatFileSize(row.size) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="type" label="文件类型" width="120">
        <template #default="{ row }">
          <el-tag :type="getTypeTagType(row.type)" size="small">
            {{ getTypeLabel(row.type) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="uploadTime" label="上传时间" width="180">
        <template #default="{ row }">
          {{ formatTime(row.uploadTime) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="status" label="处理状态" width="120">
        <template #default="{ row }">
          <el-tag 
            :type="getStatusTagType(row.status)" 
            size="small"
          >
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button 
            size="small" 
            @click="handlePreview(row)"
            :disabled="row.status !== 'success'"
          >
            预览
          </el-button>
          <el-button 
            size="small" 
            type="primary"
            @click="handleReprocess(row)"
            :disabled="row.status === 'processing'"
          >
            重新处理
          </el-button>
          <el-button 
            size="small" 
            type="danger" 
            @click="handleDelete(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      />
    </div>

    <!-- 预览对话框 -->
    <el-dialog
      title="文件预览"
      v-model="previewVisible"
      width="60%"
      :before-close="handleClosePreview"
    >
      <div class="preview-content">
        <div v-if="previewLoading" class="preview-loading">
          <div v-loading="true" element-loading-text="加载中..." style="height: 300px;"></div>
        </div>
        <div v-else-if="previewData" class="preview-data">
          <pre>{{ previewData }}</pre>
        </div>
        <div v-else class="preview-empty">
          <p>暂无预览数据</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Document, DocumentCopy, EditPen } from '@element-plus/icons-vue'

// 响应式数据
const searchKeyword = ref('')
const filterType = ref('')
const selectedFiles = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const previewVisible = ref(false)
const previewLoading = ref(false)
const previewData = ref(null)

// 模拟数据
const mockFileList = ref([
  {
    id: 1,
    name: 'sample_data.xlsx',
    size: 1024000,
    type: 'excel',
    uploadTime: '2024-01-15 10:30:00',
    status: 'success'
  },
  {
    id: 2,
    name: 'document.pdf',
    size: 2048000,
    type: 'pdf',
    uploadTime: '2024-01-15 11:15:00',
    status: 'processing'
  },
  {
    id: 3,
    name: 'readme.md',
    size: 5120,
    type: 'markdown',
    uploadTime: '2024-01-15 12:00:00',
    status: 'error'
  }
])

// 计算属性
const filteredFileList = computed(() => {
  let list = mockFileList.value
  
  // 搜索过滤
  if (searchKeyword.value) {
    list = list.filter(file => 
      file.name.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  
  // 类型过滤
  if (filterType.value) {
    list = list.filter(file => file.type === filterType.value)
  }
  
  // 分页
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  total.value = list.length
  
  return list.slice(start, end)
})

// 生命周期
onMounted(() => {
  fetchFileList()
})

// 方法
const fetchFileList = async () => {
  loading.value = true
  try {
    // 模拟加载延迟
    await new Promise(resolve => setTimeout(resolve, 500))
  } catch (error) {
    ElMessage.error('获取文件列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleFilter = () => {
  currentPage.value = 1
}

const refreshList = () => {
  fetchFileList()
}

const handleSelectionChange = (selection) => {
  selectedFiles.value = selection
}

const handleBatchDelete = async () => {
  if (selectedFiles.value.length === 0) return
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedFiles.value.length} 个文件吗？`,
      '批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    ElMessage.success('批量删除成功')
    fetchFileList()
  } catch {
    // 用户取消
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文件 "${row.name}" 吗？`,
      '删除文件',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    ElMessage.success('删除成功')
    fetchFileList()
  } catch {
    // 用户取消
  }
}

const handlePreview = async (row) => {
  previewVisible.value = true
  previewLoading.value = true
  previewData.value = null
  
  try {
    // 模拟获取预览数据
    await new Promise(resolve => setTimeout(resolve, 1000))
    previewData.value = `文件名: ${row.name}\n文件大小: ${formatFileSize(row.size)}\n上传时间: ${row.uploadTime}\n\n这里是文件的预览内容...`
  } catch (error) {
    ElMessage.error('获取预览数据失败')
  } finally {
    previewLoading.value = false
  }
}

const handleReprocess = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要重新处理文件 "${row.name}" 吗？`,
      '重新处理',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    
    ElMessage.success('已提交重新处理请求')
  } catch {
    // 用户取消
  }
}

const handleClosePreview = () => {
  previewVisible.value = false
  previewData.value = null
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val) => {
  currentPage.value = val
}

// 工具方法
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatTime = (timeStr) => {
  return timeStr
}

const getFileIcon = (type) => {
  const iconMap = {
    excel: Document,
    txt: DocumentCopy,
    markdown: EditPen,
    pdf: Document,
    word: Document
  }
  return iconMap[type] || Document
}

const getTypeLabel = (type) => {
  const labelMap = {
    excel: 'Excel',
    txt: 'TXT',
    markdown: 'Markdown',
    pdf: 'PDF',
    word: 'Word'
  }
  return labelMap[type] || type
}

const getTypeTagType = (type) => {
  const typeMap = {
    excel: 'success',
    txt: 'info',
    markdown: 'warning',
    pdf: 'danger',
    word: 'primary'
  }
  return typeMap[type] || ''
}

const getStatusLabel = (status) => {
  const labelMap = {
    success: '处理成功',
    processing: '处理中',
    error: '处理失败',
    pending: '等待处理'
  }
  return labelMap[status] || status
}

const getStatusTagType = (status) => {
  const typeMap = {
    success: 'success',
    processing: 'warning',
    error: 'danger',
    pending: 'info'
  }
  return typeMap[status] || ''
}
</script>

<style lang="scss" scoped>
.data-import-management {
  height: 100%;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.search-bar {
  display: flex;
  align-items: center;
}

.actions {
  display: flex;
  gap: 10px;
}

.file-info {
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.preview-content {
  min-height: 300px;
}

.preview-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}

.preview-data pre {
  background-color: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 400px;
  overflow-y: auto;
}

.preview-empty {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  color: #909399;
}
</style>
