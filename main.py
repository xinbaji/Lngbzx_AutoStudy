from selenium import webdriver
import time
import os
import re
import json
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException,StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import ddddocr
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
        
        self.options=webdriver.EdgeOptions()
        self.options.add_experimental_option('detach',True)
        '''prefs={
            'profile.default_content_setting_values': {
            'images': 2,  #屏蔽图片
            }
        }
        self.options.add_experimental_option("prefs",prefs)'''
        #self.driver=webdriver.Edge(options=self.options)
        self.driver=webdriver.Edge()
        self.ocr=ddddocr.DdddOcr()

    def ocrToCode(self):
        image = open("needocr.png", "rb").read()
        result = self.ocr.classification(image)
        self.debug("result:"+str(result))
        if len(result) != 4:
            self.info("未识别到结果，重新检测")
            return -1
        try:
            for i in range(0,4,1):
                j=int(i)
        except ValueError as ve:
            self.info("未识别到结果，重新检测")
            return -1
        else:
            self.info("识别结果："+str(result))

        code=str(result)
        self.info("当前验证码为："+code)
        return code
    def refreshPage(self,starttime):
        while(self.status != 1 ):
            st=starttime
            time.sleep(5)
            currentTime=int(time.time())
            if self.status == 1:
                self.status = 0
                return 0
            elif currentTime-st >= 40:
                st=currentTime
                self.driver.refresh()
            
    

    def appear_wait(self,type,val):
        self.status = 0
        starttime=int(time.time())
        if type == 'xpath':
            by=By.XPATH
        elif type == 'css':
            by=By.CSS_SELECTOR
        th=Thread(target=self.refreshPage,args=(starttime,))
        ww=WebDriverWait(self.driver,180).until(EC.presence_of_element_located((by,val)))
        
        while True:
            try:
                target=self.driver.find_element(by,val)
                self.status = 1
            except Exception as e:
                self.error("appear_wait"+str(e)+type+val)
            else:
                break
        
    def appearword_execute(self,cssselector,word,func):
        try:
            while True:
                target=self.driver.find_element(By.CSS_SELECTOR,cssselector)
                if word in target.text:
                    break
            
            func()
        except Exception as e:
            self.error("appear_wait"+str(e)+cssselector+word)
    
    def appearword_click(self,type,val,word,timeout=180):
        '''
        function:等待元素出现文字时点击文字。
        type:'xpath' --> By.XPATH
             'css'   --> By.CSS_SELECTOR
        '''
        if type == 'xpath':
            by=By.XPATH
        elif type == 'css':
            by=By.CSS_SELECTOR
        ww=WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located((by,val)))
        try:
            while True:
                target=self.driver.find_element(by,val)
                self.debug(target.text)
                if word in target.text:
                    break
            
            target.click()
        
        except NoSuchElementException as nee:
            time.sleep(0.5)
        except Exception as e:
            self.error(e)

class LAS(ToolKit):

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
            "textcode_url":"https://zyjstest.lngbzx.gov.cn/trainee/login/verifyCode?code=",
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

        def washpage():
            time.sleep(0.5)
            self.driver.execute_script("document.querySelector('.el-message-box__wrapper').remove()")
            self.driver.execute_script("document.querySelector('.v-modal').remove()")
            self.driver.execute_script("document.querySelector('.right_service1').remove()")
            self.driver.execute_script("document.querySelector('.right_service2').remove()")
            self.driver.execute_script("document.querySelector('.right_service3').remove()")
            self.driver.execute_script("document.querySelector('.right_service4').remove()")
            self.driver.execute_script("document.querySelector('.right_service5').remove()")
            time.sleep(0.5)

        
        self.driver.set_page_load_timeout(10)
        try:
            self.driver.get(self.url['index'])
        except TimeoutException as te:
            pass
        #self.appearword_execute(self.css['index_infoWord'],'通知',washpage)
        self.appearword_click('css',self.css['index_infoButtonWord'],'确定')
        self.driver.execute_script("document.querySelector('.right_service1').remove()")
        self.driver.execute_script("document.querySelector('.right_service2').remove()")
        self.driver.execute_script("document.querySelector('.right_service3').remove()")
        self.driver.execute_script("document.querySelector('.right_service4').remove()")
        self.driver.execute_script("document.querySelector('.right_service5').remove()")
        self.driver.find_element(By.XPATH,self.xpath['username_input']).send_keys(self.config['userName'])
        self.driver.find_element(By.XPATH,self.xpath['password_input']).send_keys(self.config['passWord'])
        self.debug("输入用户名和密码")

        while True:
            self.debug("识别验证码")
            #截图获取验证码
            self.driver.find_element(By.XPATH,self.xpath['textcode_img']).screenshot('needocr.png')
            #requests请求验证码
            '''textcodeurl=self.driver.find_element(By.XPATH,self.xpath['textcode_img']).get_attribute('src').replace("blob:","")
            self.debug(textcodeurl)
            imgdata=requests.get(textcodeurl).content
            with open("needocr.png","wb") as f:
                f.write(imgdata)
                f.close()'''
            textcode=self.ocrToCode()
            if textcode == -1:
                self.driver.find_element(By.XPATH,self.xpath['textcode_img']).click()
                time.sleep(2)
            else:
                break
        self.debug("输入验证码")
        self.driver.find_element(By.XPATH,self.xpath['textcode_input']).send_keys(textcode)
        self.driver.find_element(By.XPATH,self.xpath['login_button']).click()
        time.sleep(1)

        self.appearword_click('css',self.css['index_studyCenter'],'学习中心')
        if os.path.exists("config.json") == False:
            with open("config.json","w") as f:
                    f.write(self.json_str)
                    f.close()
        return self

    def tasklist_create(self):
        #获取当前剩余任务，获取进度和剩余时间，并添加到任务队列中。
        
        self.appearword_click('xpath',self.xpath['course_mycourse'],'我的课程')
        self.info("正在获取当前进度，请稍后...")
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,self.css['course_remainCourseNum'])))
        self.remainNum=eval(self.driver.find_element(By.CSS_SELECTOR,self.css['course_remainCourseNum']).text)
        
        if  self.remainNum == 0:
            self.error("请先选课或本次学习已完成...")
        else:
            self.info("当前有 "+str(self.remainNum)+" 节未完成学习")
        
        return self
    
    def checkstudycourseprestatus(self):
        self.appearword_execute(self.css['course_checkcomplete'],'课程',self.studyCourse)

    def studyCourse(self):
        while True:
            if self.remainNum == 0:
                self.info("全部学习已完成...")
                break
            else:
            #获取当前进度
                self.appear_wait('css',self.css['study_title'])
                title=self.driver.find_element(By.CSS_SELECTOR,self.css['study_title']).text
                videoPercentage=self.driver.find_element(By.CSS_SELECTOR,self.css['study_percentage']).text
                self.info("正在学习："+str(title))
                self.info("当前课程学习进度："+str(videoPercentage))
                self.info("进入播放页面开始学习...")
                self.driver.find_element(By.CSS_SELECTOR,self.css['course_study']).click()
                time.sleep(5)
                self.debug(self.driver.window_handles[0])
                self.debug("********************************")
                self.debug(self.driver.window_handles[-1])
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.implicitly_wait(10)
                time.sleep(5)
                self.appear_wait('xpath',self.xpath['study_confirmbutton'])
                self.driver.find_element(By.XPATH,self.xpath['study_confirmbutton']).click()
                #self.driver.find_element(By.CSS_SELECTOR,self.css['study_confirm']).click()
                
                while True:
                    try:
                        self.appear_wait('xpath',self.xpath['study_videoduration'])
                        studytime=self.driver.find_element(By.XPATH,self.xpath['study_videoduration']).text
                    except StaleElementReferenceException as sere:
                        self.error("加载不了，这是一个坏课。我要删掉哦")
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.driver.refresh()

                        self.appear_wait('css',self.css['study_title'])
                        self.driver.find_element(By.CSS_SELECTOR,self.css['course_cancel']).click()
                        self.appear_wait('css',self.css['course_cancelConfirm'])
                        self.driver.find_element(By.CSS_SELECTOR,self.css['course_cancelConfirm']).click()
                        time.sleep(2)
                        self.driver.refresh()
                        break
                        
                        

                    if studytime[0] == '0':
                        studytime=studytime[1:len(studytime)]
                    if studytime[2] == '0':
                        studytime=studytime[0:2]+studytime[3:len(studytime)]
                    if studytime[6] == '0':
                        studytime=studytime[0:6]+studytime[7:len(studytime)]
                    self.debug("当前时间，总时间:"+studytime)
                    '''21:08 / 45:48'''
                    '''0:8 / 33:50'''
                    ex='(.*?):(.*?) / (.*?):'
                    result=re.findall(ex,studytime,re.S)[0]
                    studyCurrentTimeMin,videoDurationMin=eval(result[0]),eval(result[2])
                    remainingMin=videoDurationMin-studyCurrentTimeMin
                    self.debug("剩余分钟： "+str(studytime))
                    '''if remainingMin == 0:
                        self.info("延时一分钟，准备退出...")
                        time.sleep(60)
                        self.info("本课学习完成，准备切换至下一课...")
                        self.remainNum -=1
                        '''
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
while True:
    try:
        las.login().tasklist_create().studyCourse()
    except TimeoutError as te:
        las.error("超时，等待30喵重新执行程序...")
        time.sleep(30)