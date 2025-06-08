<template>
  <div id="app">
    <el-container>
      <!-- 主菜单 -->
      <el-aside width="200px" class="main-sidebar">
        <el-menu
          :default-active="activeMenuItem"
          @select="handleMenuSelect"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          class="full-height-menu"
        >
          <div class="logo">
            <h2>RAG系统</h2>
          </div>
          
          <!-- 数据导入 -->
          <el-sub-menu index="data-import">
            <template #title>
              <el-icon><Upload /></el-icon>
              <span>数据导入</span>
            </template>
            <el-menu-item index="/data-import/config">配置数据导入</el-menu-item>
            <el-menu-item index="/data-import/management">数据导入内容管理</el-menu-item>
          </el-sub-menu>

          <!-- 文本分块 -->
          <el-sub-menu index="text-chunk">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>文本分块</span>
            </template>
            <el-menu-item index="/text-chunk/config">配置文本分块</el-menu-item>
            <el-menu-item index="/text-chunk/management">文本分块内容管理</el-menu-item>
          </el-sub-menu>

          <!-- 向量嵌入 -->
          <el-sub-menu index="vector-embed">
            <template #title>
              <el-icon><Connection /></el-icon>
              <span>向量嵌入</span>
            </template>
            <el-menu-item index="/vector-embed/config">配置向量嵌入</el-menu-item>
            <el-menu-item index="/vector-embed/management">向量嵌入内容管理</el-menu-item>
          </el-sub-menu>

          <!-- 向量数据库 -->
          <el-sub-menu index="vector-db">
            <template #title>
              <el-icon><Coin /></el-icon>
              <span>向量数据库</span>
            </template>
            <el-menu-item index="/vector-db/config">配置向量数据库</el-menu-item>
            <el-menu-item index="/vector-db/management">向量数据库内容管理</el-menu-item>
          </el-sub-menu>

          <!-- 检索 -->
          <el-sub-menu index="retrieval">
            <template #title>
              <el-icon><Search /></el-icon>
              <span>检索</span>
            </template>
            <el-menu-item index="/retrieval/config">配置检索</el-menu-item>
            <el-menu-item index="/retrieval/management">检索内容管理</el-menu-item>
          </el-sub-menu>

          <!-- 内容生成 -->
          <el-sub-menu index="generation">
            <template #title>
              <el-icon><EditPen /></el-icon>
              <span>内容生成</span>
            </template>
            <el-menu-item index="/generation/config">配置内容生成</el-menu-item>
            <el-menu-item index="/generation/management">内容生成内容管理</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <!-- 主内容区域 -->
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Upload, Document, Connection, Coin, 
  Search, EditPen
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const activeMenuItem = ref('/data-import/config')

// 处理菜单选择
const handleMenuSelect = (index) => {
  activeMenuItem.value = index
  router.push(index)
}

// 监听路由变化，更新激活的菜单项
watch(() => route.path, (newPath) => {
  activeMenuItem.value = newPath
}, { immediate: true })
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

.main-sidebar {
  height: 100vh;
  
  .full-height-menu {
    height: 100vh;
    border: none;
    
    .logo {
      padding: 20px;
      text-align: center;
      color: #bfcbd9;
      background-color: #304156;
      border-bottom: 1px solid #434a50;
      
      h2 {
        margin: 0;
        font-size: 18px;
      }
    }
  }
}
</style>
