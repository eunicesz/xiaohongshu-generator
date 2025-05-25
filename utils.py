from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from prompt_template import system_template_text, user_template_text
from xiaohongshu_model import Xiaohongshu
import json
import re

def parse_response_manually(response_text):
    """手动解析响应文本，提取标题和内容"""
    try:
        # 清理响应文本
        response_text = response_text.strip()
        
        # 尝试直接解析JSON
        if response_text.startswith('{') and response_text.endswith('}'):
            try:
                data = json.loads(response_text)
                if 'titles' in data and 'content' in data:
                    return data
            except json.JSONDecodeError:
                pass
        
        # 如果包含```json代码块，提取其中的JSON
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                if 'titles' in data and 'content' in data:
                    return data
            except json.JSONDecodeError:
                pass
        
        # 如果不是JSON格式，尝试手动提取
        titles = []
        content = ""
        
        # 提取标题的多种模式
        title_patterns = [
            r'(?:标题\d+[：:]|^\d+[\.、])\s*(.+)',
            r'(?:^|\n)[-•]\s*(.+)',
            r'(?:^|\n)\d+[\.、]\s*(.+)',
            r'"([^"]+)"',  # 引号内的内容
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, response_text, re.MULTILINE)
            if matches and len(matches) >= 5:
                titles = [title.strip() for title in matches[:5]]
                break
        
        # 如果没找到足够的标题，尝试按行分割
        if len(titles) < 5:
            lines = [line.strip() for line in response_text.split('\n') if line.strip()]
            potential_titles = []
            for line in lines:
                # 过滤掉明显不是标题的行
                if (len(line) <= 50 and 
                    not line.startswith('{') and 
                    not line.startswith('}') and
                    '：' not in line and
                    'JSON' not in line.upper() and
                    'content' not in line.lower()):
                    potential_titles.append(line)
            
            if len(potential_titles) >= 5:
                titles = potential_titles[:5]
        
        # 提取正文（寻找较长的段落）
        paragraphs = [p.strip() for p in response_text.split('\n\n') if len(p.strip()) > 50]
        for para in paragraphs:
            # 过滤掉包含JSON关键词的段落
            if ('content' not in para.lower() and 
                'titles' not in para.lower() and
                '{' not in para and '}' not in para):
                content = para
                break
        
        # 如果还是没找到内容，尝试提取最长的行
        if not content:
            lines = [line.strip() for line in response_text.split('\n') if len(line.strip()) > 100]
            if lines:
                content = lines[0]
        
        return {
            "titles": titles if len(titles) == 5 else [f"精彩标题{i+1}" for i in range(5)],
            "content": content if content else "正文内容生成中，请重试..."
        }
        
    except Exception as e:
        print(f"手动解析失败: {e}")
        return {
            "titles": [f"默认标题{i+1}" for i in range(5)],
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

        # 直接获取字符串响应，不使用任何输出解析器
        chain = prompt | model
        response = chain.invoke({"theme": theme})
        
        # 获取响应内容
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        print(f"AI响应原文: {response_text[:200]}...")  # 调试信息
        
        # 手动解析响应
        parsed_data = parse_response_manually(response_text)
        
        # 创建并返回Xiaohongshu对象
        xiaohongshu_result = Xiaohongshu(**parsed_data)
        return xiaohongshu_result

    except Exception as e:
        print(f"生成小红书内容时出错: {str(e)}")
        # 返回默认内容而不是抛出异常
        return Xiaohongshu(
            titles=[f"关于{theme}的精彩标题{i+1}" for i in range(5)],
            content=f"关于{theme}的精彩内容正在生成中，请稍后重试..."
        )