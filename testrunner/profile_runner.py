import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.report_runner import run_tests

def run_profile_tests():
    return run_tests("tests/test_profile.py", "profile_report")

if __name__ == "__main__":
    run_profile_tests()
