import os
import json

from utils.log import Log
from utils.encrypt import usnmdcfiiro1cqqt,pwdcfiiro1c


class Config:
    def __init__(self) -> None:
        self.log=Log('config','d')
        
        if not os.path.exists('./config/config.json'):
            self.config={
            'STUDY_ORDER':1,   
            "RESTART_SECONDS":60,
            'userName':"",
            'passWord':"", 
            }
        
        else:
            with open ('./config/config.json','r') as f:
                self.config=json.load(f)
                f.close()
        
        if self.username() is None:
            self.get_username_and_password()
                
    def get_username_and_password(self):
        username=input("请输入用户名（按回车键确认）：")
        password=input("请输入密码（按回车键确认）：")
        
        self.add_encrypted_val('userName',username)
        self.add_encrypted_val('passWord',password)
          
        
    def study_order(self):
        return self.config['STUDY_ORDER']
    
    def restart_seconds(self):
        return self.config['RESTART_SECONDS']
    
    def username(self):
        if self.config['userName'] == "":
            return None
        else:
            return self.get_encryed_val(self.config['userName'])
    
    def password(self):
        if self.config['passWord'] == "":
            return None
        else:
            return self.get_encryed_val(self.config['passWord'])
                
    def save_to_config_file(self):
        with open("./config/config.json","w") as f:
            f.write(json.dumps(self.config))
            f.close()
            
    def get(self,key):
        return self.config[key]
    
    def add_encrypted_val(self,key,value):
        self.config[key]= usnmdcfiiro1cqqt(value)
        
    def get_encryed_val(self,str):
        return pwdcfiiro1c(str)
                    