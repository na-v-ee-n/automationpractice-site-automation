import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.report_runner import run_tests

def run_login_tests():
    return run_tests("tests/test_login.py", "login_report")

if __name__ == "__main__":
    run_login_tests()