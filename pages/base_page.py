"""
页面基类
功能：所有页面对象的基类，提供通用的页面操作方法
"""
from playwright.sync_api import Page, Locator, expect
from typing import Optional, Tuple, List, Any
from config.config import config
from config import settings
from utils.logger import get_logger
from utils.screenshot import ScreenshotManager
from utils.helper import helper

logger = get_logger(__name__)

class BasePage:
    """页面基类"""
    
    def __init__(self, page: Page):
        """
        初始化页面对象
        
        Args:
            page: Playwright页面对象
        """
        self.page = page
        self.timeout = settings.ELEMENT_TIMEOUT * 1000  # 转换为毫秒
        self.screenshot_manager = ScreenshotManager(page)
        
        # 设置默认超时
        self.page.set_default_timeout(self.timeout)
    
    def navigate(self, url: str = None):
        """
        导航到指定URL
        
        Args:
            url: 要访问的URL，如果为None则使用配置的BASE_URL
        """
        target_url = url or config.BASE_URL
        logger.info(f"导航到: {target_url}")
        self.page.goto(target_url, timeout=settings.PAGE_TIMEOUT * 1000)
        self.page.wait_for_load_state("networkidle")
    
    def get_element(self, selector: str) -> Locator:
        """
        获取元素定位器
        
        Args:
            selector: 元素选择器
            
        Returns:
            元素定位器
        """
        return self.page.locator(selector).first
    
    def click(self, selector: str, timeout: int = None):
        """
        点击元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.info(f"点击元素: {selector}")
        
        try:
            element = self.get_element(selector)
            element.scroll_into_view_if_needed()
            element.click(timeout=timeout)
        except Exception as e:
            logger.error(f"点击元素失败: {selector}, 错误: {e}")
            raise
    
    def fill(self, selector: str, text: str, timeout: int = None):
        """
        填充文本
        
        Args:
            selector: 元素选择器
            text: 要输入的文本
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.info(f"在元素 {selector} 中输入文本: {text}")
        
        try:
            element = self.get_element(selector)
            element.scroll_into_view_if_needed()
            element.fill(text, timeout=timeout)
        except Exception as e:
            logger.error(f"输入文本失败: {selector}, 错误: {e}")
            raise
    
    def get_text(self, selector: str, timeout: int = None) -> str:
        """
        获取元素文本
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒）
            
        Returns:
            元素文本
        """
        timeout = timeout or self.timeout
        logger.info(f"获取元素文本: {selector}")
        
        try:
            element = self.get_element(selector)
            return element.text_content(timeout=timeout) or ""
        except Exception as e:
            logger.error(f"获取文本失败: {selector}, 错误: {e}")
            raise
    
    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """
        检查元素是否可见
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒）
            
        Returns:
            是否可见
        """
        timeout = timeout or self.timeout
        
        try:
            element = self.get_element(selector)
            return element.is_visible(timeout=timeout)
        except:
            return False
    
    def wait_for_element(self, selector: str, timeout: int = None):
        """
        等待元素出现
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.info(f"等待元素: {selector}")
        
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
        except Exception as e:
            logger.error(f"等待元素超时: {selector}, 错误: {e}")
            raise
    
    def wait_for_element_hidden(self, selector: str, timeout: int = None):
        """
        等待元素隐藏
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.info(f"等待元素隐藏: {selector}")
        
        try:
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
        except Exception as e:
            logger.error(f"等待元素隐藏超时: {selector}, 错误: {e}")
            raise
    
    def assert_text_contains(self, selector: str, expected_text: str, timeout: int = None):
        """
        断言元素文本包含指定内容
        
        Args:
            selector: 元素选择器
            expected_text: 期望的文本
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.info(f"断言元素 {selector} 包含文本: {expected_text}")
        
        try:
            element = self.get_element(selector)
            expect(element).to_contain_text(expected_text, timeout=timeout)
        except Exception as e:
            logger.error(f"断言失败: 元素 {selector} 不包含文本 '{expected_text}', 错误: {e}")
            self.screenshot_manager.take_screenshot(f"assert_failed_{selector}")
            raise
    
    def assert_element_visible(self, selector: str, timeout: int = None):
        """
        断言元素可见
        
        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.info(f"断言元素可见: {selector}")
        
        try:
            element = self.get_element(selector)
            expect(element).to_be_visible(timeout=timeout)
        except Exception as e:
            logger.error(f"断言失败: 元素 {selector} 不可见, 错误: {e}")
            self.screenshot_manager.take_screenshot(f"assert_failed_{selector}")
            raise
    
    def get_title(self) -> str:
        """
        获取页面标题
        
        Returns:
            页面标题
        """
        return self.page.title()
    
    def get_url(self) -> str:
        """
        获取当前URL
        
        Returns:
            当前URL
        """
        return self.page.url
    
    def refresh(self):
        """
        刷新页面
        """
        logger.info("刷新页面")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
    
    def go_back(self):
        """
        返回上一页
        """
        logger.info("返回上一页")
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")
    
    def go_forward(self):
        """
        前进到下一页
        """
        logger.info("前进到下一页")
        self.page.go_forward()
        self.page.wait_for_load_state("networkidle")
    
    def screenshot(self, name: str = None, full_page: bool = True) -> Optional[str]:
        """
        截取页面截图
        
        Args:
            name: 截图名称
            full_page: 是否截取完整页面
            
        Returns:
            截图文件路径
        """
        return self.screenshot_manager.take_screenshot(name, full_page)
    
    def highlight(self, selector: str, color: str = "red", duration: int = 2000):
        """
        高亮元素
        
        Args:
            selector: 元素选择器
            color: 高亮颜色
            duration: 高亮持续时间（毫秒）
        """
        helper.highlight_element(self.page, selector, color, duration)
    
    def scroll_to(self, selector: str):
        """
        滚动到元素
        
        Args:
            selector: 元素选择器
        """
        helper.scroll_to_element(self.page, selector)