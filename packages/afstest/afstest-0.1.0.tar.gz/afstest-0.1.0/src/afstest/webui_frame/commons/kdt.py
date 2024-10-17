from playwright.sync_api import Page, expect


class Word:
    """
    locator操作
    https://playwright.dev/python/docs/actionability
    """

    def __init__(self, page: Page):
        self.page = page

    def __getattr__(self, item):
        if item.startswith("assert_"):
            if item not in self.__dict__:
                self._assert_func = item.replace("assert_", "")
                return self._assert

    def _assert(self, *args):
        """
        支持所有locator所有断言
        https://playwright.dev/python/docs/test-assertions
        eg: assert_to_have_text(selector,expected)
        """
        exp = expect(self.page.locator(args[0]))
        getattr(exp, self._assert_func)(*args[1:])

    def goto(self, url):
        """页面跳转"""
        self.page.goto(url)

    def click(self, selector, click_count=1):
        """点击元素"""
        self.page.click(selector, click_count=click_count)

    def fill(self, selector, value):
        """输入内容"""
        self.page.fill(selector, value)

    def set_input_files(self, selector, files):
        """上传文件<input type="file">"""
        self.page.set_input_files(selector, files)

    def wait_for_selector(self, selector, timeout=10):
        """等待selector"""
        self.page.wait_for_selector(selector, timeout=timeout * 1000)

    def wait_for_timeout(self, timeout):
        """固定等待"""
        self.page.wait_for_timeout(timeout=timeout * 1000)

    def evaluate(self, expression):
        """执行js脚本"""
        return self.page.evaluate(expression)

    def assert_contain_text(self, selector, expected):
        """断言selector包含文本"""
        expect(self.page.locator(selector)).to_contain_text(expected)

    def assert_not_contain_text(self, selector, expected):
        """断言selector不包含文本"""
        expect(self.page.locator(selector)).not_to_contain_text(expected)

    def assert_have_attribute(self, selector, name, value):
        """断言selector有属性值"""
        expect(self.page.locator(selector)).to_have_attribute(name, value)

    def assert_not_have_attribute(self, selector, name, value):
        """断言selector没有属性值"""
        expect(self.page.locator(selector)).not_to_have_attribute(name, value)
