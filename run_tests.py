"""
测试运行脚本
功能：运行测试并自动生成Allure可视化报告
"""
import os
import sys
import subprocess
import argparse
import webbrowser
from pathlib import Path
from utils.logger import get_logger

# 导入Allure HTML生成器
sys.path.insert(0, str(Path(__file__).parent))
from allure_html_generator import AllureReportGenerator

logger = get_logger(__name__)

def run_pytest(test_path: str = None, 
               markers: str = None, 
               workers: int = 1,
               html_report: bool = True,
               allure_report: bool = True,
               clean_allure: bool = True) -> bool:
    """
    运行pytest测试
    
    Args:
        test_path: 测试路径
        markers: 测试标记
        workers: 并行worker数量
        html_report: 是否生成HTML报告
        allure_report: 是否生成Allure报告
        clean_allure: 是否清理旧的Allure结果
        
    Returns:
        测试是否成功
    """
    # 构建命令
    cmd = ["pytest"]
    
    # 添加测试路径
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    # 添加标记
    if markers:
        cmd.extend(["-m", markers])
    
    # 添加并行执行
    if workers > 1:
        cmd.extend(["-n", str(workers), "--dist", "loadscope"])
    
    # 添加HTML报告
    if html_report:
        cmd.extend(["--html", "reports/pytest_report.html", "--self-contained-html"])
    
    # 添加Allure报告
    if allure_report:
        cmd.extend(["--alluredir", "reports/allure-results"])
        if clean_allure:
            cmd.append("--clean-alluredir")
    
    # 添加其他选项
    cmd.extend(["-v", "--tb=short", "--disable-warnings"])
    
    logger.info(f"运行命令: {' '.join(cmd)}")
    
    # 运行测试
    result = subprocess.run(cmd)
    
    return result.returncode == 0

def generate_allure_report(open_report: bool = False):
    """
    生成Allure报告（使用HTML生成器）
    
    Args:
        open_report: 是否自动打开报告
    """
    results_dir = "reports/allure-results"
    output_dir = "reports/allure-report"
    
    if not Path(results_dir).exists():
        logger.error(f"Allure结果目录不存在: {results_dir}")
        return False
    
    try:
        logger.info("生成Allure HTML报告...")
        generator = AllureReportGenerator(results_dir, output_dir)
        
        # 加载测试结果
        if not generator.load_results():
            logger.error("加载测试结果失败")
            return False
        
        # 生成HTML报告
        report_file = generator.generate_html()
        logger.info(f"✅ Allure报告已生成: {report_file}")
        
        # 打开报告
        if open_report:
            logger.info("在浏览器中打开报告...")
            webbrowser.open(f"file:///{report_file.absolute()}")
        
        return True
        
    except Exception as e:
        logger.error(f"生成报告失败: {e}")
        return False

def run_specific_test(test_name: str):
    """
    运行特定测试
    
    Args:
        test_name: 测试名称或路径
    """
    logger.info(f"运行特定测试: {test_name}")
    
    cmd = ["pytest", test_name, "-v", "--tb=short"]
    result = subprocess.run(cmd)
    
    return result.returncode == 0

def install_playwright_browsers():
    """
    安装Playwright浏览器
    """
    logger.info("安装Playwright浏览器...")
    
    cmd = ["playwright", "install", "chromium", "--with-deps"]
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        logger.info("Playwright浏览器安装成功")
    else:
        logger.error("Playwright浏览器安装失败")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="UI自动化测试运行器")
    
    # 添加参数
    parser.add_argument("--test", "-t", help="运行特定测试文件或测试用例")
    parser.add_argument("--markers", "-m", help="运行指定标记的测试")
    parser.add_argument("--workers", "-n", type=int, default=1, help="并行worker数量")
    parser.add_argument("--no-html", action="store_true", help="不生成HTML报告")
    parser.add_argument("--no-allure", action="store_true", help="不生成Allure报告")
    parser.add_argument("--no-open", action="store_true", help="生成报告但不自动打开")
    parser.add_argument("--install-browsers", action="store_true", help="安装Playwright浏览器")
    parser.add_argument("--list-tests", action="store_true", help="列出所有测试")
    
    args = parser.parse_args()
    
    # 安装浏览器
    if args.install_browsers:
        install_playwright_browsers()
        return
    
    # 列出测试
    if args.list_tests:
        cmd = ["pytest", "--collect-only", "-q"]
        subprocess.run(cmd)
        return
    
    # 运行测试
    success = False
    
    if args.test:
        success = run_specific_test(args.test)
    else:
        success = run_pytest(
            markers=args.markers,
            workers=args.workers,
            html_report=not args.no_html,
            allure_report=not args.no_allure
        )
    
    # 生成并打开Allure报告（如果没有禁用）
    if not args.no_allure:
        open_report = not args.no_open  # 默认打开，除非指定--no-open
        logger.info("\n" + "="*60)
        logger.info("正在生成Allure可视化报告...")
        logger.info("="*60)
        generate_allure_report(open_report=open_report)
    
    # 退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()