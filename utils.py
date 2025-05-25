from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from prompt_template import system_template_text, user_template_text
from xiaohongshu_model import Xiaohongshu
import json
import re

def parse_response_manually(response_text):
    """手动解析响应文本，提取标题和内容"""
    try:
        # 尝试直接解析JSON
        if response_text.strip().startswith('{'):
            return json.loads(response_text)
        
        # 如果不是JSON格式，尝试手动提取
        titles = []
        content = ""
        
        # 提取标题（寻找数字编号或项目符号）
        title_patterns = [
            r'(?:标题\d+[：:]|^\d+[\.、])\s*(.+)',
            r'(?:^|\n)[-•]\s*(.+)',
            r'(?:^|\n)\d+[\.、]\s*(.+)'
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, response_text, re.MULTILINE)
            if matches and len(matches) >= 5:
                titles = matches[:5]
                break
        
        # 如果没找到足够的标题，尝试按行分割
        if len(titles) < 5:
            lines = [line.strip() for line in response_text.split('\n') if line.strip()]
            potential_titles = [line for line in lines if len(line) <= 30 and '：' not in line]
            if len(potential_titles) >= 5:
                titles = potential_titles[:5]
        
        # 提取正文（通常是较长的段落）
        paragraphs = [p.strip() for p in response_text.split('\n\n') if len(p.strip()) > 50]
        if paragraphs:
            content = paragraphs[0]
        
        return {
            "titles": titles if len(titles) == 5 else ["标题1", "标题2", "标题3", "标题4", "标题5"],
            "content": content if content else "正文内容生成中..."
        }
    except Exception as e:
        print(f"手动解析失败: {e}")
        return {
            "titles": ["标题1", "标题2", "标题3", "标题4", "标题5"],
            "content": "内容解析失败，请重试"
        }

def generate_xiaohongshu(theme, openai_api_key):
    """生成小红书内容的主函数"""
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template_text),
            ("user", user_template_text)
        ])

        model = ChatOpenAI(
            model="gpt-3.5-turbo", 
            openai_api_key=openai_api_key,
            base_url="https://api.aigc369.com/v1",
            temperature=0.7
        )

        # 首先尝试JSON输出解析器
        try:
            output_parser = JsonOutputParser(pydantic_object=Xiaohongshu)
            chain = prompt | model | output_parser
            result = chain.invoke({"theme": theme})
            
            if isinstance(result, dict):
                xiaohongshu_result = Xiaohongshu(**result)
                return xiaohongshu_result
        except Exception as json_error:
            print(f"JSON解析失败，尝试字符串解析: {json_error}")
            
            # 备用方案：使用字符串解析器
            str_parser = StrOutputParser()
            chain = prompt | model | str_parser
            response_text = chain.invoke({"theme": theme})
            
            # 手动解析响应
            parsed_data = parse_response_manually(response_text)
            xiaohongshu_result = Xiaohongshu(**parsed_data)
            return xiaohongshu_result

    except Exception as e:
        print(f"生成小红书内容时出错: {str(e)}")
        raise