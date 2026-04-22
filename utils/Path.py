class Path:
    def __init__(self):
        self.url = {"login":"https://zyjs.lngbzx.gov.cn/",
                    "mycourse":"study_center/my_course",
                    "lesson":"video_detail"
                    }
        self.path = {"login_username":'//*[@id="app"]/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/form[1]/div[1]/div/div/input',
                     "login_password":"#app > div.is_cont > div.index_bg > div > div.banner_info > div.login_info.fr > div > div.form > form:nth-child(1) > div.el-form-item.password.is-required.el-form-item--small > div > div > input",
                     "login_passcode":"#app > div.is_cont > div.index_bg > div > div.banner_info > div.login_info.fr > div > div.form > form:nth-child(1) > div.el-form-item.aucthCode.is-required.el-form-item--small > div > div > input",
                     "login_passcodeimg":"#app > div.is_cont > div.index_bg > div > div.banner_info > div.login_info.fr > div > div.form > form:nth-child(1) > div.el-form-item.aucthCode.is-required.el-form-item--small > div > img",
                     "login_submit":"#app > div.is_cont > div.index_bg > div > div.banner_info > div.login_info.fr > div > div.form > form:nth-child(1) > div:nth-child(4) > div > button",
                     "ad_1":"#app > div.custom_service",
                     "ad_2":".right_service1",
                     "ad_3":".right_service2",
                     "ad_4":".right_service3",
                     "ad_5":".right_service4",#app > div:nth-child(5) > div
                     "ad_6":".right_service5",
                     "login_donehours":"#app > div.is_cont > div.index_bg > div > div.banner_info > div.login_info.fr > div > div.user_study_data > div.study_data_info.common_flex > div:nth-child(2) > span",
                     "login_studycourse":"#app > div.is_cont > div.index_bg > div > div.banner_info > div.login_info.fr > div > div.category > div:nth-child(1)",
                     "study_mycourse":"#app > div.is_cont > div.wrapper > ul > li:nth-child(2) > div.nav_bar_title",
                     "study_allcoursehours":"#app > div.is_cont > div:nth-child(3) > div.wrapper > div > div.content_right > div.optional > div.optional_left.clearfix > div:nth-child(2) > span",
                     "course_name":'//*[@id="app"]/div[2]/div[3]/div[1]/div/div[2]/div[3]/div/ul/li[1]/div[1]/div/div[2]/div[1]',
                     "course_studyhours":'//*[@id="app"]/div[2]/div[3]/div[1]/div/div[2]/div[3]/div/ul/li[1]/div[1]/div/div[2]/div[3]/span/span/span',
                     "course_progress":'//*[@id="app"]/div[2]/div[3]/div[1]/div/div[2]/div[3]/div/ul/li[1]/div[2]/div/div[2]',
                     "course_study":'//*[@id="app"]/div[2]/div[3]/div[1]/div/div[2]/div[3]/div/ul/li[1]/div[1]/div/div[2]/div[4]/div[2]/div/div[1]',
                     "lesson_confirm":'//*[@id="app"]/div[2]/div[5]/div/div[3]/span/button',
                     "lesson_controlbar":"#app > div.bodys.is_cont > div.video_center > div > div.video_box.wrapper > div.player > div",
                     "lesson_videoprogress":'//*[@id="app"]/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[8]'
                     }
    def get(self,key:str):
        return self.path[key]
    
    def get_url(self,key:str):
        return self.url[key]
    
