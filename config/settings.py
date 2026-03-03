"""
项目设置 - 包含项目级设置和常量
"""
# 元素定位超时时间（秒）
ELEMENT_TIMEOUT = 30
PAGE_TIMEOUT = 60

# 重试配置
RETRY_INTERVAL = 2  # 重试间隔（秒）
MAX_RETRIES = 3     # 最大重试次数

# 截图配置
SCREENSHOT_QUALITY = 80
SCREENSHOT_TYPE = "png"

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# 测试数据文件
TEST_DATA_FILE = "test_data.json"
EXCEL_DATA_FILE = "test_data.xlsx"

# 邮件配置（可选）
EMAIL_ENABLED = False
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = ""
EMAIL_PASSWORD = ""
EMAIL_TO = []