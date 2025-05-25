# 爆款小红书写作助手 🌟

一个基于AI的小红书内容生成工具，帮助用户快速创作吸引人的小红书标题和正文内容。

## 功能特点

- 🤖 基于GPT-3.5-turbo的智能内容生成
- 📝 一次生成5个不同风格的标题
- 📄 自动生成配套的正文内容
- 🎨 美观的Streamlit界面
- 🚀 支持Streamlit Cloud部署

## 技术栈

- **前端框架**: Streamlit
- **AI模型**: OpenAI GPT-3.5-turbo
- **LLM框架**: LangChain
- **数据验证**: Pydantic
- **Python版本**: 3.10

## 最新更新 (2025-01-25)

✅ **已解决Python 3.13兼容性问题**
- 使用Python 3.10作为目标版本（更稳定）
- 简化依赖管理，移除版本冲突
- 修复Pydantic字段验证问题
- 优化LangChain导入路径

## 本地运行

1. 克隆项目
```bash
git clone <your-repo-url>
cd xiaohongshu-generator
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
streamlit run main.py
```

## Streamlit Cloud 部署

1. 将代码推送到GitHub仓库
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 连接GitHub仓库并选择分支
4. 确保仓库包含以下文件：
   - `main.py` (主应用文件)
   - `requirements.txt` (依赖列表)
   - `runtime.txt` (Python版本)
   - `.streamlit/config.toml` (配置文件)

## 使用说明

1. 在侧边栏输入您的OpenAI API密钥
2. 在主界面输入想要创作的主题
3. 点击"开始写作"按钮
4. 等待AI生成内容

## 故障排除

### 依赖冲突问题
如果遇到依赖版本冲突，请确保：
- 使用Python 3.10版本
- 清除pip缓存：`pip cache purge`
- 重新安装依赖：`pip install -r requirements.txt --force-reinstall`

### 部署问题
- 确保所有文件都已推送到GitHub
- 检查runtime.txt文件是否正确
- 验证requirements.txt中的依赖格式

## 文件结构

```
├── main.py                 # 主应用文件
├── utils.py               # 工具函数
├── xiaohongshu_model.py   # 数据模型
├── prompt_template.py     # 提示词模板
├── requirements.txt       # 依赖列表
├── runtime.txt           # Python版本
├── .python-version       # Python版本文件
├── .streamlit/
│   └── config.toml       # Streamlit配置
└── README.md             # 项目说明
```

## 许可证

MIT License 