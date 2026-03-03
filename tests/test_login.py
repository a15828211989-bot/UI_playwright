"""
登录测试用例
"""
import time
from pathlib import Path
from playwright.sync_api import Page


def test_login(login_page: Page):
    """
    登录测试：验证登录功能
    该测试使用 login_page fixture 自动完成登录，然后验证登录结果
    """
    
    # 此时已经登录成功，可以验证页面内容或截图
    print("✅ 登录后的页面验证...")
    
    # 等待2秒确保页面稳定
    time.sleep(2)
    
    # 截图保存登录成功页面
    print("📸 截图保存...")
    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    screenshot_path = screenshot_dir / "login_success.png"
    login_page.screenshot(path=str(screenshot_path))
    
    print(f"✅ 测试完成！截图已保存到: {screenshot_path}")
