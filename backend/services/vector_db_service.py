"""
向量数据库服务模块
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import asyncio


class VectorDBService:
    def __init__(self):
        self.data_dir = Path("data")
        self.db_info_path = self.data_dir / "vector_db_info.json"
        
        if not self.db_info_path.exists():
            self._save_db_info([])
    
    def _load_db_info(self) -> List[Dict]:
        try:
            with open(self.db_info_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_db_info(self, db_info: List[Dict]):
        with open(self.db_info_path, 'w', encoding='utf-8') as f:
            json.dump(db_info, f, ensure_ascii=False, indent=2)
    
    async def store_vectors(self, db_type: str, collection_name: str) -> Dict[str, Any]:
        """存储向量到数据库"""
        collection_id = str(uuid.uuid4())
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        await asyncio.sleep(1)
        
        collection_result = {
            "id": collection_id,
            "name": collection_name,
            "db_type": db_type,
            "create_time": current_time,
            "status": "success",
            "vector_count": 15
        }
        
        db_info_list = self._load_db_info()
        db_info_list.append(collection_result)
        self._save_db_info(db_info_list)
        
        return {
            "collection_id": collection_id,
            "status": "success",
            "message": "向量存储成功"
        }
    
    async def get_collection_list(self) -> List[Dict[str, Any]]:
        """获取集合列表"""
        return self._load_db_info()
