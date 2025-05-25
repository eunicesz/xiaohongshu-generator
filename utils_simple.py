import requests
import json
import re

class SimpleXiaohongshu:
    """简单的小红书内容类，不依赖pydantic"""
    def __init__(self, titles, content):
        self.titles = titles if isinstance(titles, list) and len(titles) == 5 else [f"🌟 标题{i+1}" for i in range(5)]
        self.content = content if content else "内容生成中..."

def parse_simple_response(response_text):
    """解析简单文本格式的响应"""
    print(f"解析响应: {response_text[:100]}...")
    
    # 检查是否是schema格式
    if 'properties' in response_text and 'required' in response_text:
        print("检测到schema格式，返回默认内容")
        return {
            "titles": ["🔥 热门话题", "💡 实用技巧", "✨ 生活妙招", "🚀 必看攻略", "💯 超实用"],
            "content": "内容正在生成中，请稍后重试... 🌟"
        }
    
    titles = []
    content = ""
    
    # 提取标题
    title_pattern = r'标题\d+:\s*(.+)'
    title_matches = re.findall(title_pattern, response_text)
    if title_matches and len(title_matches) >= 5:
        titles = [title.strip() for title in title_matches[:5]]
        print(f"找到{len(titles)}个标题")
    
    # 提取正文
    content_pattern = r'正文:\s*(.+?)(?:\n\n|$)'
    content_match = re.search(content_pattern, response_text, re.DOTALL)
    if content_match:
        content = content_match.group(1).strip()
        print(f"找到正文: {len(content)}字符")
    
    # 如果没找到，使用备用方法
    if len(titles) < 5:
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) <= 50 and '正文' not in line and not line.startswith('#'):
                titles.append(line)
                if len(titles) >= 5:
                    break
    
    if not content:
        paragraphs = response_text.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50 and '标题' not in para:
                content = para
                break
    
    return {
        "titles": titles[:5] if len(titles) >= 5 else [f"🌟 精彩标题{i+1}" for i in range(5)],
        "content": content if content else "内容生成中，请重试..."
    }

def generate_xiaohongshu_simple(theme, openai_api_key):
    """使用requests直接调用OpenAI API生成小红书内容"""
    print(f"生成内容，主题: {theme}")
    
    try:
        # API请求配置
        url = "https://api.aigc369.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }
        
        # 简单的提示词
        prompt = f"""
请为主题"{theme}"创作小红书内容。

格式要求：
标题1: [包含emoji的标题1]
标题2: [包含emoji的标题2]
标题3: [包含emoji的标题3]
标题4: [包含emoji的标题4]
标题5: [包含emoji的标题5]

正文:
[包含emoji和标签的正文内容]
"""
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        print("调用OpenAI API...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        response_text = result['choices'][0]['message']['content']
        print(f"API响应: {response_text[:200]}...")
        
        # 解析响应
        parsed_data = parse_simple_response(response_text)
        
        # 创建对象
        result = SimpleXiaohongshu(**parsed_data)
        print("成功创建对象")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {str(e)}")
        return SimpleXiaohongshu(
            titles=[f"🎨 {theme}相关标题{i+1}" for i in range(5)],
            content=f"关于{theme}的内容正在准备中... 🌟\n\n#{theme} #小红书"
        )
    except Exception as e:
        print(f"生成失败: {str(e)}")
        return SimpleXiaohongshu(
            titles=[f"🎨 {theme}相关标题{i+1}" for i in range(5)],
            content=f"关于{theme}的内容正在准备中... 🌟\n\n#{theme} #小红书"
        ) 