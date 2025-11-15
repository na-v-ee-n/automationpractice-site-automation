import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    pytest.main([
        "tests/test_cart.py",
        "-v",
        "-s",
        "--log-cli-level=INFO",
        "--alluredir=reports/allure-results",
        "--html=reports/cart_report.html",
        "--self-contained-html"
    ])
