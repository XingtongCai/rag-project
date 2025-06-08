"""
RAG全流程服务系统 - 后端主入口
使用FastAPI框架提供RESTful API接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from pathlib import Path

# 导入服务模块
from services.data_import_service import DataImportService
from services.text_chunk_service import TextChunkService
from services.vector_embed_service import VectorEmbedService
from services.vector_db_service import VectorDBService
from services.retrieval_service import RetrievalService
from services.generation_service import GenerationService

# 创建FastAPI应用实例
app = FastAPI(
    title="RAG全流程服务系统",
    description="提供数据导入、文本分块、向量嵌入、向量数据库、检索和生成等完整RAG流程的API服务",
    version="1.0.0"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保data目录存在
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# 初始化服务实例
data_import_service = DataImportService()
text_chunk_service = TextChunkService()
vector_embed_service = VectorEmbedService()
vector_db_service = VectorDBService()
retrieval_service = RetrievalService()
generation_service = GenerationService()

# 根路径
@app.get("/")
async def root():
    return {
        "message": "RAG全流程服务系统API",
        "version": "1.0.0",
        "status": "running"
    }

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ==================== 数据导入相关接口 ====================

@app.post("/api/data-import/upload")
async def upload_file(file_type: str, file_format: str, pdf_parser: str = None):
    """
    上传文件接口
    """
    try:
        result = await data_import_service.upload_file(file_type, file_format, pdf_parser)
        return {"code": 200, "message": "上传成功", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data-import/files")
async def get_file_list():
    """
    获取文件列表接口
    """
    try:
        result = await data_import_service.get_file_list()
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/data-import/files/{file_id}")
async def delete_file(file_id: str):
    """
    删除文件接口
    """
    try:
        result = await data_import_service.delete_file(file_id)
        return {"code": 200, "message": "删除成功", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 文本分块相关接口 ====================

@app.post("/api/text-chunk/process")
async def process_text_chunk(chunk_method: str, chunk_size: int, overlap_size: int):
    """
    文本分块处理接口
    """
    try:
        result = await text_chunk_service.process_chunk(chunk_method, chunk_size, overlap_size)
        return {"code": 200, "message": "分块成功", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/text-chunk/chunks")
async def get_chunk_list():
    """
    获取分块列表接口
    """
    try:
        result = await text_chunk_service.get_chunk_list()
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 向量嵌入相关接口 ====================

@app.post("/api/vector-embed/process")
async def process_vector_embed(embed_model: str, batch_size: int):
    """
    向量嵌入处理接口
    """
    try:
        result = await vector_embed_service.process_embed(embed_model, batch_size)
        return {"code": 200, "message": "嵌入成功", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vector-embed/vectors")
async def get_vector_list():
    """
    获取向量列表接口
    """
    try:
        result = await vector_embed_service.get_vector_list()
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 向量数据库相关接口 ====================

@app.post("/api/vector-db/store")
async def store_vectors(db_type: str, collection_name: str):
    """
    存储向量到数据库接口
    """
    try:
        result = await vector_db_service.store_vectors(db_type, collection_name)
        return {"code": 200, "message": "存储成功", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vector-db/collections")
async def get_collection_list():
    """
    获取集合列表接口
    """
    try:
        result = await vector_db_service.get_collection_list()
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 检索相关接口 ====================

@app.post("/api/retrieval/search")
async def search_vectors(query: str, top_k: int = 5):
    """
    向量检索接口
    """
    try:
        result = await retrieval_service.search(query, top_k)
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/retrieval/history")
async def get_search_history():
    """
    获取检索历史接口
    """
    try:
        result = await retrieval_service.get_search_history()
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 生成相关接口 ====================

@app.post("/api/generation/generate")
async def generate_content(query: str, context: list, model: str = "gpt-3.5-turbo"):
    """
    内容生成接口
    """
    try:
        result = await generation_service.generate(query, context, model)
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/generation/history")
async def get_generation_history():
    """
    获取生成历史接口
    """
    try:
        result = await generation_service.get_generation_history()
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # 启动服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
