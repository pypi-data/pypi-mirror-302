from commons.kdt import Word


def test_baidu(page):
    wd = Word(page)
    wd.goto("https://www.baidu.com/")
    wd.assert_have_attribute('//*[@id="su"]', "value", "百度一下")
