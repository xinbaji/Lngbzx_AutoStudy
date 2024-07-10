from selenium import webdriver
import time
import os
import re
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
import ddddocr

class NotSelectCourseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Log:
    def __init__(self) -> None:
        pass

    def info(self,text):
        print("[info]"+str(text))

    def error(self,text):
        print("[error]"+str(text))

    def debug(self,text):
        debug_mode = 0

        if debug_mode == 0:
            print("[debug]"+str(text))
        else:
            pass

    
class ToolKit(Log):
    def __init__(self) -> None:
        super().__init__()
    
        self.driver=webdriver.Edge()
        self.ocr=ddddocr.DdddOcr()

    def ocrToCode(self) -> str:
        image = open("needocr.png", "rb").read()
        result = self.ocr.classification(image)
        self.debug("result:"+str(result))
        if len(result) != 4:
            self.info("未识别到结果，重新检测")
            return -1
        for i in result:
            if i.isdigit() == False:
                self.info("未识别到结果，重新检测")
                return -1
        code=str(result)
        self.info("当前验证码为："+code)
        return code
            
    def appear_wait(self,byType,val:str,retryTime:int=3,word:str='-1') -> WebElement:
        """等待元素出现或元素中出现目标文字，返回网页元素对象

        Args:
            byType : self.CSS or self.XPATH
            val (str): _description_
            retryTime (int, optional): 重试次数. Defaults to 3.
            word (str, optional): 目标文字. Defaults to None.

        Returns:
            WebElement: 元素对象
        """        
        for i in range(0,retryTime,1):
            try:
                locator=(byType,val)
                element=WebDriverWait(self.driver,60).until(EC.presence_of_element_located(locator))
                if word != '-1':
                    
                    element=WebDriverWait(self.driver,60).until(EC.text_to_be_present_in_element(locator,word))
                return element
            except TimeoutException:
                self.debug("刷新页面")
                self.driver.refresh()
                
        argsDic={
            'func_name':'appear_wait',
            'type':type,
            'val':val,
            'retryTime':retryTime,
            'word':word
        }        
        raise TimeoutException("等待元素超时，程序退出。"+str(argsDic))

class LAS(ToolKit):
    
    CSS=By.CSS_SELECTOR
    XPATH=By.XPATH

    def __init__(self) -> None:

        super().__init__()

        if os.path.exists('config.json') == False:
            self.config={
            'userName':"",
            'passWord':"", 
            }
            self.config['userName']=input("请输入用户名：(按回车键确认)：")
            self.config['passWord']=input("请输入密码：(按回车键确认)：")
            self.json_str=json.dumps(self.config)
            
        else:
            with open ('config.json','r') as f:
                self.config=json.load(f)
                f.close()

        
        self.url={
            "index":"https://zyjstest.lngbzx.gov.cn/",
        }
        self.xpath={
            "index_info":"/html/body/div[3]",
            "index_black":'/html/body/div[4]',
            "index_infoConfirm":"/html/body/div[3]/div/div[3]/button",
            "username_input":'//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div/div[1]/form[1]/div[1]/div/div/input',
            "password_input":'//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div/div[1]/form[1]/div[2]/div/div/input',
            "textcode_input":'//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div/div[1]/form[1]/div[3]/div/div/input',
            "login_button":'//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div/div[1]/form[1]/div[4]/div/button',
            "textcode_img":'//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div/div[1]/form[1]/div[3]/div/img',
            "study_videoduration":'//*[@id="app"]/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[8]',
            "study_confirmbutton":'//*[@id="app"]/div[2]/div[5]/div/div[3]/span/button',
            "course_mycourse":'//*[@id="app"]/div[2]/div[2]/ul/li[2]/div[1]'
            }
        
        self.css={
            "textcode_new":"body > img",
            "index_infoButtonWord":'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button',
            "index_infoWord":'body > div.el-message-box__wrapper > div > div.el-message-box__header > div > span',
            "index_studyCenter":"#app > div.is_cont > div > div > div.banner_info > div.login_info.fr > div > div.category > div:nth-child(1)",
            "course_mycourse":'#app > div.is_cont > div.wrapper > ul > li.nav_bar.active > div.nav_bar_title',
            "course_incompleteCourse":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_left > div > ul > li:nth-child(1) > div.text.activeText",
            "course_remainCourseNum":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.optional > div.optional_left.clearfix > div:nth-child(1) > span",
            "course_study":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.content_course > div > ul > li:nth-child(1) > div:nth-child(1) > div > div.course_list_right > div.course_list_right_timer > div.antClick.clearfix > div > div.Save",
            "course_cancel":'#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.content_course > div > ul > li:nth-child(1) > div:nth-child(1) > div > div.course_list_right > div.course_list_right_timer > div.antClick.clearfix > div > div.Cancel',
            "course_cancelConfirm":"body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary",
            "course_checkcomplete":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.optional > div.optional_left.clearfix > div:nth-child(1)",
            "study_confirmWord":"#app > div.bodys.is_cont > div:nth-child(5) > div > div.el-dialog__footer > span > button > span",
            "study_confirm":"#app > div.bodys.is_cont > div:nth-child(5) > div > div.el-dialog__footer > span > button",
            "study_videoduration":"#app > div.bodys.is_cont > div.video_center > div > div.video_box.wrapper > div.player > div > div.controlbarchtrsoygjdbz > div.timetextchtrsoygjdbz",
            "study_percentage":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.content_course > div > ul > li:nth-child(1) > div.foter > div > div.el-progress__text",
            "study_title":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.content_course > div > ul > li:nth-child(1) > div:nth-child(1) > div > div.course_list_right > div.course_list_right_title.oneEllipsis",
            }

    def login(self):

        self.driver.set_page_load_timeout(10)
        try:
            self.driver.get(self.url['index'])
        except TimeoutException as te:
            pass
        
        self.appear_wait(self.CSS,self.css['index_infoButtonWord'])
        elementRemove=['body > div.el-message-box__wrapper','body > div.v-modal','.right_service1','.right_service2','.right_service3','.right_service4','.right_service5']
        for i in elementRemove:
            self.driver.execute_script("document.querySelector(\'"+i+"\').remove()")
        
        self.appear_wait(self.XPATH,self.xpath['username_input']).send_keys(self.config['userName'])
        self.appear_wait(self.XPATH,self.xpath['password_input']).send_keys(self.config['passWord'])
        self.debug("输入用户名和密码")

        while True:
            self.debug("识别验证码")
            #截图获取验证码
            self.driver.find_element(By.XPATH,self.xpath['textcode_img']).screenshot('needocr.png')
            textcode=self.ocrToCode()
            if textcode == -1:
                self.driver.find_element(By.XPATH,self.xpath['textcode_img']).click()
                time.sleep(2)
            else:
                self.debug("输入验证码")
                self.driver.find_element(By.XPATH,self.xpath['textcode_input']).send_keys(textcode)
                self.driver.find_element(By.XPATH,self.xpath['login_button']).click()
                break

        self.appear_wait(self.CSS,self.css['index_studyCenter'],word='学习中心').click()
        
        self.info("登录成功，用户信息保存至config.json中...")
        if os.path.exists("config.json") == False:
            with open("config.json","w") as f:
                    f.write(self.json_str)
                    f.close()
        
        self.appear_wait(self.XPATH,self.css['course_mycourse'],word='我的课程')
        self.info("正在获取当前进度，请稍后...")
        self.remainNum=eval(self.appear_wait(self.CSS,self.css['course_remainCourseNum']).text)
        
        if  self.remainNum == 0:
            #self.error("请先选课或本次学习已完成...")
            raise NotSelectCourseError("请先选课或本次学习已完成...")
        else:
            self.info("当前有 "+str(self.remainNum)+" 节未完成学习")
        
        return self
    
    def studyCourse(self):
        while True:
            if self.remainNum == 0:
                self.info("全部学习已完成...")
                break
            else:
                title=self.appear_wait(self.CSS,self.css['study_title']).text
                videoPercentage=self.driver.find_element(By.CSS_SELECTOR,self.css['study_percentage']).text
                self.info("正在学习："+str(title))
                self.info("当前课程学习进度："+str(videoPercentage))
                self.info("进入播放页面开始学习...")
                self.driver.find_element(By.CSS_SELECTOR,self.css['course_study']).click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.appear_wait(self.XPATH,self.xpath['study_confirmbutton']).click()
                
                while True:
                    try:
                        studytime=self.appear_wait(self.XPATH,self.xpath['study_videoduration']).text
                    except StaleElementReferenceException as sere:
                        self.error("加载不了，这是一个坏课。我要删掉哦")
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.driver.refresh()

                        self.appear_wait(self.CSS,self.css['study_title'])
                        self.driver.find_element(By.CSS_SELECTOR,self.css['course_cancel']).click()
                        self.appear_wait(self.CSS,self.css['course_cancelConfirm'])
                        self.driver.find_element(By.CSS_SELECTOR,self.css['course_cancelConfirm']).click()
                        time.sleep(2)
                        self.driver.refresh()
                        break

                    if studytime[0] == '0':
                        studytime=studytime[1:len(studytime)]
                    if studytime[2] == '0':
                        studytime=studytime[0:2]+studytime[3:len(studytime)]
                    if studytime[6] == '0':
                        if studytime[7] == '0':
                            self.error("视频时间检测失败")
                        studytime=studytime[0:6]+studytime[7:len(studytime)]
                        
                    self.info("当前时间，总时间:"+studytime)
                    '''21:08 / 45:48'''
                    '''0:8 / 33:50'''
                    ex='(.*?):(.*?) / (.*?):'
                    result=re.findall(ex,studytime,re.S)[0]
                    studyCurrentTimeMin,videoDurationMin=eval(result[0]),eval(result[2])
                    remainingMin=videoDurationMin-studyCurrentTimeMin
                    self.debug("剩余分钟： "+str(remainingMin))
                    realremainingMin=remainingMin+1
                    for i in range(0,remainingMin+1,1):
                        if realremainingMin == 1:
                            self.info("延时一分钟，等待课程结束退出...")
                        else:
                            self.info("当前课程剩余时间："+str(realremainingMin)+" 分钟")
                        time.sleep(60)
                        realremainingMin -= 1

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.refresh()
                    break
                    
las=LAS()
las.login().studyCourse()
    