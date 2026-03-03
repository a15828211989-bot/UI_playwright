#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Allure 报告解析和HTML生成
功能：不依赖allure命令行工具，直接解析allure-results生成HTML报告
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import webbrowser

class AllureReportGenerator:
    """生成Allure风格的HTML报告"""
    
    def __init__(self, results_dir: str, output_dir: str):
        self.results_dir = Path(results_dir)
        self.output_dir = Path(output_dir)
        self.results = []
        self.categories = {}
        self.statistics = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'broken': 0
        }
    
    def load_results(self):
        """加载allure结果"""
        if not self.results_dir.exists():
            print(f"❌ 结果目录不存在: {self.results_dir}")
            return False
        
        # 加载*-result.json文件
        result_files = sorted(self.results_dir.glob("*-result.json"))
        
        if not result_files:
            print(f"⚠️ 未找到result文件")
            return False
        
        print(f"📂 加载 {len(result_files)} 个结果文件...")
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.results.append(data)
                    self.statistics['total'] += 1
                    
                    # 统计测试状态
                    status = data.get('status', 'unknown')
                    if status == 'passed':
                        self.statistics['passed'] += 1
                    elif status == 'failed':
                        self.statistics['failed'] += 1
                    elif status == 'skipped':
                        self.statistics['skipped'] += 1
                    elif status == 'broken':
                        self.statistics['broken'] += 1
            except Exception as e:
                print(f"⚠️ 加载文件失败 {result_file}: {e}")
                continue
        
        print(f"✅ 加载成功: 总计 {self.statistics['total']} 个测试")
        print(f"   通过: {self.statistics['passed']} | 失败: {self.statistics['failed']} | " +
              f"跳过: {self.statistics['skipped']} | 错误: {self.statistics['broken']}")
        
        return True
    
    def generate_html(self):
        """生成HTML报告"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        html = self._build_html()
        
        report_file = self.output_dir / "index.html"
        report_file.write_text(html, encoding='utf-8')
        
        print(f"✅ 报告已生成: {report_file}")
        return report_file
    
    def _build_html(self) -> str:
        """构建HTML内容"""
        
        # 计算通过率
        pass_rate = (self.statistics['passed'] / self.statistics['total'] * 100) if self.statistics['total'] > 0 else 0
        
        # 生成测试用例HTML
        tests_html = ""
        for result in self.results:
            tests_html += self._build_test_row(result)
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Allure 测试报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .statistics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f9f9f9;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .stat-box {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .stat-box.passed {{
            border-left-color: #4caf50;
        }}
        
        .stat-box.failed {{
            border-left-color: #f44336;
        }}
        
        .stat-box.skipped {{
            border-left-color: #ff9800;
        }}
        
        .stat-box.broken {{
            border-left-color: #9c27b0;
        }}
        
        .stat-box.total {{
            border-left-color: #2196f3;
        }}
        
        .stat-number {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #666;
        }}
        
        .pass-rate {{
            font-size: 14px;
            color: #999;
            margin-top: 10px;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .tests-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .tests-table thead {{
            background: #f5f5f5;
            border-bottom: 2px solid #ddd;
        }}
        
        .tests-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #333;
        }}
        
        .tests-table td {{
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .tests-table tr:hover {{
            background: #f9f9f9;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .status-badge.passed {{
            background: #c8e6c9;
            color: #2e7d32;
        }}
        
        .status-badge.failed {{
            background: #ffcdd2;
            color: #c62828;
        }}
        
        .status-badge.skipped {{
            background: #ffe0b2;
            color: #e65100;
        }}
        
        .status-badge.broken {{
            background: #f3e5f5;
            color: #6a1b9a;
        }}
        
        .test-name {{
            color: #333;
            font-weight: 500;
        }}
        
        .test-details {{
            font-size: 12px;
            color: #999;
            margin-top: 5px;
        }}
        
        .duration {{
            color: #666;
            font-size: 13px;
        }}
        
        .footer {{
            background: #f9f9f9;
            padding: 20px 30px;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 12px;
            text-align: center;
        }}
        
        h2 {{
            color: #333;
            font-size: 18px;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Allure 测试报告</h1>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="statistics">
            <div class="stat-box total">
                <div class="stat-number">{self.statistics['total']}</div>
                <div class="stat-label">总测试数</div>
            </div>
            <div class="stat-box passed">
                <div class="stat-number">{self.statistics['passed']}</div>
                <div class="stat-label">通过</div>
            </div>
            <div class="stat-box failed">
                <div class="stat-number">{self.statistics['failed']}</div>
                <div class="stat-label">失败</div>
            </div>
            <div class="stat-box skipped">
                <div class="stat-number">{self.statistics['skipped']}</div>
                <div class="stat-label">跳过</div>
            </div>
            <div class="stat-box broken">
                <div class="stat-number">{self.statistics['broken']}</div>
                <div class="stat-label">错误</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{pass_rate:.1f}%</div>
                <div class="stat-label">通过率</div>
            </div>
        </div>
        
        <div class="content">
            <h2>📋 测试用例详情</h2>
            <table class="tests-table">
                <thead>
                    <tr>
                        <th style="width: 40%">测试用例</th>
                        <th style="width: 15%">状态</th>
                        <th style="width: 25%">用时</th>
                        <th style="width: 20%">详情</th>
                    </tr>
                </thead>
                <tbody>
                    {tests_html}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>生成工具: UI Playwright Testing Framework | 
            <a href="https://docs.qameta.io/allure/" target="_blank">Allure Framework</a></p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _build_test_row(self, result: Dict[str, Any]) -> str:
        """构建单个测试行的HTML"""
        name = result.get('name', 'Unknown')
        status = result.get('status', 'unknown')
        start_time = result.get('start', 0)
        stop_time = result.get('stop', start_time)
        duration_ms = stop_time - start_time if stop_time and start_time else 0
        duration_sec = duration_ms / 1000 if duration_ms else 0
        
        # 格式化时间
        if duration_sec < 1:
            duration_str = f"{int(duration_ms)}ms"
        elif duration_sec < 60:
            duration_str = f"{duration_sec:.2f}s"
        else:
            minutes = int(duration_sec // 60)
            seconds = int(duration_sec % 60)
            duration_str = f"{minutes}m {seconds}s"
        
        # 获取参数信息
        test_class = result.get('testCaseId', '').split('::')[0] if '::' in result.get('testCaseId', '') else ''
        parameters = result.get('parameters', [])
        param_str = f"[{', '.join([p.get('name', '') for p in parameters])}]" if parameters else ""
        
        # 获取失败信息
        failure_info = ""
        failures = result.get('steps', [])
        for step in failures:
            if step.get('status') == 'failed':
                failure_info = step.get('name', 'Unknown failure')[:100]
                break
        
        return f"""
                    <tr>
                        <td>
                            <div class="test-name">{name} {param_str}</div>
                            <div class="test-details">{test_class}</div>
                        </td>
                        <td>
                            <span class="status-badge {status}">{status.upper()}</span>
                        </td>
                        <td>
                            <div class="duration">{duration_str}</div>
                        </td>
                        <td>
                            <div class="test-details">{failure_info}</div>
                        </td>
                    </tr>
"""

def main():
    """主函数"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="生成Allure HTML报告")
    parser.add_argument("--results", default="reports/allure-results",
                       help="allure结果目录")
    parser.add_argument("--output", default="reports/allure-report",
                       help="报告输出目录")
    parser.add_argument("--open", action="store_true", default=True,
                       help="自动打开报告")
    
    args = parser.parse_args()
    
    print("🚀 开始生成Allure HTML报告...\n")
    
    generator = AllureReportGenerator(args.results, args.output)
    
    if not generator.load_results():
        print("❌ 加载结果失败")
        sys.exit(1)
    
    report_file = generator.generate_html()
    
    if args.open:
        print(f"\n🌐 在浏览器中打开报告...")
        webbrowser.open(f"file:///{report_file.absolute()}")
    else:
        print(f"\n📊 报告地址: file:///{report_file.absolute()}")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
