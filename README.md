## UI 自动化测试框架使用说明（基于 Playwright + Pytest）1111111111

这是一个基于 **Playwright** 和 **Pytest** 的 Web UI 自动化测试框架，包含完整的登录 fixture 和订单流程演示，适合快速上手并在此基础上扩展自己的项目。

---

## 🚀 快速开始

### 一键运行测试并生成报告

```bash
python run_tests.py
```

此命令会：
1. ✅ 运行所有测试（自动 Chromium 浏览器）
2. ✅ 自动生成 Allure 可视化报告  
3. ✅ 自动生成 pytest HTML 报告
4. ✅ 自动在浏览器中打开报告

### 快速测试示例

```bash
# 仅运行登录测试
python -m pytest tests/test_login.py -v

# 仅运行订单测试（会自动使用登录fixture）
python -m pytest tests/test_order.py -v

# 运行所有测试并显示输出
python -m pytest tests/ -v -s
```

---

## 📌 登录 Fixture 的使用

框架提供了一个开箱即用的 `login_page` fixture，自动完成登录流程。在任何测试中都可以直接使用它：

### 示例：订单功能测试

```python
def test_order(login_page: Page):
    """
    已自动登录，现在开始测试订单功能
    """
    # 点击左菜单的Order选项
    order_menu = login_page.locator(".el-submenu__title:has-text('Order')")
    order_menu.first.click()

    # 点击Delivery order子菜单
    delivery = login_page.locator(".el-menu-item:has-text('Delivery order')").first
    delivery.click()

    # 等待页面加载并截图
    import time
    time.sleep(2)
    login_page.screenshot(path="screenshots/order_list.png")
```

---

## 技术栈与特点

- **Playwright 同步版**：多浏览器（Chromium / Firefox / WebKit）
- **Pytest**：支持 fixtures、参数化、标记等
- **报告体系**：
  - `pytest-html` 生成 HTML 报告
  - `allure-pytest` 生成可视化报告
- **工程化特性**：
  - ✅ `login_page` fixture 提供复用的登录逻辑
  - ✅ 自动页面加载等待（networkidle）
  - ✅ UTF-8 编码支持中文输出
  - ✅ 无需 Allure CLI，纯 Python 生成报告
  - `pages` 页面对象封装（Page Object Model）
  - `utils` 常用工具：日志、截图、辅助方法
  - `config` 统一配置，支持环境变量控制

---

## 目录结构说明

```text
UI_playwright/
├─ config/               # 配置相关
│  ├─ config.py          # 全局配置（环境、浏览器、路径等）
│  └─ settings.py        # 常量配置（超时、日志格式、数据文件等）
├─ fixtures/             # Pytest fixtures（浏览器、页面对象）
│  └─ browser_fixture.py
├─ pages/                # 页面对象（Page Object）
│  ├─ base_page.py       # 页面基类，封装常用操作
│  └─ baidu_page.py      # 百度首页页面对象示例
├─ tests/                # 测试用例
│  ├─ test_baidu_demo.py # 百度示例用例
│  └─ conftest.py        # Pytest 全局配置 & 钩子
├─ utils/                # 工具类
│  ├─ logger.py          # 日志封装（控制台 + 文件）
│  ├─ screenshot.py      # 统一截图管理（含失败自动截图）
│  └─ helper.py          # 常用辅助方法（高亮元素、随机数据等）
├─ reports/              # 测试报告（运行后自动生成）
├─ screenshots/          # 截图目录（运行后自动生成）
├─ run_tests.py          # 核心脚本：一键运行测试+生成报告
├─ allure_html_generator.py  # Allure报告生成器
├─ pytest.ini            # Pytest 全局配置（报告、日志、markers 等）
└─ requirements.txt      # Python 依赖
```

---

## 环境准备

### 安装 Python 和依赖

要求 **Python 3.8+**。

```bash
pip install -r requirements.txt
```

### 安装 Playwright 浏览器

可以用两种方式：

- 方式一：命令行直接安装

```bash
playwright install chromium
```

- 方式二：使用项目自带脚本（推荐新手）

```bash
python run_tests.py --install-browsers
```

---

## 快速开始：运行示例用例

### 基本用法

```bash
# 一键运行所有测试+生成报告+打开浏览器（推荐）
python run_tests.py
```

### 进阶用法

```bash
# 生成报告但不自动打开
python run_tests.py --no-open

# 运行特定测试文件
python run_tests.py --test tests/test_baidu_demo.py

# 运行特定测试用例
python run_tests.py --test tests/test_baidu_demo.py::test_baidu_homepage

# 运行带特定标记的测试
python run_tests.py --markers smoke

# 并行运行（4个worker）
python run_tests.py --workers 4

# 仅列出所有测试（不运行）
python run_tests.py --list-tests

# 安装Playwright浏览器
python run_tests.py --install-browsers

# 不生成Allure报告，仅运行测试
python run_tests.py --no-allure
```

---

## 配置说明

### 环境与浏览器

`config/config.py` 中通过环境变量控制：

- `ENVIRONMENT`：环境（`test` / `staging` / `production`）
- `BROWSER`：浏览器类型（`chromium` / `firefox` / `webkit`）
- `HEADLESS`：是否无头运行（`True` / `False`）
- `SLOW_MO`：慢动作间隔（毫秒，方便观察执行过程）

示例（Windows PowerShell）：

```powershell
$env:HEADLESS="False"   # 有界面运行
$env:ENVIRONMENT="test" # 使用测试环境
```

### 目录与超时

`config.Config` 会自动创建：

- 日志目录：`logs/`
- 报告目录：`reports/`
- 截图目录：`screenshots/`

超时、重试等常量在 `config/settings.py` 中维护，例如：

- 元素定位超时：`ELEMENT_TIMEOUT`
- 页面加载超时：`PAGE_TIMEOUT`
- 截图格式与质量等

---

## 框架核心模块简介

- **fixtures/browser_fixture.py**
  - 统一管理浏览器启动参数 & 上下文（视口、无头模式、视频录制等）
  - 提供 `page`、`baidu_page` 等 Pytest fixtures
  - 用例里只需声明参数即可自动获得页面对象

- **pages/base_page.py**
  - 所有页面对象的基类，封装常用操作：
    - `navigate` / `click` / `fill` / `get_text`
    - 元素可见性校验、等待、断言
    - 截图、高亮元素、滚动等

- **pages/baidu_page.py**
  - 百度首页的页面对象示例，演示如何：
    - 定义 locator 常量
    - 封装业务方法：`open`、`search`、`click_news` 等

- **tests/test_baidu_demo.py**
  - 多个示例用例：
    - 基本页面加载验证
    - 搜索功能验证（参数化）
    - 导航链接验证
    - 异常场景与断言写法演示
  - 大量 Allure 的 `epic/feature/story/title/description/step` 使用示例

---

## 新手如何新增一个页面和用例

下面以“假设新增一个登录页”为例，给出最小步骤，照着改名即可。

### 新建页面对象

在 `pages/` 下新建 `login_page.py`：

```python
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login"

    def open(self):
        self.navigate()  # 使用配置里的 BASE_URL，或传入具体 URL

    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
```

如需在 fixture 中提供 `login_page` 对象，可以参考 `browser_fixture.py` 里 `baidu_page` 的写法。

### 新增测试用例

在 `tests/` 下新建 `test_login.py`：

```python
import allure
from pages.login_page import LoginPage


@allure.epic("登录模块")
@allure.feature("登录功能")
class TestLogin:
    def test_login_success(self, page):
        login_page = LoginPage(page)

        login_page.open()
        login_page.login("demo_user", "demo_pass")

        # 这里根据实际系统添加断言，例如：
        assert "欢迎" in login_page.get_title()
```

### 运行新增用例

```bash
python run_tests.py --test tests/test_login.py
```

---

## 常见问题（FAQ）

- **Q1：浏览器没有弹出来 / 太快一闪而过？**  
  请确认：
  - 环境变量 `HEADLESS` 设置为 `False`
  - `config.Config.SLOW_MO` 可以适当调大（比如 500–1000 毫秒）

- **Q2：报告在哪？**  
  - HTML 报告：`reports/pytest_report.html`
  - Allure 原始结果：`reports/allure-results/`
  - Allure 可视化报告：`reports/allure-report/`（通过 `python run_tests.py --open-allure` 生成并打开）

- **Q3：如何只跑一部分用例？**  
  - 用 `-m` 跑指定标记，如：`python run_tests.py -m smoke`
  - 或用 `--test` 指定文件 / 具体用例。

---

如果你是第一次接触 Playwright / Pytest，**最好的学习方式** 是：

1. 先直接跑一遍：`python run_tests.py`
2. 打开报告，看每个步骤截图和描述
3. 仿照 `test_baidu_demo.py` 和 `baidu_page.py`，拷贝一份改成自己的系统页面和用例