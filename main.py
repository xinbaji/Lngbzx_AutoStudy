from utils.log import Log
from utils.ocr import Ocr
from utils.selenium import Driver
from utils.selenium import NoSuchElementException,StaleElementReferenceException
from data.path import Xpath,Css,Url
from config.config import Config
from time import sleep
import traceback

import os
import re

class Las:
    def __init__(self) -> None:
        self.log=Log('las','d')
        self.log.info("__________ 辽宁干部学习网刷课程序 Created by Xinbaji __________")
        
        self.config=Config()
        self.ocr=Ocr()
        self.driver = Driver()
        
        self.xpath=Xpath()
        self.css=Css()
        self.url=Url()
        
    def login(self):
        self.driver.get(self.url.index())
        self.driver.wait_to_be_visible(self.css.index_infoButtonWord())
        elementRemove=['body > div.el-message-box__wrapper','body > div.v-modal','.right_service1','.right_service2','.right_service3','.right_service4','.right_service5']
        self.driver.remove_elements(elementRemove)
        
        while True:
            self.log.info("识别验证码中...")
            self.driver.wait_to_be_visible(self.xpath.textcode_img()).screenshot('./img/needocr.png')
            textcode=self.ocr.ocr_verifycode()
            if not textcode :
                self.driver.find_element(self.xpath.textcode_img()).click()
                sleep(2)
            else:
                self.log.info("正在输入验证码...")
                self.driver.find_element(self.xpath.textcode_input()).clear()
                self.driver.find_element(self.xpath.textcode_input()).send_keys(textcode)
                self.driver.wait_to_be_visible(self.xpath.username_input()).clear()
                self.driver.wait_to_be_visible(self.xpath.password_input()).clear()
                self.log.info("正在输入用户名和密码...")
                self.driver.wait_to_be_visible(self.xpath.username_input()).send_keys(self.config.username())
                self.driver.wait_to_be_visible(self.xpath.password_input()).send_keys(self.config.password())
                self.driver.find_element(self.xpath.login_button()).click()
                sleep(3)
                try:
                    self.driver.find_element(self.xpath.login_button())
                except NoSuchElementException:
                    self.driver.wait_to_be_visible(self.css.index_studyCenter(),retryTime=3).click()
                    self.log.info("成功进入学习中心...")
                    break
                else:
                    continue
                
        if os.path.exists("./config/config.json") == False:
            self.log.info("登录成功，用户信息保存至config.json中...")        
            self.config.save_to_config_file()
        else:
            self.log.info("登录成功！")
        
        self.driver.wait_to_be_visible(self.xpath.course_mycourse()).click()    
        self.log.info("正在获取当前进度，请稍后...")
        remainNum_str= self.driver.wait_to_be_visible(self.css.course_remainCourseNum()).text
        self.log.info("检测剩余科目数："+remainNum_str)
        self.remainNum=eval(remainNum_str)
        
        if  self.remainNum == 0:
            self.log.error("请先选课或本次学习已完成...")
            raise Exception("请先选课或本次学习已完成...")
        else:
            self.log.info("当前有 "+str(self.remainNum)+" 节未完成学习")
        
        return self 
        
    def study_course(self,study_order):
        while True:
            if self.remainNum == 0:
                self.log.info("全部学习已完成...")
                break
            else:
                self.driver.wait_to_be_visible(self.css.study_title())
                if study_order == -1:
                    self.driver.wait_to_be_visible(self.css.course_remainCoursePageInput()).send_keys('99'+"\ue007")
                    sleep(0.5)
                title=self.driver.wait_to_be_visible(self.css.study_title()).text
                videoPercentage=self.driver.find_element(self.css.study_percentage()).text
                self.log.info("正在学习："+str(title))
                self.log.info("当前课程学习进度："+str(videoPercentage))
                self.log.info("进入播放页面开始学习...")
                self.driver.wait_to_be_visible(self.css.course_study()).click()
                sleep(2)
                
                self.driver.switch_to_last_window()
                self.driver.wait_to_be_visible(self.css.study_confirm()).click()
                
                while True:
                    try:
                        self.driver.wait_to_be_visible(self.xpath.study_videoduration(),retryTime=1).text
                    except StaleElementReferenceException as sere:
                        self.log.error("加载不了，这是一个坏课。我要删掉哦")
                        self.driver.close()
                        self.driver.switch_to_last_window()
                        self.driver.refresh()
                        self.driver.wait_to_be_visible(self.css.study_title())
                        self.driver.find_element(self.css.course_cancel()).click()
                        self.driver.wait_to_be_visible(self.css.course_cancelConfirm()).click()
                        sleep(2)
                        self.driver.refresh()
                        break
                    
                    retrytime_getstudytime=0
                    while True:
                        if retrytime_getstudytime == 120:
                            self.driver.refresh()
                            self.driver.wait_to_be_visible(self.css.study_confirm()).click()
                            retrytime_getstudytime=0
                        studytime=self.getVideoPlayTime()    
                        if studytime[8] == '0' and studytime[9] == '0':
                            retrytime_getstudytime+=1
                            sleep(1)
                        else:
                            break
                        
                    self.log.info("当前时间/总时间："+str(studytime))
                    
                    remainingMin=self.getVideoRemainingMin(studytime)
                    preremainingMin=remainingMin
                    retrycount = 0
                    self.log.info("剩余分钟： "+str(remainingMin))
                    
                    while True:
                        studytime=self.getVideoPlayTime()
                        remainingMin=self.getVideoRemainingMin(studytime)
                        if remainingMin == 0:
                            self.log.info("延时一分钟，等待课程结束退出...")
                            sleep(60)
                            self.remainNum -=1
                            self.log.info("开始学习下一课...")
                            break
                        else:
                            self.log.info("当前课程剩余时间："+str(remainingMin)+" 分钟")
                            if preremainingMin != remainingMin:
                                preremainingMin = remainingMin
                                retrycount = 0
                            else:
                                if retrycount == 6:
                                    self.log.error("视频加载超时，准备刷新...")
                                    break
                                else:
                                    retrycount +=1
                            
                            sleep(60)

                    self.driver.close()
                    self.driver.switch_to_last_window()
                    self.driver.refresh()
                    
                    break
    def getVideoPlayTime(self,timeout=120):
        retryCount=0
        while retryCount<=timeout:
            ex='\d{2}:\d{2} / \d{2}:\d{2}'
            text=self.driver.get_page_source()
            result=re.findall(ex,text,re.S)
            '''21:08 / 45:48'''
            if len(result) != 1 :
                sleep(0.5)
                retryCount+=1
                continue
            if len(result[0]) != 13:
                sleep(0.5)
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
while True:
    try:
        log=Log('main','i')
        las=Las()
        las.login().study_course(las.config.study_order())
        if las.remainNum == 0:
            break
    except Exception as e:
        log.error(traceback.format_exc())
        log.error('发生错误， '+str(las.config.restart_seconds())+' 秒等待后重启')
        sleep(las.config.restart_seconds())
        
    
    

