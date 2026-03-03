"""
截图工具模块
功能：提供统一的截图功能，支持失败自动截图
"""
import allure
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from playwright.sync_api import Page
from config.config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class ScreenshotManager:
    """截图管理器"""
    
    def __init__(self, page: Page):
        """
        初始化截图管理器
        
        Args:
            page: Playwright页面对象
        """
        self.page = page
        self.screenshot_dir = config.SCREENSHOT_DIR
    
    def take_screenshot(self, 
                       name: str = None, 
                       full_page: bool = True,
                       attach_to_allure: bool = True) -> Optional[Path]:
        """
        截取当前页面
        
        Args:
            name: 截图名称，如果为None则使用时间戳
            full_page: 是否截取完整页面
            attach_to_allure: 是否附加到Allure报告
            
        Returns:
            截图文件路径
        """
        try:
            # 生成截图文件名
            if name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                name = f"screenshot_{timestamp}"
            
            # 确保截图目录存在
            self.screenshot_dir.mkdir(exist_ok=True, parents=True)
            
            # 生成文件路径
            file_path = self.screenshot_dir / f"{name}.png"
            
            # 执行截图
            self.page.screenshot(
                path=str(file_path),
                full_page=full_page
            )
            
            logger.info(f"截图已保存: {file_path}")
            
            # 附加到Allure报告
            if attach_to_allure:
                with open(file_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=name,
                        attachment_type=allure.attachment_type.PNG
                    )
            
            return file_path
            
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    def take_element_screenshot(self, 
                               selector: str, 
                               name: str = None,
                               attach_to_allure: bool = True) -> Optional[Path]:
        """
        截取指定元素
        
        Args:
            selector: 元素选择器
            name: 截图名称
            attach_to_allure: 是否附加到Allure报告
            
        Returns:
            截图文件路径
        """
        try:
            element = self.page.locator(selector).first
            if not element.is_visible():
                logger.warning(f"元素 {selector} 不可见")
                return None
            
            # 生成截图文件名
            if name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                name = f"element_{selector}_{timestamp}"
            
            # 确保截图目录存在
            self.screenshot_dir.mkdir(exist_ok=True, parents=True)
            
            # 生成文件路径
            file_path = self.screenshot_dir / f"{name}.png"
            
            # 执行截图
            element.screenshot(path=str(file_path))
            
            logger.info(f"元素截图已保存: {file_path}")
            
            # 附加到Allure报告
            if attach_to_allure:
                with open(file_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=name,
                        attachment_type=allure.attachment_type.PNG
                    )
            
            return file_path
            
        except Exception as e:
            logger.error(f"元素截图失败: {e}")
            return None
    
    def take_screenshot_on_failure(self, 
                                  test_name: str,
                                  error_message: str = None) -> Optional[Path]:
        """
        测试失败时自动截图
        
        Args:
            test_name: 测试用例名称
            error_message: 错误信息
            
        Returns:
            截图文件路径
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 清理测试名称，避免特殊字符
            clean_test_name = "".join(
                c for c in test_name if c.isalnum() or c in ('_', '-')
            )
            
            name = f"FAILED_{clean_test_name}_{timestamp}"
            
            if error_message:
                # 截取错误信息前50个字符
                short_error = error_message[:50].replace(" ", "_")
                name = f"{name}_{short_error}"
            
            return self.take_screenshot(name=name, full_page=True)
            
        except Exception as e:
            logger.error(f"失败截图失败: {e}")
            return None