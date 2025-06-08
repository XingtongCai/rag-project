import api from './index.js'

// 数据导入相关API
export const dataImportAPI = {
  // 上传文件
  uploadFile: (fileType, fileFormat, pdfParser = null) => {
    const params = new URLSearchParams()
    params.append('file_type', fileType)
    params.append('file_format', fileFormat)
    if (pdfParser) {
      params.append('pdf_parser', pdfParser)
    }
    return api.post(`/data-import/upload?${params.toString()}`)
  },
  
  // 获取文件列表
  getFileList: () => {
    return api.get('/data-import/files')
  },
  
  // 删除文件
  deleteFile: (fileId) => {
    return api.delete(`/data-import/files/${fileId}`)
  }
}

export default dataImportAPI
