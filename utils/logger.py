"""
日志工具模块
功能：提供统一的日志记录功能，支持控制台和文件输出
"""
import sys
from loguru import logger
from pathlib import Path
from config.config import config

class Logger:
    """日志管理类"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """配置logger"""
        # 移除默认的logger
        logger.remove()
        
        # 控制台输出
        logger.add(
            sys.stderr,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            ),
            level="INFO",
            colorize=True
        )
        
        # 文件输出 - 按天分割
        log_file = config.LOG_DIR / "ui_test_{time:YYYY-MM-DD}.log"
        logger.add(
            log_file,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level: <8} | "
                "{name}:{function}:{line} - "
                "{message}"
            ),
            level="DEBUG",
            rotation="1 day",  # 每天轮换
            retention="30 days",  # 保留30天
            compression="zip",  # 压缩为zip
            encoding="utf-8"
        )
        
        # 错误日志单独记录
        error_log_file = config.LOG_DIR / "error_{time:YYYY-MM-DD}.log"
        logger.add(
            error_log_file,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level: <8} | "
                "{name}:{function}:{line} - "
                "{message}"
            ),
            level="ERROR",
            rotation="1 day",
            retention="30 days"
        )
    
    def get_logger(self):
        """获取logger实例"""
        return logger

# 创建全局日志实例
log = Logger().get_logger()

# 方便导出的快捷函数
def get_logger(name: str = __name__):
    """获取指定名称的logger"""
    return log.bind(name=name)