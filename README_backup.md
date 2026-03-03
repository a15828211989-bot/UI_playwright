## UI 自动化测试框架使用说明（基于 Playwright + Pytest）

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

### 常用测试命令

```bash
# 运行特定测试文件
python run_tests.py --test tests/test_baidu_demo.py

# 运行特定测试用例
python run_tests.py --test tests/test_baidu_demo.py::test_baidu_homepage

# 并行运行（4个worker）
python run_tests.py --workers 4

# 仅列出所有测试（不运行）
python run_tests.py --list-tests
```

---

## 📌 登录 Fixture 的使用

框架提供了一个开箱即用的 `login_page` fixture，自动完成登录流程。在任何测试中都可以直接使用它：

### 示例：订单功能测试

```python
def test_order(login_page):
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

## 目录结构

```text
UI_playwright/
├─ config/               # 配置相关
├─ fixtures/             # Pytest fixtures（浏览器、页面对象）
├─ pages/                # 页面对象（Page Object）
├─ tests/                # 测试用例
├─ utils/                # 工具类
├─ reports/              # 测试报告（运行后自动生成）
├─ screenshots/          # 截图目录（运行后自动生成）
├─ run_tests.py          # 核心脚本：一键运行测试+生成报告
├─ requirements.txt      # Python 依赖
└─ README.md             # 项目说明文档
```

---

## 环境准备

### 安装依赖

1. 安装 Python 3.8+。
2. 安装项目依赖：

```bash
pip install -r requirements.txt
```

3. 安装 Playwright 浏览器：

```bash
playwright install chromium
```

---

## 常见问题（FAQ）

- **Q1：浏览器没有弹出来 / 太快一闪而过？**  
  请确认：
  - 环境变量 `HEADLESS` 设置为 `False`
  - `config.Config.SLOW_MO` 可以适当调大（比如 500–1000 毫秒）

- **Q2：报告在哪？**  
  - HTML 报告：`reports/pytest_report.html`
  - Allure 可视化报告：`reports/allure-report/`

- **Q3：如何只跑一部分用例？**  
  - 用 `-m` 跑指定标记，如：`python run_tests.py -m smoke`
  - 或用 `--test` 指定文件 / 具体用例。

---

祝您测试愉快！🚀