
"""
百度测试用例
"""
from playwright.sync_api import Page

def test_baidu_homepage(page: Page):
    """打开百度首页，验证页面中是否有'百度一下'文案"""
    # 打开百度首页
    page.goto("https://www.baidu.com")
    page.wait_for_load_state("networkidle")
    
    # 获取整个页面的文本内容
    page_text = page.locator("body").text_content()
    
    # 断言：检查整个页面是否包含"百度一下"
    assert "百度一下" in page_text, f"错误: 页面中找不到'百度一下'文案"
    
    print(f"✅ 测试通过! 页面中找到了'百度一下'文案")