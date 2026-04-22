from utils.EasySelenium import Driver,Log
from utils.Path import Path
from utils.Ocr import ocr

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].driver.quit()
    return wrapper
class Lngbzx_Autostudy:
    def __init__(self,username:str,password:str):
        self.username = username
        self.password = password
        self.driver = Driver(mute=True)
        self.log=Log("Lngbzx_Autostudy", "i").logger
        self.path = Path()
        
    def login(self):
        
        self.driver.wait(self.path.get("ad_1")).remove()
        self.driver.wait(self.path.get("ad_2")).remove()
        self.driver.wait(self.path.get("ad_3")).remove()
        self.driver.wait(self.path.get("ad_4")).remove()
        self.driver.wait(self.path.get("ad_5")).remove()
        self.driver.wait(self.path.get("ad_6")).remove()
        
        self.driver.wait(self.path.get("login_username"),timeout=60).send_keys(self.username)
        self.log.info(str(self.username)+" 用户正在登录...")
        self.driver.wait(self.path.get("login_password")).send_keys(self.password)
        img_path=self.driver.wait(self.path.get("login_passcodeimg")).screenshot("passcode")
        result=ocr(img_path)
        self.driver.wait(self.path.get("login_passcode")).send_keys(result)
        self.driver.wait(self.path.get("login_submit")).click()
    
    @handle_exception
    def start(self):
        self.driver.get(self.path.get_url("login"))
        
        self.login()
        
        current_hours = float(self.driver.wait(self.path.get("login_donehours"),timeout=120).get_text())
        target_hours = 50.00
        self.log.info("已完成学时: " + str(current_hours) + " 目标学时: " + str(target_hours))
        
        
        self.driver.wait(self.path.get("login_studycourse")).click()
        self.driver.wait(self.path.get("study_mycourse")).click()
        while True:
            if float(current_hours) >= target_hours:
                self.log.info("已达到目标学时，正在退出...")
                self.driver.quit()
                return
        
            title=self.driver.wait(self.path.get("course_name")).get_text()
            progress=self.driver.wait(self.path.get("course_progress")).get_text()
            studyhours=self.driver.wait(self.path.get("course_studyhours")).get_text()
            if "100" in progress:
                self.log.info("全部课程已学习完成，正在退出...")
                self.driver.quit()
                return 
            
            
            self.driver.wait(self.path.get("course_study")).click()
            self.driver.switch_to_window(self.path.get_url("lesson"))
            self.driver.wait(self.path.get("lesson_confirm")).click()
            self.driver.reset_window_size()
            loading_first_flag=True
            play_first_flag=True
            while True:
                "00:12 / 23:59"
                video_progress=self.driver.wait(self.path.get("lesson_videoprogress")).get_text()
                current_min=video_progress[0:2]
                current_sec=video_progress[3:5]
                total_min=video_progress[8:10]
                total_sec=video_progress[11:13]
                self.log.debug("当前current_min: "+current_min+" current_sec: "+current_sec+" total_min: "+total_min+" total_sec: "+total_sec)
                if video_progress == "00:00 / 00:00":
                    if loading_first_flag:
                        self.log.info("课程加载中...")
                        loading_first_flag = False
                
                elif len(current_min) == 2 and current_min == total_min and current_sec == total_sec:
                    
                    self.log.info("当前课程学习完成，正在退出...")
                    current_hours = current_hours+float(studyhours)
                    self.driver.close()
                    self.driver.switch_to_window(self.path.get_url("mycourse"))
                    self.driver.refresh()
                    break
                else:
                    if play_first_flag:
                        self.log.info("正在学习：" + title +" 学时：" + studyhours + " 目前视频进度: " + video_progress)
                        play_first_flag = False
                
                self.driver.sleep(10)
            
        
if __name__ == "__main__":
    # 请替换成你的登录信息
    Lngbzx_Autostudy("username","password").start()