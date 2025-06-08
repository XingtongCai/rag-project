"""
检索服务模块
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import asyncio


class RetrievalService:
    def __init__(self):
        self.data_dir = Path("data")
        self.search_history_path = self.data_dir / "search_history.json"
        
        if not self.search_history_path.exists():
            self._save_search_history([])
    
    def _load_search_history(self) -> List[Dict]:
        try:
            with open(self.search_history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_search_history(self, history: List[Dict]):
        with open(self.search_history_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    async def search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """向量检索"""
        search_id = str(uuid.uuid4())
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        await asyncio.sleep(1)
        
        # 模拟检索结果
        results = [
            {
                "id": f"result_{i}",
                "content": f"这是与查询'{query}'相关的第{i+1}个检索结果",
                "score": 0.9 - i * 0.1,
                "metadata": {"source": f"document_{i}.txt"}
            }
            for i in range(top_k)
        ]
        
        search_record = {
            "id": search_id,
            "query": query,
            "top_k": top_k,
            "search_time": current_time,
            "results_count": len(results)
        }
        
        history = self._load_search_history()
        history.append(search_record)
        self._save_search_history(history)
        
        return {
            "search_id": search_id,
            "query": query,
            "results": results
        }
    
    async def get_search_history(self) -> List[Dict[str, Any]]:
        """获取检索历史"""
        return self._load_search_history()
