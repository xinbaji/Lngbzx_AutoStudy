from selenium.webdriver.common.by import By

class Url:
    def __init__(self) -> None:
        self.url={"index":"https://zyjstest.lngbzx.gov.cn/"}
        
    def index(self):
        return self.url['index']

    
class Xpath:
    
    def __init__(self) -> None:
        self.XPATH = {
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
        "course_mycourse":'//*[@id="app"]/div[2]/div[2]/ul/li[2]/div[1]',
        "study_percentage":'//*[@id="app"]/div[2]/div[3]/div[1]/div/div[2]/div[3]/div/ul/li[1]/div[2]/div/div[2]'
        
    }
    def study_percentage(self):
        return (By.XPATH,self.XPATH['study_percentage'])
        
    def index_info(self):
        return (By.XPATH,self.XPATH['index_info'])
    
    def index_black(self):
        return (By.XPATH,self.XPATH["index_black"])
    
    def index_infoConfirm(self):
        return (By.XPATH,self.XPATH['index_infoConfirm'])
    
    def username_input(self):
        return (By.XPATH,self.XPATH['username_input'])
    
    def password_input(self):
        return (By.XPATH,self.XPATH['password_input'])
    
    def textcode_input(self):
        return (By.XPATH,self.XPATH['textcode_input'])
    
    def login_button(self):
        return (By.XPATH,self.XPATH['login_button'])
    
    def textcode_img(self):
        return (By.XPATH,self.XPATH['textcode_img'])
    
    def study_videoduration(self):
        return (By.XPATH,self.XPATH['study_videoduration'])
    
    def study_confirmbutton(self):
        return (By.XPATH,self.XPATH['study_confirmbutton'])
    
    def course_mycourse(self):
        return (By.XPATH,self.XPATH['course_mycourse'])
    
class Css:
    def __init__(self) -> None:
        self.CSS={
        "index_info":'body > div.el-message-box__wrapper',
        "index_black":'body > div.v-modal',
        "index_right1":'.right_service1',
        "index_right2":'.right_service2',
        "index_right3":'.right_service3',
        "index_right4":'.right_service4',
        "index_right5":'.right_service5',
        
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
    def index_info(self):
        
        return (By.CSS_SELECTOR,self.CSS['textcode_new'])
    def index_black(self):
        return (By.CSS_SELECTOR,self.CSS['index_black']   )
    def index_right1(self):
        return (By.CSS_SELECTOR,self.CSS['index_right1']   )
    def index_right2(self):
        return (By.CSS_SELECTOR,self.CSS['index_right2']   )
    def index_right3(self):
        return (By.CSS_SELECTOR,self.CSS['index_right3']  ) 
    def index_right4(self):
        return (By.CSS_SELECTOR,self.CSS['index_right4'])
    def index_right5(self):
        return (By.CSS_SELECTOR,self.CSS['index_right5'])
             
    def textcode_new(self):
        return (By.CSS_SELECTOR,self.CSS['textcode_new'])
        
    def index_infoButtonWord(self):
        return (By.CSS_SELECTOR,self.CSS['index_infoButtonWord'])
        
    def index_infoWord(self):
        return (By.CSS_SELECTOR,self.CSS['index_infoWord'])
        
    def index_studyCenter(self):
        return (By.CSS_SELECTOR,self.CSS['index_studyCenter'])
        
    def course_mycourse(self):
        return (By.CSS_SELECTOR,self.CSS['course_mycourse'])
        
    def course_incompleteCourse(self):
        return (By.CSS_SELECTOR,self.CSS['course_incompleteCourse'])
        
    def course_remainCourseNum(self):
        return (By.CSS_SELECTOR,self.CSS['course_remainCourseNum'])
        
    def course_remainCoursePageInput(self):
        return (By.CSS_SELECTOR,self.CSS['course_remainCoursePageInput'])
        
    def course_study(self):
        return (By.CSS_SELECTOR,self.CSS['course_study'])
        
    def course_cancel(self):
        return (By.CSS_SELECTOR,self.CSS['course_cancel'])
        
    def course_cancelConfirm(self):
        return (By.CSS_SELECTOR,self.CSS['course_cancelConfirm'])
        
    def course_checkcomplete(self):
        return (By.CSS_SELECTOR,self.CSS['course_checkcomplete'])
        
    def study_confirmWord(self):
        return (By.CSS_SELECTOR,self.CSS['study_confirmWord'])
        
    def study_confirm(self):
        return (By.CSS_SELECTOR,self.CSS['study_confirm'])
        
    def study_videoduration(self):
        return (By.CSS_SELECTOR,self.CSS['study_videoduration'])
        
    def study_percentage(self):
        return (By.CSS_SELECTOR,self.CSS['study_percentage'])
        
    def study_title(self):
        return (By.CSS_SELECTOR,self.CSS['study_title'])
    
    


