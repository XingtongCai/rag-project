"""
生成服务模块
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import asyncio


class GenerationService:
    def __init__(self):
        self.data_dir = Path("data")
        self.generation_history_path = self.data_dir / "generation_history.json"
        
        if not self.generation_history_path.exists():
            self._save_generation_history([])
    
    def _load_generation_history(self) -> List[Dict]:
        try:
            with open(self.generation_history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_generation_history(self, history: List[Dict]):
        with open(self.generation_history_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    async def generate(self, query: str, context: list, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """内容生成"""
        generation_id = str(uuid.uuid4())
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        await asyncio.sleep(2)  # 模拟生成时间
        
        # 模拟生成结果
        generated_content = f"""
基于您的查询"{query}"和提供的上下文信息，我为您生成以下内容：

根据检索到的相关信息，{query}的相关内容如下：

1. 首先，从上下文中我们可以了解到相关的背景信息
2. 其次，结合具体的需求和场景
3. 最后，提供具体的解决方案和建议

这个回答是基于{len(context)}个相关文档片段生成的，使用了{model}模型进行内容生成。
        """.strip()
        
        generation_record = {
            "id": generation_id,
            "query": query,
            "model": model,
            "context_count": len(context),
            "generation_time": current_time,
            "content_length": len(generated_content)
        }
        
        history = self._load_generation_history()
        history.append(generation_record)
        self._save_generation_history(history)
        
        return {
            "generation_id": generation_id,
            "query": query,
            "generated_content": generated_content,
            "model": model,
            "context_used": len(context)
        }
    
    async def get_generation_history(self) -> List[Dict[str, Any]]:
        """获取生成历史"""
        return self._load_generation_history()
