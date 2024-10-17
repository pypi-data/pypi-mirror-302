import os

import pytest

if __name__ == "__main__":
    # pytest.main(["-k", "test_baidu"])
    pytest.main()
    os.system("allure generate temps -c -o report")
