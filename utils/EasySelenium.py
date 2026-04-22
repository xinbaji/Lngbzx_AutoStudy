import logging
import os
from time import strftime,localtime,sleep,time
from datetime import datetime
from selenium.common import ScreenshotException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from random import randint

class BaseEasySeleniumException(Exception):
    def __init__(self,msg):
        self.msg=msg
        Log("Error").logger.error(msg)

    def __str__(self):
        return self.msg
class NoSuchDriverException(BaseEasySeleniumException):...
class PathInvalid(BaseEasySeleniumException):...
class NoSuchCaseException(BaseEasySeleniumException):...
class NoSuchElementException(BaseEasySeleniumException):...
class ScreenshotException(BaseEasySeleniumException):...
class Log:
    def __init__(self, log_name, mode: str = "i") -> None:
        log_level = logging.DEBUG if mode == "d" else logging.INFO
        log_file_name = strftime("%Y-%m-%d", localtime())
        if not os.path.exists("./log/" + log_file_name + ".txt"):

            os.makedirs("log", exist_ok=True)
            with open("./log/" + log_file_name + ".txt", "w") as f:
                f.write("*********EasySelenium Log************\n")
                f.close()
        handler = logging.FileHandler("./log/" + log_file_name + ".txt")
        handler.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(log_level)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level=log_level)
        self.logger.addHandler(handler)
        self.logger.addHandler(console)

def only_chained_calls(func):
    def wrapper(self, *args, **kwargs):
        if self.temp_element is not None:
            result = func(self, *args, **kwargs)
            self.temp_element = None
            self.temp_locator = None
            return result
        else:
            raise NoSuchElementException("被处理的元素不存在")

    return wrapper

class Driver:

    def __init__(self) -> None:

        self.log = Log("EasySelenium", "i").logger
        
        if os.path.exists("env/browser.txt"):
            with open("env/browser.txt", "r") as f:
                driver_str=f.read()
                if driver_str not in ["chrome","edge"]:
                    driver_str = self._driver_isavailable()
        else:
            driver_str=self._driver_isavailable()

        if "chrome" in driver_str:
            __driver = Chrome
            options = ChromeOptions()
            self.log.debug("当前浏览器: Chrome")
        elif "edge" in driver_str:
            __driver = Edge
            options = EdgeOptions()
            self.log.debug("当前浏览器: Edge")
        else:
            raise NoSuchDriverException("无支持的浏览器，安装Edge或Chrome。")




        '''self.download_location = os.path.join(os.getcwd(), "download")
        self.prefs = {"download.default_directory": os.path.join(os.getcwd(), "temp")}'''

        self.prefs={}
        self.userdata_dir = os.path.join(os.getcwd(), "env")
        self.timeout_seconds = 12
        self.temp_element:WebElement = None
        self.temp_locator:tuple = None

        options.add_experimental_option("prefs", self.prefs)
        options.add_experimental_option("detach", True)
        options.add_argument("--user-data-dir=" + self.userdata_dir)
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("log-level=3")
        self.driver = __driver(options=options)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(self.timeout_seconds)
    def _driver_isavailable(self) -> str:
        driver_dict={
            "chrome":Chrome,
            "edge":Edge
        }
        for driver_str,driver_class in driver_dict.items():
            try:
                driver =driver_class()
            except Exception as e:
                self.log.error(e)
            else:
                driver.quit()
                os.makedirs("env", exist_ok=True)
                with open("env/browser.txt", "w") as f:
                    f.write(driver_str)
                return driver_str

        raise NoSuchDriverException("无支持的浏览器，安装Edge或Chrome。")


    def get(self, url):
        self.driver.get(url)

    def wait(self, path,case:str="visible", target_string="", timeout=-1):
        case_dict = {
            "visible": EC.presence_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "iframe_available": EC.frame_to_be_available_and_switch_to_it,
            "string_visible": EC.text_to_be_present_in_element,
            
        }
        if timeout < 0:
            timeout = self.timeout_seconds
        if path[0] == "#" or path[0] == ".":
            locator = (By.CSS_SELECTOR, path)
        elif path[0] == "/":
            locator = (By.XPATH, path)
        else:
            raise PathInvalid("非法的CSS或XPATH格式 Path: " + path)

        if case not in case_dict.keys():
            raise NoSuchCaseException("case错误，可用case列表: " + str(case_dict.keys()))

        for key, value in case_dict.items():
            if case == key:
                case_handler = value
                case_handler_value = locator
                break

        if case_handler == EC.text_to_be_present_in_element:
            case_handler_value = (locator, target_string)

        self.driver.implicitly_wait(timeout)

        self.log.debug("正在寻找元素: " + str(path) + " 寻找成功条件: " + str(case) + " 等待时间(秒): " + str(timeout))
        try:
            element = WebDriverWait(self.driver, timeout).until(case_handler(case_handler_value))
        except TimeoutException as e:
            self.log.error("等待元素超时")
            raise e
        else:
            self.temp_element = element
            self.temp_locator = locator
        return self

    @only_chained_calls
    def remove(self):
        self.driver.execute_script("document.querySelector('" + self.temp_locator[1] + "').remove()")

    @only_chained_calls
    def click(self):
        self.temp_element.click()

    @only_chained_calls
    def send_keys(self, keys):
        self.temp_element.send_keys(keys)

    @only_chained_calls
    def get_attribute(self, attr):
        return self.temp_element.get_attribute(attr)

    @only_chained_calls
    def get_text(self):
        return self.temp_element.text

    @only_chained_calls
    def force_click(self):
        self.driver.execute_script("arguments[0].click()", self.temp_element)

    @only_chained_calls
    def clear(self):
        self.temp_element.clear()
    @only_chained_calls
    def exist(self):
        return self.temp_element is not None
    def screenshot(self,name=None):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots",exist_ok=True)
        if name is not None:
            filename=name
        else:
            filename=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
        if len(filename)>4 and filename[-4:].lower()!=".png":
            filename+=".png"
        filepath=os.path.join(os.getcwd(),"screenshots",filename).replace("\\","/")
        self.log.debug("element: "+str(self.temp_element))
        self.log.debug("save_path: "+filepath)
        result=self.temp_element.screenshot(filepath)
        if not result:
            raise ScreenshotException("截图写入文件失败，请检查该工作目录的读写权限")
        return filepath

    

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()
    def refresh(self):
        self.driver.refresh()

    def get_page_source(self):
        return self.driver.page_source

    def switch_to_default_frame(self):
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            self.log.error("错误：" + str(e))
    def get_url(self):
        return str(self.driver.current_url)
    
    def sleep(self, seconds):
        sleep(seconds)
        
    @only_chained_calls
    def delete_event_listener(self,event:str):
        self.driver.execute_script("document.querySelector('" + self.temp_locator[1] + "').removeEventListener('"+event+"')")
    def maximize_window(self):
        self.driver.maximize_window()
    def minimize_window(self):
        self.driver.minimize_window()
    def set_window_size(self,width:int,height:int):
        self.driver.set_window_size(width,height)
    def get_current_window_size(self):
        return self.driver.get_window_size()
    def set_random_window_size(self):
        x,y=self.get_current_window_size().values()
        width=randint(x-10,x)
        height=randint(y-10,y)
        self.set_window_size(width,height)
    def switch_to_window(self,index=-1):
        success_flag=False
        if isinstance(index, int):
            if abs(index) < len(self.driver.window_handles):
                self.driver.switch_to.window(self.driver.window_handles[index])
            else:
                raise NoSuchElementException("没有对应的窗口句柄: "+str(index))
        elif isinstance(index, str):
            start_time=time()
            while True:
                current_time=time()
                if current_time-start_time>2:
                    raise NoSuchElementException("超时，没有找到对应的窗口句柄: "+index)
                    
                
                for i in self.driver.window_handles:
                    self.driver.switch_to.window(i)
                    self.log.debug("正在切换到窗口...,url: "+self.get_url()  ,  " 目标url: "+index)
                    if index in self.get_url():
                        return
                
    
if __name__ == "__main__":
    driver=Driver()
    driver.get("http://www.baidu.com")
    print(driver.get_current_window_size())

