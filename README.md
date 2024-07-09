**Lngbzx_AutoStudy**

**———————————————————————————————————————————**

**功能：一键自动学习辽宁公需科目（专技区），自动播放下一课，输入一次账号密码后下次免输入。**

用法：

一.准备工作

  1.下载最新版的edge浏览器，一般电脑上面都自带edge无需安装。

  2.查看edge的版本号：通过浏览器右上角的三个小点--> 帮助与反馈 --> 关于 Microsoft Edge 中查看版本号

  3.从网上下载对应版本号的webdriver驱动。
  
      网址：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH
    
      旧版本edge的webdriver驱动下载网址：https://msedgewebdriverstorage.z22.web.core.windows.net/?form=MA13LH
    
      一般下载x64版本的或者压缩包后缀带win64的驱动就ok。

  4.将edgedriver解压，将里面的exe文件放在C:/Windows 文件夹中。
  
      当然也可以给存放edgedriver.exe的文件夹设置环境变量。

  5.由于我没写自动选课，所以在使用之前确保账号上已经选满50学时的课。
  
二.使用

  1.克隆本项目，按照requirements.txt安装selenium库和ddddocr库，使用ide运行main.py

  2.按照提示输入用户名和密码，刷课，启动！

三.FAQ

  1.有时候没刷完怎么自动退出了？
  
      公需科目的服务器很烂，有时候很长时间都加载不完网页，所以就自动退出了，重新打开程序即可。

  2.我刷完了怎么还不够学时？

      公需科目中有的视频是看不了的，看不了的课程序就会直接退课。选择其他课之后重新启动程序。

  3.进不去学习中心的页面怎么办？

      有可能账号密码输错的进不去，重启程序重新输入账号密码。

      正确的话，那是网站卡比了。

  2.有其他问题？

      请提issue捏。

    



