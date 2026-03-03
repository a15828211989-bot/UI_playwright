"""
配置文件 - 存储项目所有配置信息
功能：集中管理项目配置，便于维护和修改
"""
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """配置类，包含所有项目配置"""
    
    # 项目根目录
    BASE_DIR = Path(__file__).parent.parent
    
    # 环境配置
    ENVIRONMENT = os.getenv("ENVIRONMENT", "test")  # test, staging, production
    
    # Playwright配置
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "100"))  # 延迟毫秒，方便观察
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))  # 默认超时时间
    
    # 测试配置
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))  # 隐式等待秒数
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "30"))  # 显式等待秒数
    RETRY_TIMES = int(os.getenv("RETRY_TIMES", "3"))  # 失败重试次数
    
    # URL配置
    URLS: Dict[str, str] = {
        "test": "https://www.baidu.com",
        "staging": "https://www.baidu.com",
        "production": "https://www.baidu.com"
    }
    
    # 获取当前环境的URL
    @property
    def BASE_URL(self) -> str:
        """返回当前环境的Base URL"""
        return self.URLS.get(self.ENVIRONMENT, self.URLS["test"])
    
    # 路径配置
    @property
    def LOG_DIR(self) -> Path:
        """日志目录"""
        return self.BASE_DIR / "logs"
    
    @property
    def REPORT_DIR(self) -> Path:
        """报告目录"""
        return self.BASE_DIR / "reports"
    
    @property
    def SCREENSHOT_DIR(self) -> Path:
        """截图目录"""
        return self.BASE_DIR / "screenshots"
    
    @property
    def DATA_DIR(self) -> Path:
        """数据目录"""
        return self.BASE_DIR / "data"
    
    # 创建必要的目录
    def create_directories(self):
        """创建项目所需的所有目录"""
        directories = [
            self.LOG_DIR,
            self.REPORT_DIR,
            self.SCREENSHOT_DIR,
            self.DATA_DIR
        ]
        for directory in directories:
            directory.mkdir(exist_ok=True, parents=True)
    
    # 浏览器参数
    @property
    def BROWSER_ARGS(self) -> Dict[str, Any]:
        """浏览器启动参数"""
        args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars"
        ]
        
        if self.HEADLESS:
            args.append("--headless=new")
        
        return {
            "args": args,
            "viewport": {"width": 1920, "height": 1080},
            "ignore_https_errors": True
        }

# 创建配置实例
config = Config()

# 初始化时创建目录
config.create_directories()