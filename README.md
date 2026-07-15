# 🧪 LLM 质量测试平台（DeepEval + SiliconFlow）

&gt; 大二软件工程学生的 AI 大模型质量测试实践项目  
&gt; 技术栈：Python | DeepEval | pytest | SiliconFlow API 

## 📌 项目简介

本项目基于 [DeepEval](https://github.com/confident-ai/deepeval) 框架，使用 SiliconFlow 提供的大模型 API 作为评测模型（LLM-as-a-Judge），对 LLM 输出进行自动化质量评估。

### 评测指标覆盖

| 指标 | 说明 | 适用场景 |
|------|------|----------|
| Faithfulness | 忠实度 | RAG 回答是否忠实于检索上下文 |
| Hallucination | 幻觉检测 | 回答是否包含虚构信息 |
| Answer Relevancy | 答案相关性 | 回答是否切题 |
| Contextual Relevancy | 上下文相关性 | 检索到的上下文是否相关 |

## 🚀 快速开始

### 环境要求
- Python 3.10+
- SiliconFlow API Key（[免费注册](https://cloud.siliconflow.cn)）

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourname/llm-quality-testing.git
cd llm-quality-testing

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 SiliconFlow API Key
SILICONFLOW_API_KEY=sk-your-key-here

# 运行全部测试
pytest tests/ -v

# 运行单个测试文件
pytest tests/test_faithfulness.py -v

# 生成 HTML 测试报告
pytest tests/ -v --html=report.html

# 运行批量评测脚本
python scripts/run_evaluation.py

---

### 2. `.env.example` — 环境变量模板

```env
# SiliconFlow API 配置
# 注册地址：https://cloud.siliconflow.cn
SILICONFLOW_API_KEY=sk-your-siliconflow-api-key-here

# 可选：评测模型选择
# EVAL_MODEL=deepseek-ai/DeepSeek-V3
# EVAL_MODEL=Qwen/Qwen2.5-72B-Instruct
