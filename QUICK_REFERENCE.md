# 🚀 快速参考卡（Quick Reference）

## 最常用命令

```bash
# 一键运行所有测试 + 生成报告（推荐）
python run_tests.py

# 运行特定测试
python -m pytest tests/test_login.py -v
python -m pytest tests/test_order.py -v

# 查看完整输出
python -m pytest tests/ -v -s
```

---

## 项目状态

| 组件 | 状态 |
|------|------|
| 百度测试 | ✅ 通过 |
| 登录测试 | ✅ 通过 |
| 订单测试 | ✅ 通过 |
| 报告生成 | ✅ 成功 |
| 中文支持 | ✅ 完整 |
| Fixture 复用 | ✅ 工作 |

---

## 核心文件位置

```
tests/conftest.py         ← login_page fixture 在这里
tests/test_login.py       ← 登录测试示例
tests/test_order.py       ← 订单测试示例（使用 fixture）
run_tests.py              ← 一键运行脚本
```

---

## 创建新测试的模板

```python
# tests/test_my_feature.py
from playwright.sync_api import Page

def test_my_feature(login_page: Page):
    """已自动登录，可直接开始操作"""
    
    # 操作已登录页面
    login_page.locator(".button").click()
    
    # 截图
    login_page.screenshot(path="screenshots/my_feature.png")
```

---

## 登录信息

- **URL**: https://ent-cloud-sit2.fcbox.com/#/login
- **手机号**: 0888888888
- **密码**: Fc123456

> ⚠️ 修改凭证: 编辑 `tests/conftest.py` 中的 `login_page` fixture

---

## 截图位置

所有截图自动保存到: `screenshots/`

- `login_success.png` - 登录后的首页
- `order_page.png` - 订单列表页面

---

## 报告位置

- **Pytest HTML**: `reports/pytest_report.html`
- **Allure 报告**: `reports/allure-report/index.html`

---

## 常见问题排查

### 问题: 测试超时
**解决**: 增加 Playwright 超时时间
```python
page.set_default_timeout(60000)  # 60秒
```

### 问题: 选择器找不到元素
**解决**: 使用 Playwright Inspector 调试
```bash
playwright codegen https://ent-cloud-sit2.fcbox.com/
```

### 问题: 报告生成失败
**解决**: 检查 `reports/allure-results/` 目录是否有 JSON 文件

---

## 项目结构速览

```
项目根目录/
├── tests/                    # 测试用例
│   ├── conftest.py          # 全局配置 & fixtures
│   ├── test_login.py        # 登录测试
│   ├── test_order.py        # 订单测试
│   └── test_baidu_demo.py   # 百度演示
├── reports/                 # 测试报告
├── screenshots/             # 截图输出
├── run_tests.py             # 主运行脚本
├── pytest.ini               # Pytest 配置
├── requirements.txt         # 依赖清单
└── README.md                # 详细文档
```

---

## 下一步

1. **创建更多测试**: 在 `tests/` 中添加 `test_*.py` 文件
2. **复用登录**: 所有新测试都可以用 `login_page` fixture
3. **定制凭证**: 修改 `conftest.py` 中的登录参数
4. **CI/CD 集成**: 将 `python run_tests.py` 加入 CI pipeline

---

## 技术栈

- Playwright 1.40+
- Pytest 7.4+
- Python 3.8+
- allure-pytest 2.13+
- pytest-html 4.1+

---

## 获取帮助

- 查看详细文档: `README.md`
- 查看实现总结: `IMPLEMENTATION_SUMMARY.md`
- 检查错误日志: 运行测试时的 stdout 输出
- 查看截图/HTML: `screenshots/` 和 `reports/`

---

**最后更新**: 2026-02-28  
**框架版本**: 1.0 Production Ready  
**所有测试**: ✅ 3/3 通过
