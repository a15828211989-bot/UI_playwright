## UI 自动化测试框架使用说明（基于 Playwright + Pytest）

这是一个基于 **Playwright** 和 **Pytest** 的 Web UI 自动化测试框架，包含完整的登录 fixture 和订单流程演示，适合快速上手并在此基础上扩展自己的项目。

---

## 🚀 快速开始（最常用）

### 一键运行测试并生成报告

```bash
python run_tests.py
```

这个命令会：
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

## 📌 【重要】登录 Fixture 的使用方法

框架提供了一个开箱即用的 `login_page` fixture，自动完成登录流程。在任何测试中都可以直接使用它：

### 1. 直接使用登录 Fixture（推荐方式）

```python
# tests/my_test.py
from playwright.sync_api import Page

def test_my_feature(login_page: Page):
    """
    此时已经自动登录，可以直接操作系统功能
    """
    # 直接点击菜单或操作页面
    login_page.locator(".menu-item").click()
    
    # 截图
    login_page.screenshot(path="screenshots/my_feature.png")
```

### 2. 登录 Fixture 做了什么？

位置：`tests/conftest.py` 中的 `login_page` fixture

自动执行以下步骤：
1. ✅ 打开登录页面
2. ✅ 填充手机号码：`0888888888`
3. ✅ 填充密码：`Fc123456`
4. ✅ 点击"我同意"条款复选框
5. ✅ 点击登录按钮
6. ✅ 等待页面加载完成（networkidle）

### 3. 实际例子：订单功能测试

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

## 一、技术栈与特点

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

## 二、目录结构说明

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

## 三、环境准备


### 1. 安装 Python 和依赖

要求 **Python 3.8+**。

```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

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

## 四、快速开始：运行示例用例

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

## 五、配置说明（config）

### 1. 环境与浏览器

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

### 2. 目录与超时

`config.Config` 会自动创建：

- 日志目录：`logs/`
- 报告目录：`reports/`
- 截图目录：`screenshots/`

超时、重试等常量在 `config/settings.py` 中维护，例如：

- 元素定位超时：`ELEMENT_TIMEOUT`
- 页面加载超时：`PAGE_TIMEOUT`
- 截图格式与质量等

---

## 六、框架核心模块简介

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

## 七、新手如何新增一个页面和用例

下面以“假设新增一个登录页”为例，给出最小步骤，照着改名即可。

### 1. 新建页面对象

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

### 2. 新增测试用例

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

### 3. 运行新增用例

```bash
python run_tests.py --test tests/test_login.py
```

---

## 八、常见问题（FAQ）

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

不会的地方，直接在 Cursor 里 @ 我，让我帮你改。 🙂

UI自动化测试框架

基于Python + Playwright + Pytest + Allure的现代化UI自动化测试框架，专为Web应用自动化测试设计。

特性

• 🚀 现代化技术栈：基于最新的Playwright自动化库

• 📊 专业报告：集成Allure生成美观的测试报告

• 🏗️ 模块化设计：采用页面对象模式（Page Object Model）

• 🔧 高度可配置：支持多种环境和浏览器配置

• 📈 完整监控：集成日志记录、自动截图和错误追踪

• ⚡ 高效执行：支持并行测试和数据驱动测试

• 🛠️ 易用性：简洁的API和详细的示例，新手也能快速上手

项目结构


ui-automation-framework/
├── config/                 # 配置文件目录
│   ├── __init__.py
│   ├── config.py          # 主配置文件
│   └── settings.py        # 项目设置
├── data/                  # 测试数据目录
│   ├── __init__.py
│   └── test_data.json    # 测试数据文件
├── pages/                 # 页面对象模型目录
│   ├── __init__.py
│   ├── base_page.py      # 基类页面
│   └── baidu_page.py     # 百度页面对象
├── tests/                 # 测试用例目录
│   ├── __init__.py
│   ├── conftest.py       # Pytest配置
│   └── test_baidu_demo.py # 示例测试用例
├── utils/                 # 工具函数目录
│   ├── __init__.py
│   ├── logger.py         # 日志工具
│   ├── screenshot.py     # 截图工具
│   └── helper.py         # 辅助函数
├── fixtures/             # Pytest fixtures目录
│   ├── __init__.py
│   └── browser_fixture.py # 浏览器相关fixtures
├── reports/              # 测试报告目录（自动生成）
├── logs/                 # 日志目录（自动生成）
├── screenshots/          # 截图目录（自动生成）
├── requirements.txt      # Python依赖包列表
├── .gitignore           # Git忽略文件配置
├── pytest.ini           # Pytest配置文件
├── run_tests.py         # 测试运行入口脚本
└── README.md           # 项目说明文档


环境要求

最低要求

• 操作系统：Windows 10/11，macOS 10.15+，Linux（Ubuntu 18.04+）

• Python版本：Python 3.8或更高版本

• 内存：至少4GB RAM

• 磁盘空间：至少2GB可用空间

推荐配置

• 操作系统：Windows 11或macOS 12+

• Python版本：Python 3.10+

• 内存：8GB RAM或更高

• 磁盘空间：5GB可用空间

• 网络：稳定的互联网连接

环境搭建

第一步：安装Python

Windows系统

1. 访问 https://www.python.org/downloads/
2. 下载Windows安装程序（推荐版本3.10+）
3. 运行安装程序，务必勾选"Add Python to PATH"选项
4. 验证安装：
   python --version
   pip --version
   

macOS系统

# 使用Homebrew安装（推荐）
brew install python@3.10

# 验证安装
python3 --version
pip3 --version


Linux系统（Ubuntu）

# 安装Python和pip
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# 验证安装
python3 --version
pip3 --version


第二步：获取项目代码

克隆项目

git clone <repository-url>
cd ui-automation-framework


或手动创建

mkdir ui-automation-framework
cd ui-automation-framework
# 按照项目结构创建目录和文件


第三步：创建虚拟环境

Windows

python -m venv venv
# 激活虚拟环境
venv\Scripts\activate
# 如果PowerShell提示权限错误，先运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser


macOS/Linux

python3 -m venv venv
# 激活虚拟环境
source venv/bin/activate


第四步：安装依赖包

# 使用国内镜像加速安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 如果安装缓慢或失败，分别安装主要依赖
pip install playwright pytest allure-pytest loguru -i https://pypi.tuna.tsinghua.edu.cn/simple


第五步：安装Playwright浏览器

# 安装Chromium浏览器（推荐）
playwright install chromium

# 验证安装
playwright --version


第六步：验证安装

# 运行示例测试
python run_tests.py --test tests/test_baidu_demo.py::TestBaiduHomePage::test_baidu_button_text


预期结果：
• 自动打开浏览器并执行测试

• 在控制台看到测试通过信息

• 在logs/目录生成日志文件

• 在reports/目录生成测试报告

快速开始

运行测试

# 运行所有测试
python run_tests.py

# 运行单个测试文件
python run_tests.py --test tests/test_baidu_demo.py

# 运行特定测试方法
python run_tests.py --test tests/test_baidu_demo.py::TestBaiduHomePage::test_baidu_button_text

# 并行运行测试（4个worker）
python run_tests.py --workers 4

# 运行标记测试
python run_tests.py --markers smoke


查看报告

# 生成HTML报告（自动生成）
# 报告位置：reports/pytest_report.html

# 生成Allure报告
python run_tests.py --generate-allure

# 生成并打开Allure报告
python run_tests.py --open-allure


配置框架

编辑config/config.py文件：
# 修改浏览器类型
BROWSER = "chromium"  # 可选: chromium, firefox, webkit

# 修改是否无头模式
HEADLESS = False  # True: 不显示浏览器窗口，False: 显示浏览器窗口

# 修改环境
ENVIRONMENT = "test"  # test, staging, production

# 修改超时时间
TIMEOUT = 30000  # 毫秒


编写测试用例

创建页面对象

在pages/目录下创建新文件，如login_page.py：
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class LoginPage(BasePage):
    """登录页面"""
    
    # 页面元素定位器
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#loginBtn"
    
    def login(self, username: str, password: str):
        """执行登录"""
        logger.info(f"登录用户: {username}")
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)


创建测试用例

在tests/目录下创建新文件，如test_login.py：
import allure
from pages.login_page import LoginPage

@allure.epic("用户认证")
@allure.feature("登录功能")
class TestLogin:
    
    @allure.story("成功登录")
    @allure.title("测试用户成功登录")
    def test_successful_login(self, page):
        """测试成功登录"""
        login_page = LoginPage(page)
        
        with allure.step("打开登录页面"):
            login_page.open_login_page()
        
        with allure.step("输入用户名和密码"):
            login_page.login("testuser", "password123")
        
        with allure.step("验证登录成功"):
            assert "dashboard" in login_page.get_url().lower()


运行新测试

python run_tests.py --test tests/test_login.py


示例测试用例

框架包含一个完整的示例测试用例，演示如何测试百度搜索功能：
# tests/test_baidu_demo.py 中的教学用例
def test_baidu_button_text(self, baidu_page: BaiduPage):
    """
    验证百度一下按钮文本 - 示例测试用例
    这是教学用例，演示如何断言页面中有【百度一下】的按钮文案
    """
    with allure.step("步骤1: 打开百度首页"):
        baidu_page.open()
    
    with allure.step("步骤2: 获取搜索按钮文本"):
        button_text = baidu_page.get_search_button_text()
    
    with allure.step("步骤3: 验证按钮文本包含'百度一下'"):
        # 方法1: 使用页面对象的断言方法
        baidu_page.assert_search_button_contains_text("百度一下")
        
        # 方法2: 使用pytest的assert语句
        assert "百度一下" in button_text
        
        # 方法3: 使用更详细的断言信息
        expected_text = "百度一下"
        assert expected_text in button_text, (
            f"搜索按钮文本断言失败！\n"
            f"期望包含: '{expected_text}'\n"
            f"实际文本: '{button_text}'"
        )


运行示例测试：
python run_tests.py --test tests/test_baidu_demo.py::TestBaiduHomePage::test_baidu_button_text


常用命令

测试运行

# 运行所有测试
pytest

# 运行指定测试
pytest tests/test_baidu_demo.py

# 运行并显示详细输出
pytest -v

# 运行失败后重试
pytest --reruns 3


报告生成

# 生成HTML报告
pytest --html=reports/report.html

# 生成Allure结果
pytest --alluredir=reports/allure-results

# 查看Allure报告
allure serve reports/allure-results


调试命令

# 输出详细日志
pytest --log-cli-level=DEBUG

# 失败时进入调试模式
pytest --pdb

# 只收集测试不执行
pytest --collect-only


配置说明

环境变量

框架支持通过环境变量覆盖配置：
# 设置环境变量
export ENVIRONMENT=staging
export BROWSER=firefox
export HEADLESS=true

# Windows系统
set ENVIRONMENT=staging
set BROWSER=firefox
set HEADLESS=true


配置文件

• config/config.py：主配置文件，包含所有可配置项

• config/settings.py：项目设置，包含常量

• pytest.ini：Pytest配置文件

故障排除

常见问题

Q1：浏览器无法启动

A：检查是否安装了浏览器：playwright install chromium
   检查是否有浏览器冲突：关闭所有浏览器后再运行测试


Q2：元素找不到或超时

A：增加等待时间：修改config.py中的TIMEOUT
   检查元素定位器：使用浏览器开发者工具验证


Q3：测试运行缓慢

A：启用无头模式：设置HEADLESS=true
   减少SLOW_MO：修改config.py中的SLOW_MO


Q4：依赖安装失败

A：使用国内镜像：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple
   升级pip：pip install --upgrade pip


获取帮助

1. 查看日志文件：logs/目录下的日志文件
2. 查看截图：screenshots/目录下的截图
3. 查看官方文档：
   • https://playwright.dev/python/

   • https://docs.pytest.org/

   • https://docs.qameta.io/allure/

最佳实践

1. 页面对象模式

• 每个页面创建一个类

• 将元素定位器定义为类属性

• 将页面操作封装为方法

• 避免在测试用例中直接使用选择器

2. 测试数据管理

• 使用JSON/YAML文件管理测试数据

• 使用Faker生成测试数据

• 数据与代码分离

3. 测试用例设计

• 使用描述性的测试名称

• 每个测试用例只测试一个功能

• 添加详细的断言信息

4. 报告和日志

• 为每个测试步骤添加Allure步骤

• 记录详细的日志信息

• 失败时自动截图

更新和维护

更新依赖

# 更新所有依赖
pip install --upgrade -r requirements.txt

# 更新Playwright
pip install --upgrade playwright
playwright install --force chromium



祝您测试愉快！🚀