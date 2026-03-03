"""
百度页面对象
功能：封装百度首页的所有操作
"""
from typing import Optional
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class BaiduPage(BasePage):
    """百度页面对象"""
    
    # 页面元素定位器
    SEARCH_INPUT = "#kw"  # 搜索输入框
    SEARCH_BUTTON = "#su"  # 百度一下按钮
    NEWS_LINK = "text=新闻"  # 新闻链接
    MAP_LINK = "text=地图"  # 地图链接
    VIDEO_LINK = "text=视频"  # 视频链接
    HAO123_LINK = "text=hao123"  # hao123链接
    LOGIN_BUTTON = "#s-top-loginbtn"  # 登录按钮
    SETTING_LINK = "#s-usersetting-top"  # 设置链接
    ADVANCED_SEARCH_LINK = "#s-top-advanced"  # 高级搜索链接
    
    def __init__(self, page):
        """
        初始化百度页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
    
    def open(self):
        """
        打开百度首页
        """
        logger.info("打开百度首页")
        self.navigate("https://www.baidu.com")
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """
        等待页面加载完成
        """
        logger.info("等待百度页面加载完成")
        self.wait_for_element(self.SEARCH_INPUT)
        logger.info("百度页面加载完成")
    
    def search(self, keyword: str):
        """
        执行搜索
        
        Args:
            keyword: 搜索关键词
        """
        logger.info(f"搜索关键词: {keyword}")
        
        # 输入搜索词
        self.fill(self.SEARCH_INPUT, keyword)
        
        # 点击搜索按钮
        self.click(self.SEARCH_BUTTON)
        
        # 等待搜索结果加载
        self.page.wait_for_load_state("networkidle")
        logger.info("搜索完成")
    
    def click_news(self):
        """
        点击新闻链接
        """
        logger.info("点击新闻链接")
        self.click(self.NEWS_LINK)
        self.page.wait_for_load_state("networkidle")
    
    def click_map(self):
        """
        点击地图链接
        """
        logger.info("点击地图链接")
        self.click(self.MAP_LINK)
        self.page.wait_for_load_state("networkidle")
    
    def click_video(self):
        """
        点击视频链接
        """
        logger.info("点击视频链接")
        self.click(self.VIDEO_LINK)
        self.page.wait_for_load_state("networkidle")
    
    def get_search_button_text(self) -> str:
        """
        获取搜索按钮文本
        
        Returns:
            搜索按钮文本
        """
        logger.info("获取搜索按钮文本")
        return self.get_text(self.SEARCH_BUTTON)
    
    def is_search_button_visible(self) -> bool:
        """
        检查搜索按钮是否可见
        
        Returns:
            是否可见
        """
        return self.is_visible(self.SEARCH_BUTTON)
    
    def assert_search_button_contains_text(self, expected_text: str = "百度一下"):
        """
        断言搜索按钮包含指定文本
        
        Args:
            expected_text: 期望的文本，默认为"百度一下"
        """
        logger.info(f"断言搜索按钮包含文本: {expected_text}")
        self.assert_text_contains(self.SEARCH_BUTTON, expected_text)
    
    def get_search_input_value(self) -> str:
        """
        获取搜索输入框的值
        
        Returns:
            输入框的值
        """
        logger.info("获取搜索输入框的值")
        return self.page.input_value(self.SEARCH_INPUT)
    
    def clear_search_input(self):
        """
        清空搜索输入框
        """
        logger.info("清空搜索输入框")
        self.page.fill(self.SEARCH_INPUT, "")
    
    def take_homepage_screenshot(self, name: str = "baidu_homepage"):
        """
        截取百度首页截图
        
        Args:
            name: 截图名称
        """
        logger.info(f"截取百度首页截图: {name}")
        return self.screenshot(name)