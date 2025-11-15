import pytest
import os
import shutil

def run_tests(test_path, report_name="test_report"):
    """Unified test runner with HTML and Allure reporting"""
    os.makedirs("reports", exist_ok=True)
    
    if os.path.exists("allure-results"):
        shutil.rmtree("allure-results")
    
    report_file = f"reports/{report_name}.html"
    exit_code = pytest.main([
        test_path,
        f"--html={report_file}",
        "--self-contained-html",
        "--alluredir=allure-results",
        "-v"
    ])
    
    print(f"\n{'='*50}")
    print(f"Tests {'COMPLETED' if exit_code == 0 else 'FAILED'}")
    print(f"Report: {report_file}")
    print(f"{'='*50}")
    
    return exit_code
