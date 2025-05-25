from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from prompt_template import system_template_text, user_template_text
from xiaohongshu_model import Xiaohongshu
import json
import re

def parse_response_manually(response_text):
    """手动解析响应文本，提取标题和内容"""
    print(f"开始解析响应: {response_text[:100]}...")
    
    try:
        # 清理响应文本
        response_text = response_text.strip()
        
        # 检查是否是schema格式（我们要避免的）
        if 'properties' in response_text and 'required' in response_text:
            print("检测到schema格式，使用默认内容")
            return {
                "titles": ["🔥 精彩标题1", "💡 精彩标题2", "✨ 精彩标题3", "🚀 精彩标题4", "💯 精彩标题5"],
                "content": "AI正在学习中，请稍后重试..."
            }
        
        # 尝试直接解析JSON
        if response_text.startswith('{') and response_text.endswith('}'):
            try:
                data = json.loads(response_text)
                if 'titles' in data and 'content' in data and isinstance(data['titles'], list):
                    print("成功解析JSON格式")
                    return data
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}")
        
        # 解析新的简单文本格式
        titles = []
        content = ""
        
        # 提取标题（格式：标题1: xxx）
        title_pattern = r'标题\d+:\s*(.+)'
        title_matches = re.findall(title_pattern, response_text)
        if title_matches and len(title_matches) >= 5:
            titles = [title.strip() for title in title_matches[:5]]
            print(f"通过标题模式找到: {len(titles)}个标题")
        
        # 提取正文（格式：正文: xxx）
        content_pattern = r'正文:\s*(.+?)(?:\n\n|$)'
        content_match = re.search(content_pattern, response_text, re.DOTALL)
        if content_match:
            content = content_match.group(1).strip()
            print(f"通过正文模式找到内容: {len(content)}字符")
        
        # 如果没有找到标准格式，尝试其他方法
        if len(titles) < 5:
            print("尝试其他标题提取方法")
            # 提取标题的多种模式
            title_patterns = [
                r'(?:^|\n)\d+[\.、]\s*(.+)',
                r'(?:^|\n)[-•]\s*(.+)',
                r'"([^"]+)"',  # 引号内的内容
            ]
            
            for pattern in title_patterns:
                matches = re.findall(pattern, response_text, re.MULTILINE)
                if matches and len(matches) >= 5:
                    titles = [title.strip() for title in matches[:5]]
                    print(f"通过模式匹配找到标题: {len(titles)}个")
                    break
        
        # 如果还是没找到足够的标题，按行分割
        if len(titles) < 5:
            lines = [line.strip() for line in response_text.split('\n') if line.strip()]
            potential_titles = []
            for line in lines:
                # 过滤掉明显不是标题的行
                if (len(line) <= 50 and 
                    not line.startswith('{') and 
                    not line.startswith('}') and
                    '正文' not in line and
                    'JSON' not in line.upper() and
                    'content' not in line.lower() and
                    'properties' not in line.lower()):
                    potential_titles.append(line)
            
            if len(potential_titles) >= 5:
                titles = potential_titles[:5]
                print(f"通过行分割找到标题: {len(titles)}个")
        
        # 如果没有找到正文，尝试其他方法
        if not content:
            print("尝试其他正文提取方法")
            # 寻找较长的段落
            paragraphs = [p.strip() for p in response_text.split('\n\n') if len(p.strip()) > 50]
            for para in paragraphs:
                # 过滤掉包含关键词的段落
                if ('标题' not in para and
                    'properties' not in para.lower() and
                    '{' not in para and '}' not in para):
                    content = para
                    print(f"找到正文内容: {len(content)}字符")
                    break
        
        # 如果还是没找到内容，使用最长的行
        if not content:
            lines = [line.strip() for line in response_text.split('\n') if len(line.strip()) > 100]
            if lines:
                content = lines[0]
                print(f"使用最长行作为内容: {len(content)}字符")
        
        result = {
            "titles": titles if len(titles) == 5 else [f"🌟 精彩标题{i+1}" for i in range(5)],
            "content": content if content else "正文内容生成中，请重试..."
        }
        
        print(f"最终解析结果: 标题{len(result['titles'])}个, 内容{len(result['content'])}字符")
        return result
        
    except Exception as e:
        print(f"手动解析失败: {e}")
        return {
            "titles": [f"🎯 默认标题{i+1}" for i in range(5)],
            "content": "内容解析失败，请重试"
        }

def generate_xiaohongshu(theme, openai_api_key):
    """生成小红书内容的主函数"""
    print(f"开始生成小红书内容，主题: {theme}")
    
    try:
        # 创建一个更简单的提示词，避免复杂的格式要求
        simple_prompt = f"""
你是小红书爆款写作专家。请为主题"{theme}"创作内容。

要求：
1. 生成5个吸引人的标题（每个标题包含emoji，20字以内）
2. 生成1段正文内容（包含emoji和标签，800字以内）

请直接返回以下格式的内容，不要添加任何解释：

标题1: [第一个标题]
标题2: [第二个标题]  
标题3: [第三个标题]
标题4: [第四个标题]
标题5: [第五个标题]

正文:
[正文内容]
"""
        
        model = ChatOpenAI(
            model="gpt-3.5-turbo", 
            openai_api_key=openai_api_key,
            base_url="https://api.aigc369.com/v1",
            temperature=0.7
        )

        # 直接调用模型，不使用任何链或解析器
        print("调用AI模型...")
        response = model.invoke(simple_prompt)
        
        # 获取响应内容
        response_text = response.content if hasattr(response, 'content') else str(response)
        print(f"AI响应长度: {len(response_text)}字符")
        print(f"AI响应前200字符: {response_text[:200]}...")
        
        # 手动解析响应
        parsed_data = parse_response_manually(response_text)
        
        # 创建并返回Xiaohongshu对象
        xiaohongshu_result = Xiaohongshu(**parsed_data)
        print("成功创建Xiaohongshu对象")
        return xiaohongshu_result

    except Exception as e:
        print(f"生成小红书内容时出错: {str(e)}")
        # 返回默认内容而不是抛出异常
        return Xiaohongshu(
            titles=[f"🎨 关于{theme}的精彩标题{i+1}" for i in range(5)],
            content=f"关于{theme}的精彩内容正在生成中，请稍后重试... 🌟\n\n#小红书 #{theme} #AI生成"
        )