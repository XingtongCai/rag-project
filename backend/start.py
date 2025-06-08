"""
RAG系统后端启动脚本
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 启动RAG全流程服务系统后端...")
    print("📍 API文档地址: http://localhost:8000/docs")
    print("📍 健康检查: http://localhost:8000/health")
    print("📍 前端地址: http://localhost:3000")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
