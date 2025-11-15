from utils.report_runner import run_tests

def run_all_tests():
    return run_tests("tests/", "all_tests_report")

if __name__ == "__main__":
    run_all_tests()