"""
文本分块服务模块
处理文本的分块操作
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import asyncio


class TextChunkService:
    def __init__(self):
        self.data_dir = Path("data")
        self.chunks_dir = self.data_dir / "chunks"
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        
        # 分块信息存储文件
        self.chunk_info_path = self.data_dir / "chunk_info.json"
        
        if not self.chunk_info_path.exists():
            self._save_chunk_info([])
    
    def _load_chunk_info(self) -> List[Dict]:
        """加载分块信息"""
        try:
            with open(self.chunk_info_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_chunk_info(self, chunk_info: List[Dict]):
        """保存分块信息"""
        with open(self.chunk_info_path, 'w', encoding='utf-8') as f:
            json.dump(chunk_info, f, ensure_ascii=False, indent=2)
    
    async def process_chunk(self, chunk_method: str, chunk_size: int, overlap_size: int) -> Dict[str, Any]:
        """
        处理文本分块
        
        Args:
            chunk_method: 分块方法 (fixed, semantic, sentence, paragraph)
            chunk_size: 块大小
            overlap_size: 重叠大小
        
        Returns:
            分块结果
        """
        # 模拟分块处理
        chunk_id = str(uuid.uuid4())
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 模拟处理延迟
        await asyncio.sleep(1)
        
        # 模拟分块结果
        chunk_result = {
            "id": chunk_id,
            "method": chunk_method,
            "chunk_size": chunk_size,
            "overlap_size": overlap_size,
            "process_time": current_time,
            "status": "success",
            "total_chunks": 15,
            "chunks": [
                {
                    "id": f"chunk_{i}",
                    "content": f"这是使用{chunk_method}方法生成的第{i+1}个文本块，大小约为{chunk_size}字符。",
                    "start_pos": i * (chunk_size - overlap_size),
                    "end_pos": (i + 1) * chunk_size - overlap_size,
                    "size": len(f"这是使用{chunk_method}方法生成的第{i+1}个文本块，大小约为{chunk_size}字符。")
                }
                for i in range(15)
            ]
        }
        
        # 保存分块信息
        chunk_info_list = self._load_chunk_info()
        chunk_info_list.append(chunk_result)
        self._save_chunk_info(chunk_info_list)
        
        return {
            "chunk_id": chunk_id,
            "status": "success",
            "message": "文本分块成功",
            "total_chunks": 15
        }
    
    async def get_chunk_list(self) -> List[Dict[str, Any]]:
        """获取分块列表"""
        chunk_info_list = self._load_chunk_info()
        
        result = []
        for chunk_info in chunk_info_list:
            result.append({
                "id": chunk_info["id"],
                "method": chunk_info["method"],
                "chunk_size": chunk_info["chunk_size"],
                "overlap_size": chunk_info["overlap_size"],
                "total_chunks": chunk_info["total_chunks"],
                "process_time": chunk_info["process_time"],
                "status": chunk_info["status"]
            })
        
        return result
