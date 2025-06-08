# RAG前端系统 - Vue3 + Vite

基于Vue3和Vite构建的现代化前端框架，用于RAG全流程服务系统。

## 技术栈

- **Vue 3.4+** - 渐进式JavaScript框架
- **Vite 5+** - 下一代前端构建工具
- **Element Plus** - Vue 3组件库
- **Pinia** - Vue状态管理
- **Vue Router 4** - 官方路由
- **Axios** - HTTP客户端
- **Sass** - CSS预处理器

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API接口
│   │   └── index.js       # 统一API管理
│   ├── components/        # 公共组件
│   ├── router/           # 路由配置
│   │   └── index.js      # 路由定义
│   ├── stores/           # 状态管理
│   │   └── index.js      # Pinia stores
│   ├── styles/           # 样式文件
│   │   ├── index.scss    # 全局样式
│   │   ├── variables.scss # 样式变量
│   │   └── mixins.scss   # 样式混合
│   ├── views/            # 页面组件
│   │   ├── Home.vue      # 主页面
│   │   └── DataImport/   # 数据导入页面
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── index.html            # HTML模板
├── vite.config.js        # Vite配置
├── package.json          # 项目配置
└── README.md            # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 3. 构建生产版本

```bash
npm run build
```

### 4. 预览生产版本

```bash
npm run preview
```

## 主要特性

### 🚀 现代化开发体验
- **Vite** 提供极速的热重载和构建
- **Vue 3 Composition API** 更好的逻辑复用
- **TypeScript支持** (可选)

### 🎨 UI组件库
- **Element Plus** 完整的Vue 3组件库
- **自动导入** 组件和API，无需手动引入
- **主题定制** 支持SCSS变量定制

### 📦 状态管理
- **Pinia** 轻量级状态管理
- **模块化设计** 按功能划分store
- **TypeScript友好**

### 🛠 开发工具
- **ESLint** 代码质量检查
- **Sass** CSS预处理器
- **路径别名** @指向src目录

### 📱 响应式设计
- **移动端适配** 响应式布局
- **主题切换** 支持明暗主题
- **国际化准备** i18n结构预留

## 配置说明

### Vite配置 (vite.config.js)

```javascript
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
      imports: ['vue', 'vue-router', 'pinia']
    }),
    Components({
      resolvers: [ElementPlusResolver()]
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

### 路由配置

```javascript
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/data-import',
    name: 'DataImport',
    component: () => import('@/views/DataImport/index.vue')
  }
  // ... 更多路由
]
```

### API配置

```javascript
// 统一的API管理
export const dataImportAPI = {
  uploadFile: (file) => api.post('/data-import/upload', formData),
  getFileList: () => api.get('/data-import/files'),
  deleteFile: (fileId) => api.delete(`/data-import/files/${fileId}`)
}
```

## 开发指南

### 添加新页面

1. 在 `src/views/` 下创建页面组件
2. 在 `src/router/index.js` 中添加路由
3. 在侧边栏菜单中添加导航

### 添加新的API

1. 在 `src/api/index.js` 中添加API方法
2. 在组件中导入并使用

### 状态管理

```javascript
// 定义store
export const useAppStore = defineStore('app', {
  state: () => ({
    loading: false
  }),
  actions: {
    setLoading(status) {
      this.loading = status
    }
  }
})

// 在组件中使用
const appStore = useAppStore()
appStore.setLoading(true)
```

### 样式开发

- 使用SCSS变量：`$primary-color`
- 使用混合：`@include flex-center`
- 响应式：`@include respond-to(md)`

## 部署

### 构建

```bash
npm run build
```

构建产物在 `dist/` 目录下。

### 部署到服务器

将 `dist/` 目录内容部署到Web服务器即可。

### 环境变量

创建 `.env.production` 文件：

```
VITE_API_BASE_URL=https://your-api-domain.com
```

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
