from selenium import webdriver
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.remote.webelement import WebElement
from utils.log import Log
import time
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import shutil

class Driver:
    
    def __init__(self) -> None:
        self.log=Log('selenium','i')
        '''target_path=os.path.join(os.getcwd(),'utils\\')
        driver_exe = target_path+"msedgedriver.exe"
        if not os.path.exists('./utils/msedgedriver.exe'):
            self.log.info("未安装浏览器驱动，正在下载...")
            driver_path=EdgeChromiumDriverManager().install()
            shutil.copy(driver_path,target_path)
        
        self.driver=webdriver.Edge(service=EdgeService(executable_path=driver_exe))'''
        self.driver=webdriver.Edge()
        self.driver.set_page_load_timeout(10)
        

    def wait_to_be_visible(self,locator,retryTime:int=10):
        """等待元素出现或元素中出现目标文字，返回网页元素对象

        Args:
            locator : union (By.selector,path)
            retryTime (int, optional): 重试次数. Defaults to 10.

        Returns:
            WebElement: 元素对象
        """     
        argsDic={
            'func_name':'appear_wait',
            'locator':locator,
            'retryTime':retryTime
        }   
        for i in range(0,retryTime,1):
            try:
                element=WebDriverWait(self.driver,60).until(EC.presence_of_element_located(locator))
                return element
            except TimeoutException:
                self.log.debug("args:"+str(argsDic))
                self.log.error("第 "+str(i+1)+" 次等待超时，刷新页面 ..")
                
                self.driver.refresh()
                
        
        self.log.error("等待元素超时"+str(argsDic))        
        raise TimeoutException("等待元素超时"+str(argsDic))
    
    def get(self,url):
        try:
            self.driver.get(url)
        except TimeoutException:
            pass
        
    def remove_elements(self,elements_list:list[str]):
        for i in elements_list:
            self.driver.execute_script("document.querySelector(\'"+i+"\').remove()")
            
    def find_element(self,locator):
        return self.driver.find_element(locator[0],locator[1])
    
    def switch_to_last_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
    def close(self):
        self.driver.close()
        
    def refresh(self):
        self.driver.refresh()
        
    def get_page_source(self):
        return self.driver.page_source