<template>
  <div class="config-layout">
    <!-- 左侧配置面板 -->
    <div class="config-panel">
      <div class="page-title">配置数据导入</div>
      
      <el-form :model="config" label-width="120px" class="config-form">
        <!-- 文件类型选择 -->
        <div class="form-section">
          <div class="form-section-title">文件类型</div>
          <el-form-item label="数据类型">
            <el-select 
              v-model="config.fileType" 
              placeholder="请选择文件类型"
              @change="handleFileTypeChange"
              style="width: 100%"
            >
              <el-option
                value="structured"
                label="结构化数据"
              >
                <span>结构化数据</span>
                <span style="float: right; color: #8492a6; font-size: 13px">表格化数据，有明确的行列结构</span>
              </el-option>
              <el-option
                value="semi-structured"
                label="半结构化数据"
              >
                <span>半结构化数据</span>
                <span style="float: right; color: #8492a6; font-size: 13px">有一定格式但不完全规范</span>
              </el-option>
              <el-option
                value="unstructured"
                label="非结构化数据"
              >
                <span>非结构化数据</span>
                <span style="float: right; color: #8492a6; font-size: 13px">自由格式文本</span>
              </el-option>
            </el-select>
          </el-form-item>
        </div>

        <!-- 文件格式选择 -->
        <div class="form-section" v-if="availableFormats.length > 0">
          <div class="form-section-title">文件格式</div>
          <el-form-item label="格式类型">
            <el-select 
              v-model="config.fileFormat" 
              placeholder="请选择文件格式"
              style="width: 100%"
            >
              <el-option
                v-for="format in availableFormats"
                :key="format.value"
                :value="format.value"
                :label="format.label"
              />
            </el-select>
          </el-form-item>
        </div>

        <!-- PDF高级设置 -->
        <div class="form-section" v-if="showPdfSettings">
          <div class="form-section-title">PDF高级设置</div>
          <el-form-item label="解析器">
            <el-select 
              v-model="config.pdfParser" 
              placeholder="请选择PDF解析器"
              style="width: 100%"
            >
              <el-option
                value="PyPDF"
                label="PyPDF"
              >
                <span>PyPDF</span>
                <span style="float: right; color: #8492a6; font-size: 13px">轻量级解析器，适合简单PDF</span>
              </el-option>
              <el-option
                value="PyMuPDF"
                label="PyMuPDF"
              >
                <span>PyMuPDF</span>
                <span style="float: right; color: #8492a6; font-size: 13px">功能强大，支持复杂布局和图像提取</span>
              </el-option>
            </el-select>
          </el-form-item>
        </div>

        <!-- 文件上传 -->
        <div class="form-section">
          <div class="form-section-title">文件上传</div>
          <el-form-item>
            <el-upload
              class="upload-demo"
              drag
              :action="uploadAction"
              :before-upload="beforeUpload"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :show-file-list="false"
              :disabled="!canUpload"
            >
              <div class="upload-area">
                <el-icon class="upload-icon"><Upload /></el-icon>
                <div class="upload-text">
                  <p>将文件拖到此处，或<em>点击上传</em></p>
                  <p class="upload-tip">{{ uploadTip }}</p>
                </div>
              </div>
            </el-upload>
          </el-form-item>
        </div>

        <!-- 操作按钮 -->
        <div class="form-actions">
          <el-button @click="resetConfig">重置配置</el-button>
          <el-button type="primary" @click="saveConfig">保存配置</el-button>
        </div>
      </el-form>
    </div>

    <!-- 右侧结果展示面板 -->
    <div class="result-panel">
      <div class="panel-title">配置预览</div>
      <div class="result-content">
        <el-card>
          <h4>当前配置</h4>
          <div class="config-preview">
            <p><strong>数据类型:</strong> {{ getFileTypeLabel(config.fileType) }}</p>
            <p><strong>文件格式:</strong> {{ getFileFormatLabel(config.fileFormat) }}</p>
            <p v-if="showPdfSettings"><strong>PDF解析器:</strong> {{ config.pdfParser }}</p>
          </div>
          
          <h4 style="margin-top: 20px;">支持的文件类型</h4>
          <div class="supported-types">
            <el-tag 
              v-for="type in getAllowedFileTypes()" 
              :key="type" 
              style="margin: 2px 4px"
            >
              .{{ type }}
            </el-tag>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'

// 响应式数据
const config = ref({
  fileType: 'structured',
  fileFormat: '',
  pdfParser: 'PyPDF'
})

// 计算属性
const availableFormats = computed(() => {
  const formatMap = {
    structured: [
      { value: 'excel', label: 'Excel (.xlsx, .xls)' },
      { value: 'txt', label: 'CSV/TXT (.csv, .txt)' }
    ],
    'semi-structured': [
      { value: 'markdown', label: 'Markdown (.md)' },
      { value: 'word', label: 'Word (.docx, .doc)' }
    ],
    unstructured: [
      { value: 'pdf', label: 'PDF (.pdf)' },
      { value: 'txt', label: 'TXT (.txt)' }
    ]
  }
  return formatMap[config.value.fileType] || []
})

const showPdfSettings = computed(() => {
  return config.value.fileFormat === 'pdf'
})

const uploadAction = computed(() => {
  return '/api/data-import/upload'
})

const canUpload = computed(() => {
  return config.value.fileType && config.value.fileFormat
})

const uploadTip = computed(() => {
  if (!config.value.fileType) {
    return '请先选择数据类型'
  }
  if (!config.value.fileFormat) {
    return '请先选择文件格式'
  }
  const formatMap = {
    excel: '支持 .xlsx, .xls 格式',
    txt: '支持 .txt, .csv 格式',
    markdown: '支持 .md 格式',
    pdf: '支持 .pdf 格式',
    word: '支持 .docx, .doc 格式'
  }
  return formatMap[config.value.fileFormat] || '请选择支持的文件格式'
})

// 方法
const handleFileTypeChange = (value) => {
  config.value.fileFormat = ''
}

const beforeUpload = (file) => {
  // 验证文件类型
  const allowedTypes = getAllowedFileTypes()
  const fileExtension = file.name.split('.').pop().toLowerCase()
  
  if (!allowedTypes.includes(fileExtension)) {
    ElMessage.error(`不支持的文件类型: .${fileExtension}`)
    return false
  }
  
  // 验证文件大小 (50MB)
  const isLt50M = file.size / 1024 / 1024 < 50
  if (!isLt50M) {
    ElMessage.error('文件大小不能超过 50MB!')
    return false
  }
  
  return true
}

const handleUploadSuccess = (response, file) => {
  if (response.code === 200) {
    ElMessage.success('文件上传成功!')
  } else {
    ElMessage.error(response.message || '文件上传失败')
  }
}

const handleUploadError = (error) => {
  console.error('Upload error:', error)
  ElMessage.error('文件上传失败，请重试')
}

const getAllowedFileTypes = () => {
  const typeMap = {
    excel: ['xlsx', 'xls'],
    txt: ['txt', 'csv'],
    markdown: ['md'],
    pdf: ['pdf'],
    word: ['docx', 'doc']
  }
  return typeMap[config.value.fileFormat] || []
}

const resetConfig = () => {
  config.value = {
    fileType: 'structured',
    fileFormat: '',
    pdfParser: 'PyPDF'
  }
  ElMessage.success('配置已重置')
}

const saveConfig = () => {
  ElMessage.success('配置已保存')
}

const getFileTypeLabel = (type) => {
  const labelMap = {
    structured: '结构化数据',
    'semi-structured': '半结构化数据',
    unstructured: '非结构化数据'
  }
  return labelMap[type] || type
}

const getFileFormatLabel = (format) => {
  const labelMap = {
    excel: 'Excel',
    txt: 'TXT/CSV',
    markdown: 'Markdown',
    pdf: 'PDF',
    word: 'Word'
  }
  return labelMap[format] || format || '未选择'
}
</script>

<style lang="scss" scoped>
.config-layout {
  display: flex;
  height: 100%;
  gap: 20px;
}

.config-panel {
  flex: 1;
  min-width: 400px;
}

.result-panel {
  width: 300px;
  border-left: 1px solid #e4e7ed;
  padding-left: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.form-section {
  margin-bottom: 24px;
  
  .form-section-title {
    font-size: 14px;
    font-weight: 600;
    color: #606266;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #f0f0f0;
  }
}

.config-form {
  max-width: 100%;
}

.form-actions {
  margin-top: 30px;
  text-align: right;
  
  .el-button {
    margin-left: 10px;
  }
}

.upload-demo {
  width: 100%;
  
  .upload-area {
    padding: 40px 20px;
    text-align: center;
    
    .upload-icon {
      font-size: 48px;
      color: #c0c4cc;
      margin-bottom: 16px;
    }
    
    .upload-text {
      p {
        margin: 8px 0;
        color: #606266;
        
        em {
          color: #409EFF;
          font-style: normal;
        }
      }
      
      .upload-tip {
        color: #909399;
        font-size: 12px;
      }
    }
  }
}

.result-content {
  .config-preview {
    p {
      margin: 8px 0;
      color: #606266;
      
      strong {
        color: #303133;
      }
    }
  }
  
  .supported-types {
    margin-top: 8px;
  }
}

:deep(.el-select-dropdown__item) {
  height: auto;
  line-height: 1.5;
  padding: 12px 20px;
  
  span:last-child {
    display: block;
    margin-top: 4px;
  }
}
</style>
