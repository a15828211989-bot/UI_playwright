"""
浏览器Fixtures
功能：提供浏览器和页面的pytest fixtures
"""
import pytest
import allure
from typing import Generator, Dict, Any
from playwright.sync_api import Browser, BrowserContext, Page
from config.config import config
from utils.logger import get_logger
from utils.screenshot import ScreenshotManager

logger = get_logger(__name__)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: Dict[str, Any]) -> Dict[str, Any]:
    """
    配置浏览器启动参数
    
    Args:
        browser_type_launch_args: 原始浏览器启动参数
        
    Returns:
        更新后的浏览器启动参数
    """
    logger.info("配置浏览器启动参数")
    
    # 更新浏览器参数
    browser_type_launch_args.update({
        "headless": config.HEADLESS,
        "slow_mo": config.SLOW_MO,
        "args": config.BROWSER_ARGS["args"]
    })
    
    logger.debug(f"浏览器启动参数: {browser_type_launch_args}")
    return browser_type_launch_args

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict[str, Any]) -> Dict[str, Any]:
    """
    配置浏览器上下文参数
    
    Args:
        browser_context_args: 原始浏览器上下文参数
        
    Returns:
        更新后的浏览器上下文参数
    """
    logger.info("配置浏览器上下文参数")
    
    # 更新浏览器上下文参数
    browser_context_args.update({
        "viewport": config.BROWSER_ARGS["viewport"],
        "ignore_https_errors": config.BROWSER_ARGS["ignore_https_errors"],
        "record_video_dir": config.REPORT_DIR / "videos" if config.HEADLESS else None,
        "record_video_size": {"width": 1920, "height": 1080} if config.HEADLESS else None
    })
    
    logger.debug(f"浏览器上下文参数: {browser_context_args}")
    return browser_context_args

@pytest.fixture(scope="function")
def page(browser: Browser, browser_context_args: Dict[str, Any], request) -> Generator[Page, None, None]:
    """
    创建页面实例
    
    Args:
        browser: 浏览器实例
        browser_context_args: 浏览器上下文参数
        request: pytest请求对象
        
    Yields:
        页面实例
    """
    logger.info("创建新页面")
    
    # 创建浏览器上下文
    context = browser.new_context(**browser_context_args)
    
    # 创建新页面
    page = context.new_page()
    
    # 设置页面超时
    page.set_default_timeout(config.TIMEOUT)
    page.set_default_navigation_timeout(config.TIMEOUT)
    
    # 添加Allure步骤
    with allure.step("打开新页面"):
        logger.info(f"打开新页面，超时时间: {config.TIMEOUT}ms")
        
        # 执行测试
        yield page
        
        # 测试完成后，如果有失败，截图
        if request.node.rep_call.failed:
            logger.error(f"测试失败: {request.node.name}")
            
            # 截图
            screenshot_manager = ScreenshotManager(page)
            screenshot_path = screenshot_manager.take_screenshot_on_failure(
                test_name=request.node.name,
                error_message=str(request.node.rep_call.longrepr)
            )
            
            # 附加到Allure
            if screenshot_path and screenshot_path.exists():
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=f"失败截图_{request.node.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
        
        # 关闭上下文
        logger.info("关闭页面上下文")
        context.close()

@pytest.fixture(scope="function")
def baidu_page(page: Page) -> Generator:
    """
    创建百度页面对象
    
    Args:
        page: Playwright页面对象
        
    Yields:
        百度页面对象
    """
    logger.info("创建百度页面对象")
    
    from pages.baidu_page import BaiduPage
    baidu_page = BaiduPage(page)
    
    yield baidu_page
    
    # 测试完成后可以执行清理操作
    logger.info("百度页面测试完成")