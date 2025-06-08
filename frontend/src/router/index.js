import { createRouter, createWebHistory } from 'vue-router'
import DataImportConfig from '@/views/DataImport/Config.vue'
import DataImportManagement from '@/views/DataImport/Management.vue'
import TextChunkConfig from '@/views/TextChunk/Config.vue'
import TextChunkManagement from '@/views/TextChunk/Management.vue'
import VectorEmbedConfig from '@/views/VectorEmbed/Config.vue'
import VectorEmbedManagement from '@/views/VectorEmbed/Management.vue'
import VectorDBConfig from '@/views/VectorDB/Config.vue'
import VectorDBManagement from '@/views/VectorDB/Management.vue'
import RetrievalConfig from '@/views/Retrieval/Config.vue'
import RetrievalManagement from '@/views/Retrieval/Management.vue'
import GenerationConfig from '@/views/Generation/Config.vue'
import GenerationManagement from '@/views/Generation/Management.vue'

const routes = [
  {
    path: '/',
    redirect: '/data-import/config'
  },
  {
    path: '/data-import/config',
    component: DataImportConfig
  },
  {
    path: '/data-import/management',
    component: DataImportManagement
  },
  {
    path: '/text-chunk/config',
    component: TextChunkConfig
  },
  {
    path: '/text-chunk/management',
    component: TextChunkManagement
  },
  {
    path: '/vector-embed/config',
    component: VectorEmbedConfig
  },
  {
    path: '/vector-embed/management',
    component: VectorEmbedManagement
  },
  {
    path: '/vector-db/config',
    component: VectorDBConfig
  },
  {
    path: '/vector-db/management',
    component: VectorDBManagement
  },
  {
    path: '/retrieval/config',
    component: RetrievalConfig
  },
  {
    path: '/retrieval/management',
    component: RetrievalManagement
  },
  {
    path: '/generation/config',
    component: GenerationConfig
  },
  {
    path: '/generation/management',
    component: GenerationManagement
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
