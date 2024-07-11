import os
import re
import time
import json
import traceback
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

import ddddocr

class NotSelectCourseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class Log:
    def __init__(self) -> None:
        self.log_file=open ("log.txt","a+")
        self.log_file.write("\n")
        self.log_file.write("****************************启动******************************")    
    def writeToLogTxt(self,text):
        self.log_file.write('\n')
        self.log_file.write(text)
    def info(self,text):
        log_text="[ "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" ][Info]  "+str(text)
        print(log_text)
        self.writeToLogTxt(log_text)

    def error(self,text):
        log_text="[ "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" ][Error] "+str(text)
        print(log_text)
        self.writeToLogTxt(log_text)

    def debug(self,text):
        debug_print = 0
        log_text="[ "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" ][Debug] "+str(text)
        if debug_print == 0:
            print(log_text)
            self.writeToLogTxt(log_text)
        else:
            pass

    
class ToolKit(Log):
    def __init__(self) -> None:
        super().__init__()
    
        
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
            
    def appear_wait(self,byType,val:str,retryTime:int=10) -> WebElement:
        """等待元素出现或元素中出现目标文字，返回网页元素对象

        Args:
            byType : self.CSS or self.XPATH
            val (str): _description_
            retryTime (int, optional): 重试次数. Defaults to 10.

        Returns:
            WebElement: 元素对象
        """     
        argsDic={
            'func_name':'appear_wait',
            'type':byType,
            'val':val,
            'retryTime':retryTime,
        }   
        for i in range(0,retryTime,1):
            try:
                element=WebDriverWait(self.driver,60).until(EC.presence_of_element_located((byType,val)))
                return element
            except TimeoutException:
                self.debug("args:"+str(argsDic))
                self.error("第 "+str(i)+" 次等待超时，刷新页面 ..")
                
                self.driver.refresh()
                
        
        self.error("等待元素超时"+str(argsDic))        
        raise TimeoutException("等待元素超时"+str(argsDic))
    
    def pwdcfiiro1c(self,s):
        q=''
        for i in range(0,len(s),1):
            q+=chr(ord(s[i])-1)
        return q
    
    def usnmdcfiiro1cqqt(self,s):
        q=''
        for i in range(0,len(s),1):
            q+=chr(ord(s[i])+1)
        return q
class LAS(ToolKit):
    
    

    def __init__(self) -> None:

        super().__init__()

        self.CSS=By.CSS_SELECTOR
        self.XPATH=By.XPATH
        
        if os.path.exists('config.json') == False:
            self.config={
            'STUDY_ORDER':1,   
            "RESTART_SECONDS":60,
            'userName':"",
            'passWord':"", 
            }
            
            self.config['userName']=self.usnmdcfiiro1cqqt(input("请输入用户名：(按回车键确认)："))
            self.config['passWord']=self.usnmdcfiiro1cqqt(input("请输入密码：(按回车键确认)："))
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
            "course_mycourse":'#app > div.is_cont > div.wrapper > ul > li:nth-child(2) > div.nav_bar_title',
            "course_incompleteCourse":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_left > div > ul > li:nth-child(1) > div.text.activeText",
            "course_remainCourseNum":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.optional > div.optional_left.clearfix > div:nth-child(1) > span",
            "course_remainCoursePageInput":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.content_course > div > div.btn > div > div > div > span.el-pagination__jump > div > input",
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
        
        self.driver=webdriver.Edge()
    def getVideoPlayTime(self,timeout=120):
        retryCount=0
        while retryCount<=timeout:
            ex='\d{2}:\d{2} / \d{2}:\d{2}'
            text=self.driver.page_source
            result=re.findall(ex,text,re.S)
            '''21:08 / 45:48'''
            if len(result) != 1 :
                time.sleep(0.5)
                retryCount+=1
                continue
            if len(result[0]) != 13:
                time.sleep(0.5)
                retryCount+=1
                continue
            else:
                return result[0]
                
    def getVideoRemainingMin(self,studytime):
        if studytime[0] == '0':
            studytime=studytime[1:len(studytime)]
        if studytime[2] == '0':
            studytime=studytime[0:2]+studytime[3:len(studytime)]
        if studytime[6] == '0':
            studytime=studytime[0:6]+studytime[7:len(studytime)]
            
        '''21:08 / 45:48'''
        '''0:8 / 33:50'''
        ex='(.*?):(.*?) / (.*?):'
        result=re.findall(ex,studytime,re.S)[0]
        studyCurrentTimeMin,videoDurationMin=eval(result[0]),eval(result[2])
        remainingMin=videoDurationMin-studyCurrentTimeMin
        return remainingMin
        
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

        while True:
            self.info("识别验证码中")
            self.appear_wait(self.XPATH,self.xpath['textcode_img']).screenshot('needocr.png')
            textcode=self.ocrToCode()
            if textcode == -1:
                self.driver.find_element(By.XPATH,self.xpath['textcode_img']).click()
                time.sleep(2)
            else:
                self.info("正在输入验证码")
                self.driver.find_element(By.XPATH,self.xpath['textcode_input']).clear()
                self.driver.find_element(By.XPATH,self.xpath['textcode_input']).send_keys(textcode)
                self.appear_wait(self.XPATH,self.xpath['username_input']).clear()
                self.appear_wait(self.XPATH,self.xpath['password_input']).clear()
                qtarget=self.pwdcfiiro1c(self.config['userName'])
                self.appear_wait(self.XPATH,self.xpath['username_input']).send_keys(qtarget)
                target=self.pwdcfiiro1c(self.config['passWord'])
                self.appear_wait(self.XPATH,self.xpath['password_input']).send_keys(target)
                self.info("正在输入用户名和密码")
                self.driver.find_element(By.XPATH,self.xpath['login_button']).click()
                time.sleep(3)
                try:
                    self.driver.find_element(By.XPATH,self.xpath['login_button'])
                except NoSuchElementException:
                    self.appear_wait(self.CSS,self.css['index_studyCenter'],retryTime=3).click()
                    self.info("进入学习中心")
                    break
                else:
                    continue
        
        
        if os.path.exists("config.json") == False:
            self.info("登录成功，用户信息保存至config.json中...")
            with open("config.json","w") as f:
                    f.write(self.json_str)
                    f.close()
        else:
            self.info("登录成功!")
        
        self.appear_wait(self.XPATH,self.xpath['course_mycourse']).click()
        self.info("正在获取当前进度，请稍后...")
        remainNum_str= self.appear_wait(self.CSS,self.css['course_remainCourseNum']).text
        self.debug("检测剩余科目数："+remainNum_str)
        self.remainNum=eval(remainNum_str)
        
        if  self.remainNum == 0:
            self.error("请先选课或本次学习已完成...")
            raise NotSelectCourseError("请先选课或本次学习已完成...")
        else:
            self.info("当前有 "+str(self.remainNum)+" 节未完成学习")
        
        return self
    
    def studyCourse(self,studyorder):
        while True:
            if self.remainNum == 0:
                self.info("全部学习已完成...")
                break
            else:
                firsttitle=self.appear_wait(self.CSS,self.css['study_title']).text
                if studyorder == -1:
                    self.appear_wait(self.CSS,self.css['course_remainCoursePageInput']).send_keys('99')
                    self.appear_wait(self.CSS,self.css['course_remainCoursePageInput']).send_keys(Keys.ENTER)
                    time.sleep(0.5)
                title=self.appear_wait(self.CSS,self.css['study_title']).text
                videoPercentage=self.driver.find_element(By.CSS_SELECTOR,self.css['study_percentage']).text
                self.info("正在学习："+str(title))
                self.info("当前课程学习进度："+str(videoPercentage))
                self.info("进入播放页面开始学习...")
                self.appear_wait(self.CSS,self.css['course_study']).click()
                time.sleep(2)
                self.debug(self.driver.window_handles[0])
                self.debug(self.driver.window_handles[-1])
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.appear_wait(self.CSS,self.css['study_confirm']).click()
                
                while True:
                    try:
                        studytime=self.appear_wait(self.XPATH,self.xpath['study_videoduration'],retryTime=1).text
                        '''34:57 / 40:40'''
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
                    
                    retrytime_getstudytime=0
                    while True:
                        if retrytime_getstudytime == 120:
                            self.driver.refresh()
                            self.appear_wait(self.CSS,self.css['study_confirm']).click()
                            retrytime_getstudytime=0
                            
                        if studytime[8] == '0' and studytime[9] == '0':
                            studytime=self.getVideoPlayTime()
                            retrytime_getstudytime+=1
                            time.sleep(1)
                        else:
                            break
                        
                    self.info("当前时间/总时间："+str(studytime))
                    remainingMin=self.getVideoRemainingMin(studytime)
                    preremainingMin=remainingMin
                    retrycount = 0
                    self.info("剩余分钟： "+str(remainingMin))
                    
                    while True:
                        studytime=self.getVideoPlayTime()
                        remainingMin=self.getVideoRemainingMin(studytime)
                        if remainingMin == 0:
                            self.info("延时一分钟，等待课程结束退出...")
                            time.sleep(60)
                            self.remainNum -=1
                            self.info("开始学习下一课...")
                            break
                        else:
                            self.info("当前课程剩余时间："+str(remainingMin)+" 分钟")
                            if preremainingMin != remainingMin:
                                preremainingMin = remainingMin
                                retrycount = 0
                            else:
                                if retrycount == 6:
                                    self.error("视频加载超时，准备刷新...")
                                    break
                                else:
                                    retrycount +=1
                            
                            time.sleep(60)

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.refresh()
                    
                    break
                    

while True:
    try:
        las=LAS()
        las.login().studyCourse(las.config['STUDY_ORDER'])
        if las.remainNum == 0:
            break
    except Exception as e:
        las.driver.quit()
        las.error(traceback.format_exc())
        las.error('发生错误， '+str(las.config['RESTART_SECONDS'])+' 秒等待后重启')
        time.sleep(las.config['RESTART_SECONDS'])
    
