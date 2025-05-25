from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from prompt_template import system_template_text, user_template_text
from xiaohongshu_model import Xiaohongshu

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

        output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)

        chain = prompt | model | output_parser

        result = chain.invoke({
            "parser_instructions": output_parser.get_format_instructions(),
            "theme": theme
        })

        return result
    
    except Exception as e:
        print(f"生成小红书内容时出错: {str(e)}")
        raise