<template>
  <div class="config-layout">
    <!-- 左侧配置面板 -->
    <div class="config-panel">
      <div class="page-title">配置文本分块</div>
      
      <el-form :model="config" label-width="120px" class="config-form">
        <!-- 分块策略 -->
        <div class="form-section">
          <div class="form-section-title">分块策略</div>
          <el-form-item label="分块方式">
            <el-select 
              v-model="config.chunkStrategy" 
              placeholder="请选择分块方式"
              style="width: 100%"
            >
              <el-option
                value="fixed-size"
                label="固定大小分块"
              >
                <span>固定大小分块</span>
                <span style="float: right; color: #8492a6; font-size: 13px">按固定字符数分块</span>
              </el-option>
              <el-option
                value="semantic"
                label="语义分块"
              >
                <span>语义分块</span>
                <span style="float: right; color: #8492a6; font-size: 13px">按语义边界分块</span>
              </el-option>
              <el-option
                value="paragraph"
                label="段落分块"
              >
                <span>段落分块</span>
                <span style="float: right; color: #8492a6; font-size: 13px">按段落分块</span>
              </el-option>
            </el-select>
          </el-form-item>
        </div>

        <!-- 固定大小分块设置 -->
        <div class="form-section" v-if="config.chunkStrategy === 'fixed-size'">
          <div class="form-section-title">固定大小设置</div>
          <el-form-item label="分块大小">
            <el-input-number
              v-model="config.chunkSize"
              :min="100"
              :max="10000"
              :step="100"
              style="width: 100%"
            />
            <span class="form-tip">字符数，建议500-2000</span>
          </el-form-item>
          <el-form-item label="重叠大小">
            <el-input-number
              v-model="config.overlapSize"
              :min="0"
              :max="500"
              :step="10"
              style="width: 100%"
            />
            <span class="form-tip">重叠字符数，建议50-200</span>
          </el-form-item>
        </div>

        <!-- 语义分块设置 -->
        <div class="form-section" v-if="config.chunkStrategy === 'semantic'">
          <div class="form-section-title">语义分块设置</div>
          <el-form-item label="最小分块">
            <el-input-number
              v-model="config.minChunkSize"
              :min="50"
              :max="1000"
              :step="50"
              style="width: 100%"
            />
            <span class="form-tip">最小分块字符数</span>
          </el-form-item>
          <el-form-item label="最大分块">
            <el-input-number
              v-model="config.maxChunkSize"
              :min="500"
              :max="5000"
              :step="100"
              style="width: 100%"
            />
            <span class="form-tip">最大分块字符数</span>
          </el-form-item>
        </div>

        <!-- 文本预处理 -->
        <div class="form-section">
          <div class="form-section-title">文本预处理</div>
          <el-form-item label="清理选项">
            <el-checkbox-group v-model="config.cleanOptions">
              <el-checkbox label="remove-whitespace">移除多余空白</el-checkbox>
              <el-checkbox label="remove-special-chars">移除特殊字符</el-checkbox>
              <el-checkbox label="normalize-unicode">Unicode标准化</el-checkbox>
              <el-checkbox label="remove-urls">移除URL链接</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </div>

        <!-- 操作按钮 -->
        <div class="form-actions">
          <el-button @click="resetConfig">重置配置</el-button>
          <el-button type="primary" @click="saveConfig">保存配置</el-button>
          <el-button type="success" @click="startChunking">开始分块</el-button>
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
            <p><strong>分块方式:</strong> {{ getStrategyLabel(config.chunkStrategy) }}</p>
            <p v-if="config.chunkStrategy === 'fixed-size'">
              <strong>分块大小:</strong> {{ config.chunkSize }} 字符
            </p>
            <p v-if="config.chunkStrategy === 'fixed-size'">
              <strong>重叠大小:</strong> {{ config.overlapSize }} 字符
            </p>
            <p v-if="config.chunkStrategy === 'semantic'">
              <strong>大小范围:</strong> {{ config.minChunkSize }} - {{ config.maxChunkSize }} 字符
            </p>
            <p><strong>预处理:</strong> {{ config.cleanOptions.length }} 项</p>
          </div>
          
          <h4 style="margin-top: 20px;">预处理选项</h4>
          <div class="clean-options">
            <el-tag 
              v-for="option in config.cleanOptions" 
              :key="option" 
              style="margin: 2px 4px"
              size="small"
            >
              {{ getCleanOptionLabel(option) }}
            </el-tag>
            <span v-if="config.cleanOptions.length === 0" class="no-options">未选择</span>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const config = ref({
  chunkStrategy: 'fixed-size',
  chunkSize: 1000,
  overlapSize: 100,
  minChunkSize: 200,
  maxChunkSize: 2000,
  cleanOptions: ['remove-whitespace', 'normalize-unicode']
})

// 方法
const resetConfig = () => {
  config.value = {
    chunkStrategy: 'fixed-size',
    chunkSize: 1000,
    overlapSize: 100,
    minChunkSize: 200,
    maxChunkSize: 2000,
    cleanOptions: ['remove-whitespace', 'normalize-unicode']
  }
  ElMessage.success('配置已重置')
}

const saveConfig = () => {
  ElMessage.success('配置已保存')
}

const startChunking = () => {
  ElMessage.success('文本分块任务已启动')
}

const getStrategyLabel = (strategy) => {
  const labelMap = {
    'fixed-size': '固定大小分块',
    'semantic': '语义分块',
    'paragraph': '段落分块'
  }
  return labelMap[strategy] || strategy
}

const getCleanOptionLabel = (option) => {
  const labelMap = {
    'remove-whitespace': '移除空白',
    'remove-special-chars': '移除特殊字符',
    'normalize-unicode': 'Unicode标准化',
    'remove-urls': '移除URL'
  }
  return labelMap[option] || option
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

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-left: 8px;
}

.form-actions {
  margin-top: 30px;
  text-align: right;
  
  .el-button {
    margin-left: 10px;
  }
}

.config-preview {
  p {
    margin: 8px 0;
    color: #606266;
    
    strong {
      color: #303133;
    }
  }
}

.clean-options {
  .no-options {
    color: #c0c4cc;
    font-size: 12px;
  }
}

:deep(.el-checkbox-group) {
  .el-checkbox {
    display: block;
    margin-bottom: 8px;
  }
}
</style>
