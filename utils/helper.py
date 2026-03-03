"""
辅助函数模块
功能：提供各种辅助功能
"""
import time
import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from faker import Faker
from utils.logger import get_logger

logger = get_logger(__name__)
fake = Faker('zh_CN')  # 使用中文数据

class Helper:
    """辅助函数类"""
    
    @staticmethod
    def wait(seconds: float):
        """
        等待指定秒数
        
        Args:
            seconds: 等待的秒数
        """
        time.sleep(seconds)
        logger.debug(f"等待 {seconds} 秒")
    
    @staticmethod
    def random_string(length: int = 10, 
                     letters: bool = True, 
                     digits: bool = True) -> str:
        """
        生成随机字符串
        
        Args:
            length: 字符串长度
            letters: 是否包含字母
            digits: 是否包含数字
            
        Returns:
            随机字符串
        """
        chars = ""
        if letters:
            chars += string.ascii_letters
        if digits:
            chars += string.digits
        
        if not chars:
            chars = string.ascii_letters + string.digits
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def random_chinese(length: int = 5) -> str:
        """
        生成随机中文字符串
        
        Args:
            length: 字符串长度
            
        Returns:
            随机中文字符串
        """
        return fake.text(max_nb_chars=length).replace("\n", "")
    
    @staticmethod
    def random_email() -> str:
        """
        生成随机邮箱
        
        Returns:
            随机邮箱地址
        """
        return fake.email()
    
    @staticmethod
    def random_phone() -> str:
        """
        生成随机手机号
        
        Returns:
            随机手机号
        """
        return fake.phone_number()
    
    @staticmethod
    def get_current_time(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        获取当前时间字符串
        
        Args:
            format_str: 时间格式
            
        Returns:
            当前时间字符串
        """
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def get_timestamp() -> int:
        """
        获取当前时间戳
        
        Returns:
            当前时间戳（秒）
        """
        return int(time.time())
    
    @staticmethod
    def get_future_date(days: int = 7) -> str:
        """
        获取未来日期
        
        Args:
            days: 天数
            
        Returns:
            未来日期字符串
        """
        future_date = datetime.now() + timedelta(days=days)
        return future_date.strftime("%Y-%m-%d")
    
    @staticmethod
    def highlight_element(page, selector: str, color: str = "red", duration: int = 2000):
        """
        高亮显示元素
        
        Args:
            page: Playwright页面对象
            selector: 元素选择器
            color: 高亮颜色
            duration: 高亮持续时间（毫秒）
        """
        try:
            script = f"""
            (function() {{
                const element = document.querySelector('{selector}');
                if (element) {{
                    const originalStyle = element.getAttribute('style') || '';
                    element.style.border = '3px solid {color}';
                    element.style.boxShadow = '0 0 10px {color}';
                    setTimeout(() => {{
                        if (originalStyle) {{
                            element.setAttribute('style', originalStyle);
                        }} else {{
                            element.removeAttribute('style');
                        }}
                    }}, {duration});
                }}
            }})();
            """
            page.evaluate(script)
            logger.debug(f"高亮元素: {selector}")
        except Exception as e:
            logger.warning(f"高亮元素失败: {e}")
    
    @staticmethod
    def scroll_to_element(page, selector: str):
        """
        滚动到元素
        
        Args:
            page: Playwright页面对象
            selector: 元素选择器
        """
        try:
            script = f"""
            (function() {{
                const element = document.querySelector('{selector}');
                if (element) {{
                    element.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                }}
            }})();
            """
            page.evaluate(script)
            logger.debug(f"滚动到元素: {selector}")
        except Exception as e:
            logger.warning(f"滚动到元素失败: {e}")
    
    @staticmethod
    def wait_for_ajax(page, timeout: int = 30):
        """
        等待所有AJAX请求完成
        
        Args:
            page: Playwright页面对象
            timeout: 超时时间（秒）
        """
        try:
            page.wait_for_function(
                "typeof jQuery !== 'undefined' && jQuery.active === 0",
                timeout=timeout * 1000
            )
            logger.debug("AJAX请求已完成")
        except:
            logger.debug("没有jQuery或AJAX请求已超时")

# 创建辅助函数实例
helper = Helper()