import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'sk-a34cfada22a747a29a54979e4c333e10')  # 替换为你的API密钥
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

# 文件上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'csv'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 其他配置参数（可选）
# 例如，设置最大token数、温度等
MAX_TOKENS = 150
TEMPERATURE = 0.7

