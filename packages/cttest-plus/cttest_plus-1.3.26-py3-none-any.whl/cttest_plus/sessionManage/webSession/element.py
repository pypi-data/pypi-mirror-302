import time
from typing import Union, List, Type, Any, NoReturn

import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from cttest_plus.globalSetting import plus_setting
from cttest_plus.utils.error import AcquireElementError
from cttest_plus.utils.js import highlight_with_element
from cttest_plus.utils.logger import logger
from cttest_plus.utils.controller import OCRDiscern


def interceptor_operations(timeout):
    exception = {"e": None}
    def out(func):
        def interceptor(cls, browser: WebDriver,  locations: List, event):
            start_time = int(time.time())
            while int(time.time()) - start_time < timeout:
                browser.switch_to.default_content()
                iframes = browser.find_elements_by_tag_name('iframe')
                ele = func(cls, browser, locations, event, exception)
                if ele: return ele
                time.sleep(2)
                for iframe in iframes:
                    cls.parent_location = iframe.location
                    logger.info(f"【iframe切换】正在切换iframe查找元素")
                    browser.switch_to.frame(iframe)
                    ele = func(cls, browser, locations, event, exception)
                    if ele:
                        return ele
                    browser.switch_to.default_content()
                logger.info(f'【元素定位】元素定位失败, location={locations}, 正在进行下一次定位尝试···')
            if event == "click_if_exits":
                logger.info(f"【可见则点击】没有发现可见则点击的元素")
            elif event == "not_displayed":
                return False
            else:
                logger.error(f'【元素定位】遍历所有元素后定位失败, location={locations}')
                allure.attach(
                    body=browser.get_screenshot_as_png(),
                    name=f"【页面等待超时】locations={locations}",
                    attachment_type=allure.attachment_type.PNG
                )
                raise exception["e"]

        return interceptor
    return out


class FindElement:
    parent_location = [0, 0]

    @classmethod
    @interceptor_operations(plus_setting.TIMEOUT_SEARCH)
    def find_element(
            cls, browser: WebDriver,  locations: List, event: str, exception
    ) -> Union[Type[OCRDiscern], WebElement, List]:
        """
        通过location定位方式定位元素
        :param browser: WebDriver对象
        :param locations: [[by, location, [x, y]], []]
            by: in [OCR XPATH LINK_TEXT PARTIAL_LINK_TEXT NAME TAG_NAME CLASS_NAME CSS_SELECTOR]
            元素定位时定位的表达式 eg. XPATH的location： //input[@id='kw']
        :return: 返回元素对象或者，OCR坐标
        """
        for location in locations:
            if len(location) == 2:
                location.append(['0', '0'])
            by, value, offset = location
            try:
                if by == 'OCR':
                    return OCRDiscern.acquire_coords_by_word(browser, location)
                elif by == 'IMG':
                    return OCRDiscern.acquire_coords_by_image(browser, location)
                else:
                    by = getattr(By, by.upper())
                    browser.execute_script('window.onload')
                    ele = browser.find_element(by, value)
                    if ele.is_displayed():
                        ele.parent_location = cls.parent_location
                        cls.parent_location = [0, 0]
                        if isinstance(ele, list):
                            raise AcquireElementError(f"【元素获取】期望获取到一个元素定位，但获得了{len(ele)}个元素")
                        highlight_with_element(browser, ele)
                        logger.info(f'【元素定位】元素定位成功, location={location}, event={event}')
                        return ele
                    logger.info(f"【元素不可见】正在进行下一次定位、并等待元素可见···")
            except (NoSuchElementException, TimeoutException) as e:
                exception["e"] = e
                continue


class Element:
    "元素对象基本类型"


class Button(Element):
    @classmethod
    def click(cls, ele: Union[Type[OCRDiscern], WebElement], browser: WebDriver) -> NoReturn:
        ActionChains(browser).reset_actions()

        if isinstance(ele, WebElement):
            try:
                ele.click()
            except ElementNotInteractableException:
                if ele.is_displayed():
                    raise
                logger.warning(f"【元素点击】元素不可交互，切换到坐标点击···")
                coord, size = ele.location, ele.size
                x = coord["x"] + size['width'] / 2 + ele.parent_location[0]
                y = coord["y"] + size['height'] / 2 + ele.parent_location[1]
                logger.info(f"【坐标点击】元素坐标【{x}, {y}】")
                ActionChains(browser).move_by_offset(x, y).click().perform()

        elif issubclass(ele, OCRDiscern):
            coords = ele.coord
            logger.info(f"【坐标点击】coord={coords}")
            ActionChains(browser).move_by_offset(*coords).click().perform()
        time.sleep(1)

    @classmethod
    def right_click(cls, browser: WebDriver, ele: WebElement) -> NoReturn:
        ActionChains(browser).context_click(ele).perform()

    @classmethod
    def double_click(cls, browser: WebDriver, ele: WebElement) -> NoReturn:
        ActionChains(browser).double_click(ele).perform()

    @classmethod
    def click_if_exits(cls, ele: Union[Type[OCRDiscern], WebElement], browser: WebDriver):
        if isinstance(ele, WebElement):
            cls.click(ele, browser)
            logger.warning(f'【click_if_exits】执行存在则点击操作成功')
        elif ele and issubclass(ele, OCRDiscern) and ele.coord:
            cls.click(ele, browser)
            logger.warning(f'【click_if_exits】执行存在则点击操作成功')
        else:
            logger.warning(f'【click_if_exits】没找到元素不执行点击操作')


class Input(Element):
    @classmethod
    def input(cls, ele: WebElement, input) -> NoReturn:
        if input.startswith('Keys.'):
            key_name = input.replace('Keys.', '')
            if not hasattr(Keys, key_name):  # Keys.ENTER Keys.TAB输入
                raise Exception(f'【Keys错误】：无【{key_name}】按键')
            else:
                key_value = getattr(Keys, key_name)
                ele.send_keys(key_value)
        else:
            logger.info(f"【文本输入】：输入内容 {input}")
            ele.send_keys(input)

    @classmethod
    def clear(cls, ele: WebElement) -> NoReturn:
        ele.clear()


class _Select(Element):
    @classmethod
    def select_by_value(cls, ele: WebElement, input: Any) -> NoReturn:
        Select(ele).select_by_value(input)

    @classmethod
    def select_by_index(cls, ele: WebElement, input: int) -> NoReturn:
        Select(ele).select_by_index(input)

    @classmethod
    def select_by_text(cls, ele: WebElement, input: str) -> NoReturn:
        Select(ele).select_by_visible_text(input)


class Iframe(Element):
    @classmethod
    def switch_to(cls, browser: WebDriver, ele: WebElement) -> NoReturn:
        browser.switch_to.frame(ele)

    @classmethod
    def switch_out(cls, browser: WebDriver) -> NoReturn:
        browser.switch_to.default_content()

    @classmethod
    def switch_parent_frame(cls, browser: WebDriver) -> NoReturn:
        browser.switch_to.parent_frame()


class ElementEvent(Element):
    @classmethod
    def move_to_point(cls, browser: WebDriver, ele: WebElement, target: List[int]):
        ActionChains(browser).drag_and_drop_by_offset(ele, *target).perform()

    @classmethod
    def hold_move_to_element(cls, browser: WebDriver, ele: WebElement, target: WebElement):
        ActionChains(browser).drag_and_drop(ele, target).perform()

    @classmethod
    def move_to_element(cls, browser: WebDriver, ele: WebElement):
        ActionChains(browser).move_to_element(ele).perform()


class MouseEvent(Element):
    @classmethod
    def mouse_hover(cls, browser: WebDriver, target: WebElement):
        ActionChains(browser).move_to_element(target)

    @classmethod
    def mouse_move(cls, browser: WebDriver, target: List[int]):
        ActionChains(browser).move_by_offset(*target)


class OtherEvent(Element):
    @classmethod
    def set_tag_attr(cls, browser: WebDriver, ele: WebElement, attr: Union[str, int]):
        browser.execute_script(f"arguments[0].setAttribute('{attr[0]}', '{attr[1]}')", ele)

    @classmethod
    def get_tag_attr(cls, analyze_class, ele: WebElement, attr: List, uuid=None):
        value = ele.get_attribute(attr[0])
        analyze_class.add_variable({attr[1]: value}, uuid=uuid)

    @classmethod
    def get_css_attr(cls, analyze_class, ele: WebElement, attr: List[Union[str, int]], uuid=None):
        value = ele.value_of_css_property(attr[0])
        analyze_class.add_variable({attr[1]: value}, uuid=uuid)

    @classmethod
    def not_displayed(cls, ele):
        if ele:
            assert False, '元素不显示断言失败'
        else:
            assert True


class WindowEvent(Element):
    @classmethod
    def scroll_into_view(cls, ele: WebElement, browser: WebDriver) -> NoReturn:
        browser.execute_script("arguments[0].scrollIntoView();", ele)

    @classmethod
    def scroll_view_by_coords(cls, browser: WebDriver, target: List[int]) -> NoReturn:
        browser.execute_script(f"window.scrollBy({target[0]}, {target[1]});")

    @classmethod
    def scroll_view_by_percentage(cls, browser: WebDriver, target: List[int]) -> NoReturn:
        width, height = browser.get_window_size()
        x = target[0]*width
        y = target[1]*height
        browser.execute_script(f"window.scrollBy({x}, {y});")

    @classmethod
    def switch_to_new_window(cls, browser: WebDriver) -> NoReturn:
        times = 3
        have_switch = False
        while times:
            time.sleep(1)
            current_window = browser.current_window_handle
            all_handler = browser.window_handles
            if all_handler[-1] != current_window:
                browser.switch_to.window(all_handler[-1])
                have_switch = True
                logger.info(f"【窗口切换】···新窗口切换成功···")
                break
            times -= 1
        if not have_switch:
            logger.info(f"【窗口切换】···新窗口切换失败···")
        cls.window = 1

    @classmethod
    def open(cls, browser: WebDriver, url):
        time.sleep(1)
        browser.get(url)


class CompatElement(Element):
    """兼容cttest1版本"""

    @classmethod
    def ele_exits(cls):
        assert True

    @classmethod
    def text_exits(cls, ele: WebElement, attr):
        assert attr in ele.text, f"'{ele.text}'不包含'{attr}'"

    @classmethod
    def useless(cls):
        assert True

    @classmethod
    def switch_to_default_tab(cls, browser: WebDriver):
        handlers = browser.window_handles
        browser.switch_to.window(handlers[0])

    @classmethod
    def swipe_screen(cls, browser, input):
        """

        :param browser:
        :param input: ['up/down/left/right', 'int(5)']
        :return:
        """
        pass
        # time.sleep(5)
        # direction, count = input
        # if type(count) == str:
        #     try:
        #         count = float(count)
        #     except:
        #         count = 1
        # start_x, start_y, end_x, end_y, _, _ = cls._gen_swipe_args(browser, direction, count)
        # num = 0
        # while num < count:
        #     logger.info(f"【屏幕滑动】执行第 {num} 次屏幕滑动")
        #     browser.swipe(start_x, start_y, end_x, end_y)
        #     num += 1

        # raise AcquireElementError(
        #     f"【元素动作】'swipe_screen' not support in cttest2, please use 'scroll_into_view' instead"
        # )

    @classmethod
    def get_elm_text(cls, ele, attr, analyze_class, uuid):
        logger.warning(f'【参数使用】please use "get_tag_attr" instead of get_elm_text')
        analyze_class.add_variable({attr: ele.text}, uuid=uuid)

    @classmethod
    def _gen_swipe_args(cls, browser, direction='down', max_swipe_screen_count=3.0):
        '''
        生成滑动屏幕参数
        :param direction: 滑动方向 up/down/left/right
        :param max_swipe_screen_count: 滑动屏幕距离
        :return: start_x, start_y, end_x, end_y, swipe_step, swipe_total_distance
        '''
        window_size_info = browser.get_window_size()
        x, y = window_size_info['width'], window_size_info['height']

        start_x = start_y = end_x = end_y = 0
        swipe_step, swipe_total_distance = 100, 2000
        # 向上滑动，y坐标减小
        if direction == 'up':
            start_x, start_y, end_x, end_y = x / 2, y / 2, x / 2, y / 3
            swipe_step, swipe_total_distance = y / 2 - y / 3, y * max_swipe_screen_count
        # 向上滑动，y坐标增大
        elif direction == 'down':
            start_x, start_y, end_x, end_y = x / 2, y / 3, x / 2, y * 5 / 6
            swipe_step, swipe_total_distance = y * 5 / 6 - y / 3, y * max_swipe_screen_count
        # 向左滑动，x坐标减小
        elif direction == 'left':
            start_x, start_y, end_x, end_y = x / 2, y / 2, x / 3, y / 2
            swipe_step, swipe_total_distance = x / 2 - x / 3, x * max_swipe_screen_count
        # 向右滑动，x坐标增大
        elif direction == 'right':
            start_x, start_y, end_x, end_y = x / 3, y / 2, x / 2, y / 2
            swipe_step, swipe_total_distance = x / 2 - x / 3, x * max_swipe_screen_count

        return start_x, start_y, end_x, end_y, swipe_step, swipe_total_distance


class CTElement(_Select, Button, Iframe, Input, MouseEvent, WindowEvent, CompatElement, ElementEvent, OtherEvent):
    """元素对象处理 """
