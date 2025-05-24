from langchain_core.pydantic_v1 import BaseModel, Field
# from pydantic import BaseModel, Field  新版
from typing import List


class Xiaohongshu(BaseModel):
    titles: List[str] = Field(description="小红书的5个标题", min_items=5, max_items=5)   #旧版min_items=5, max_items=5)  新版min_length=5, max_length=5
    content: str = Field(description="小红书的正文内容")




