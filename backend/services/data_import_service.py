"""
数据导入服务模块
处理不同类型文件的上传、解析和存储
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import asyncio

# 文档处理库
import pandas as pd
from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
    Docx2txtLoader
)


class DataImportService:
    def __init__(self):
        self.data_dir = Path("data")
        self.upload_dir = self.data_dir / "uploads"
        self.processed_dir = self.data_dir / "processed"
        
        # 确保目录存在
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # 文件信息存储文件
        self.file_info_path = self.data_dir / "file_info.json"
        
        # 初始化文件信息存储
        if not self.file_info_path.exists():
            self._save_file_info([])
    
    def _load_file_info(self) -> List[Dict]:
        """加载文件信息"""
        try:
            with open(self.file_info_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_file_info(self, file_info: List[Dict]):
        """保存文件信息"""
        with open(self.file_info_path, 'w', encoding='utf-8') as f:
            json.dump(file_info, f, ensure_ascii=False, indent=2)
    
    async def upload_file(self, file_type: str, file_format: str, pdf_parser: str = None) -> Dict[str, Any]:
        """
        上传并处理文件
        
        Args:
            file_type: 文件类型 (structured, semi-structured, unstructured)
            file_format: 文件格式 (excel, txt, markdown, pdf, word)
            pdf_parser: PDF解析器 (PyPDF, PyMuPDF)
        
        Returns:
            处理结果
        """
        # 模拟文件上传和处理过程
        file_id = str(uuid.uuid4())
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 模拟文件信息
        mock_file_info = {
            "id": file_id,
            "name": f"sample_{file_format}_file.{self._get_file_extension(file_format)}",
            "size": 1024 * 1024,  # 1MB
            "type": file_format,
            "file_type": file_type,
            "upload_time": current_time,
            "status": "processing",
            "pdf_parser": pdf_parser if file_format == "pdf" else None,
            "processed_data_path": None
        }
        
        # 模拟处理延迟
        await asyncio.sleep(1)
        
        try:
            # 根据文件类型进行处理
            processed_data = await self._process_file(mock_file_info)
            
            # 保存处理后的数据
            processed_file_path = self.processed_dir / f"{file_id}.json"
            with open(processed_file_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            
            # 更新文件信息
            mock_file_info["status"] = "success"
            mock_file_info["processed_data_path"] = str(processed_file_path)
            
            # 保存到文件信息列表
            file_info_list = self._load_file_info()
            file_info_list.append(mock_file_info)
            self._save_file_info(file_info_list)
            
            return {
                "file_id": file_id,
                "status": "success",
                "message": "文件处理成功",
                "processed_chunks": len(processed_data.get("chunks", []))
            }
            
        except Exception as e:
            # 处理失败
            mock_file_info["status"] = "error"
            mock_file_info["error_message"] = str(e)
            
            file_info_list = self._load_file_info()
            file_info_list.append(mock_file_info)
            self._save_file_info(file_info_list)
            
            raise Exception(f"文件处理失败: {str(e)}")
    
    async def _process_file(self, file_info: Dict) -> Dict[str, Any]:
        """
        根据文件类型处理文件
        """
        file_type = file_info["file_type"]
        file_format = file_info["type"]
        
        # 模拟不同类型文件的处理结果
        if file_type == "structured":
            if file_format == "excel":
                return self._process_excel_file(file_info)
            elif file_format == "txt":
                return self._process_txt_file(file_info)
        elif file_type == "semi-structured":
            if file_format == "markdown":
                return self._process_markdown_file(file_info)
        elif file_type == "unstructured":
            if file_format == "pdf":
                return self._process_pdf_file(file_info)
            elif file_format == "word":
                return self._process_word_file(file_info)
        
        # 默认处理
        return {
            "file_id": file_info["id"],
            "original_name": file_info["name"],
            "file_type": file_type,
            "file_format": file_format,
            "chunks": [
                {
                    "id": f"chunk_{i}",
                    "content": f"这是第{i+1}个文本块的模拟内容，来自文件 {file_info['name']}",
                    "metadata": {
                        "source": file_info["name"],
                        "chunk_index": i,
                        "chunk_type": "text"
                    }
                }
                for i in range(5)  # 模拟5个文本块
            ],
            "metadata": {
                "total_chunks": 5,
                "processing_time": datetime.now().isoformat(),
                "file_size": file_info["size"]
            }
        }
    
    def _process_excel_file(self, file_info: Dict) -> Dict[str, Any]:
        """处理Excel文件"""
        # 模拟Excel文件处理
        return {
            "file_id": file_info["id"],
            "original_name": file_info["name"],
            "file_type": "structured",
            "file_format": "excel",
            "chunks": [
                {
                    "id": f"row_{i}",
                    "content": f"姓名: 用户{i+1}, 年龄: {20+i}, 职业: 工程师",
                    "metadata": {
                        "source": file_info["name"],
                        "row_index": i,
                        "chunk_type": "structured_data"
                    }
                }
                for i in range(10)
            ],
            "metadata": {
                "total_chunks": 10,
                "columns": ["姓名", "年龄", "职业"],
                "processing_time": datetime.now().isoformat()
            }
        }
    
    def _process_txt_file(self, file_info: Dict) -> Dict[str, Any]:
        """处理TXT文件"""
        return {
            "file_id": file_info["id"],
            "original_name": file_info["name"],
            "file_type": "structured",
            "file_format": "txt",
            "chunks": [
                {
                    "id": f"line_{i}",
                    "content": f"这是TXT文件的第{i+1}行内容",
                    "metadata": {
                        "source": file_info["name"],
                        "line_number": i+1,
                        "chunk_type": "text_line"
                    }
                }
                for i in range(20)
            ],
            "metadata": {
                "total_chunks": 20,
                "processing_time": datetime.now().isoformat()
            }
        }
    
    def _process_markdown_file(self, file_info: Dict) -> Dict[str, Any]:
        """处理Markdown文件"""
        return {
            "file_id": file_info["id"],
            "original_name": file_info["name"],
            "file_type": "semi-structured",
            "file_format": "markdown",
            "chunks": [
                {
                    "id": f"section_{i}",
                    "content": f"# 第{i+1}节标题\n\n这是第{i+1}节的内容，包含了一些重要的信息。",
                    "metadata": {
                        "source": file_info["name"],
                        "section_index": i,
                        "chunk_type": "markdown_section"
                    }
                }
                for i in range(8)
            ],
            "metadata": {
                "total_chunks": 8,
                "processing_time": datetime.now().isoformat()
            }
        }
    
    def _process_pdf_file(self, file_info: Dict) -> Dict[str, Any]:
        """处理PDF文件"""
        pdf_parser = file_info.get("pdf_parser", "PyPDF")
        
        return {
            "file_id": file_info["id"],
            "original_name": file_info["name"],
            "file_type": "unstructured",
            "file_format": "pdf",
            "chunks": [
                {
                    "id": f"page_{i}",
                    "content": f"这是PDF文档第{i+1}页的内容，使用{pdf_parser}解析器提取。包含了文档的重要信息和数据。",
                    "metadata": {
                        "source": file_info["name"],
                        "page_number": i+1,
                        "parser": pdf_parser,
                        "chunk_type": "pdf_page"
                    }
                }
                for i in range(15)
            ],
            "metadata": {
                "total_chunks": 15,
                "parser_used": pdf_parser,
                "processing_time": datetime.now().isoformat()
            }
        }
    
    def _process_word_file(self, file_info: Dict) -> Dict[str, Any]:
        """处理Word文件"""
        return {
            "file_id": file_info["id"],
            "original_name": file_info["name"],
            "file_type": "unstructured",
            "file_format": "word",
            "chunks": [
                {
                    "id": f"paragraph_{i}",
                    "content": f"这是Word文档的第{i+1}个段落，包含了丰富的文本内容和格式信息。",
                    "metadata": {
                        "source": file_info["name"],
                        "paragraph_index": i,
                        "chunk_type": "word_paragraph"
                    }
                }
                for i in range(12)
            ],
            "metadata": {
                "total_chunks": 12,
                "processing_time": datetime.now().isoformat()
            }
        }
    
    def _get_file_extension(self, file_format: str) -> str:
        """获取文件扩展名"""
        extension_map = {
            "excel": "xlsx",
            "txt": "txt",
            "markdown": "md",
            "pdf": "pdf",
            "word": "docx"
        }
        return extension_map.get(file_format, "txt")
    
    async def get_file_list(self) -> List[Dict[str, Any]]:
        """获取文件列表"""
        file_info_list = self._load_file_info()
        
        # 格式化返回数据
        result = []
        for file_info in file_info_list:
            result.append({
                "id": file_info["id"],
                "name": file_info["name"],
                "size": file_info["size"],
                "type": file_info["type"],
                "file_type": file_info["file_type"],
                "upload_time": file_info["upload_time"],
                "status": file_info["status"],
                "error_message": file_info.get("error_message")
            })
        
        return result
    
    async def delete_file(self, file_id: str) -> Dict[str, Any]:
        """删除文件"""
        file_info_list = self._load_file_info()
        
        # 查找要删除的文件
        file_to_delete = None
        updated_list = []
        
        for file_info in file_info_list:
            if file_info["id"] == file_id:
                file_to_delete = file_info
            else:
                updated_list.append(file_info)
        
        if not file_to_delete:
            raise Exception(f"文件不存在: {file_id}")
        
        # 删除处理后的数据文件
        if file_to_delete.get("processed_data_path"):
            processed_file = Path(file_to_delete["processed_data_path"])
            if processed_file.exists():
                processed_file.unlink()
        
        # 更新文件信息列表
        self._save_file_info(updated_list)
        
        return {
            "file_id": file_id,
            "message": "文件删除成功"
        }
