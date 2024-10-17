import logging

import allure
import pytest
from commons.kdt import Word

logger = logging.getLogger(__name__)


@pytest.fixture
def login_page(page):
    wd = Word(page)
    """
    自定义fixture实现登录逻辑
    wd.goto("https://online.hitpaw.com/tools/v2/account.html#/login")
    wd.fill('//*[@id="loginForm_email"]', "test@hitpaw.com")
    wd.fill('//*[@id="loginForm_password"]', value="password123")
    wd.click('//*[@id="loginForm"]/div[4]/div/div/div/button')
    wd.assert_contain_text("//html/body/div[1]/div/div/div/div/div/span[2]","Login successful")
    """
    return page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
    }


def pytest_xlsx_run_step(item):
    for k, v in item.usefixtures.items():
        if "page" in k:
            page = v
            break
    else:
        raise RuntimeError("fixture 'page' is missing")
    wd = Word(page)
    step = item.current_step
    key_name = step["标记"]
    key_args = []
    for k, v in step.items():
        if "列" in k and v:
            key_args.append(v)
    else:
        logger.info(f"{key_name=},{key_args=}")
        func = getattr(wd, key_name)
        func(*key_args)
    # 自动截图
    allure.attach(page.screenshot(), f"{step['标记']}_{step['列1']}")
    return True
