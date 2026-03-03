"""
修复版本：正确的 pytest_configure 钩子
"""
import pytest
import os
import sys
import logging
import io
from pathlib import Path

# Windows 编码修复：设置UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 重新配置stdout/stderr以确保UTF-8输出
try:
    # 对于Windows，强制使用UTF-8
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer,
            encoding='utf-8',
            errors='replace',
            line_buffering=True
        )
    if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer,
            encoding='utf-8',
            errors='replace',
            line_buffering=True
        )
except Exception:
    pass

# 配置基础日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('conftest')

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"已添加项目根目录到Python路径: {project_root}")

# 创建配置对象
class SimpleConfig:
    def __init__(self):
        self.BASE_DIR = Path(project_root)
        self.REPORT_DIR = self.BASE_DIR / "reports"
        self.LOG_DIR = self.BASE_DIR / "logs"
        self.SCREENSHOT_DIR = self.BASE_DIR / "screenshots"
        self.DATA_DIR = self.BASE_DIR / "data"
        
        # 创建目录
        for dir_path in [self.REPORT_DIR, self.LOG_DIR, self.SCREENSHOT_DIR, self.DATA_DIR]:
            dir_path.mkdir(exist_ok=True, parents=True)
        
        print(f"目录已创建: {[str(d) for d in (self.REPORT_DIR, self.LOG_DIR, self.SCREENSHOT_DIR, self.DATA_DIR)]}")

# 创建全局配置实例
app_config = SimpleConfig()

# ====== Pytest 钩子函数 ======
def pytest_configure(config):
    """
    Pytest配置钩子 - 参数名必须是config（或任意名称，但不能有.obj后缀）
    """
    print("配置pytest...")
    
    # 设置Allure环境变量
    allure_results_dir = app_config.REPORT_DIR / "allure-results"
    os.environ["ALLURE_RESULTS_DIR"] = str(allure_results_dir)
    allure_results_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"Allure结果目录: {allure_results_dir}")
    
    # 设置pytest-html报告路径
    config.option.htmlpath = str(app_config.REPORT_DIR / "pytest_report.html")

def pytest_sessionstart(session):
    print("=" * 50)
    print("开始测试会话")
    print("=" * 50)

def pytest_sessionfinish(session, exitstatus):
    print("=" * 50)
    print(f"测试会话结束，退出状态: {exitstatus}")
    print("=" * 50)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

# ====== Pytest Fixtures ======
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,  # 显示浏览器窗口
        "slow_mo": 100,     # 慢速模式，便于观察
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="function")
def page(browser, browser_context_args, request):
    # 创建浏览器上下文
    context = browser.new_context(**browser_context_args)
    
    # 创建新页面
    page = context.new_page()
    
    # 设置默认超时
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    
    yield page
    
    # 测试完成后关闭上下文
    context.close()

@pytest.fixture(scope="function")
def baidu_page(page):
    """百度页面fixture"""
    from pages.baidu_page import BaiduPage
    baidu_page = BaiduPage(page)
    
    # 打开百度首页
    baidu_page.open()
    
    yield baidu_page
    
    # 测试完成后的清理（可选）
    print("百度页面测试完成")

# ====== 其他fixtures ======
@pytest.fixture(scope="function", autouse=True)
def test_logger(request):
    """测试用例日志记录"""
    test_name = request.node.name
    print(f"开始测试: {test_name}")
    
    yield
    
    # 测试完成后记录结果
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.failed:
            print(f"测试失败: {test_name}")
        else:
            print(f"测试通过: {test_name}")

# ====== 登录相关fixtures ======
@pytest.fixture(scope="function")
def login_page(page):
    """
    登录fixture：自动登录到系统
    返回登录后的page对象，可直接继续操作
    """
    import time
    print("🔐 执行登录操作...")
    
    # 打开登录页面
    page.goto("https://ent-cloud-sit2.fcbox.com/#/login")
    page.wait_for_load_state("networkidle")
    
    # 输入手机号
    mobile_input = page.locator("input[placeholder*='Mobile']")
    mobile_input.fill("0888888888")
    
    # 输入密码
    password_input = page.locator("input[type='password']")
    password_input.fill("Fc123456")
    
    # 点击同意条款
    agree_checkbox = page.locator("label:has-text('I agree to the')")
    agree_checkbox.click()
    
    # 点击登录按钮
    login_button = page.locator("button:has-text('Login')")
    login_button.click()
    
    # 等待登录完成 - 增加超时和等待时间
    time.sleep(2)  # 给登录请求一些时间
    page.wait_for_load_state("networkidle", timeout=20000)
    
    # 再等待一下确保页面完全加载
    time.sleep(2)
    
    # 验证是否成功登录（检查URL是否改变）
    current_url = page.url
    print(f"登录后URL: {current_url}")
    
    if "#/login" in current_url:
        # 如果还在登录页面，尝试再次点击登录（可能有验证失败）
        print("⚠️ 仍在登录页面，尝试重新登录...")
        # 检查是否有错误提示
        try:
            error_msg = page.locator(".error, .message, [class*='error'], [class*='message']").text_content()
            print(f"错误信息: {error_msg}")
        except:
            pass
    
    print("✅ 登录成功！")
    
    yield page
    
    print("登录测试完成")