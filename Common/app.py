from appium import webdriver
# from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.webdriver import WebDriver
from Common.ServersManager import *

def caps_info(file_path='application_caps.yaml',caps='shishikeCaps'):
    yaml=get_data(file_path=file_path)
    caps=yaml[caps]
    return caps

cap_info=caps_info()
# commandInfo=get_data()#获取命令大全
# print(cap_info)
if caps_info()['appPackage']=='com.xueqiu.android':
    from xueqiuPages.login_page import LoginPage
else:
    from shishikePages.loginPage import LoginPage



class App:
    log=LoginPage(WebDriver).log

    @classmethod
    def start_appiumSever(cls,port_01=4723,port_02=4724):
        start_appiumServer(port_01=port_01,port_02=port_02)

    @classmethod
    def run_emulator(cls,emulatorName):
        start_emulator(emulatorName=emulatorName)

    # 重置app数据
    @classmethod
    def reset_appData(cls):
        app_package=cap_info['appPackage']
        command=commands['clear_package'].format(app_package)
        # cls.log.info("清除app数据")
        excuteCommand(command=command)

    @classmethod
    def restart_app(cls):
        appActivity = cap_info['appActivity']
        app_package= cap_info['appPackage']
        command=commands['restart_app'].format(app_package,appActivity)
        excuteCommand(command=command)


    driver:WebDriver=None
    @classmethod
    def startApp(cls,port=4723,implicitly_wait_time=20,emulatorName='android10'):
        # 获取设备列表：如果为空，启动模拟器，默认启动一个
        while True:
            devices = get_device_list()
            print(devices)
            cls.log.info("devices：{}".format(devices))
            if '127.0.0.1:5555' in devices:
                restart_adbServer()
                time.sleep(2)
            if len(devices)>=1:
                break
            else:
                excuteCommand(commands["start_leidian4"])
                # print("执行启动")
                # cls.run_emulator(emulatorName)
                cls.log.info("开始启动模拟设备")
                time.sleep(10)

        # 检测appium-server是否启动
        while True:
            appium_server_flag=appiumServercheck(port)
            cls.log.info("appium_server_flag:{}".format(appium_server_flag))
            if appium_server_flag:
                break
            else:
                cls.log.info("开始启动appium-service")
                start_appiumServer(port_01=port)
                time.sleep(5)
        # 检测app是否安装
        packages=get_packages();app_caps=cap_info
        if not app_caps['appPackage'] in packages :
            if  app_caps['appPackage']=='com.xueqiu.android':
                app_caps['app']='../app/com.xueqiu.android_12.13.4_270.apk'
                # cls.log.info("开始安装雪球app")
                print("开始安装雪球app")
            elif app_caps['appPackage']=='io.appium.android.apis':
                app_caps['app']='../app/ApiDemos-debug.apk'
                # cls.log.info("开始安装apiDemos")
                print("开始安装apiDemos")
            elif app_caps['appPackage'] == 'com.shishike.mobile':
                app_caps['app'] = '../app/OnMobile-official-6.3.1.apk'
                # cls.log.info("开始安装shishike")
                print("开始安装shishike")
            else:
                raise Exception("暂不支持的app包名，无法自动安装")
        cls.driver = webdriver.Remote("http://127.0.0.1:{}/wd/hub".format(port), app_caps)
        cls.driver.implicitly_wait(implicitly_wait_time)
        cls.log.info('启动app')
        return LoginPage(cls.driver)

    @classmethod
    def quit(cls):
        cls.log.info("关闭app")
        cls.driver.quit()



if __name__=="__main__":
    # get_packages()
    # App.reset_appData()
    # App.restart_app()
    App.startApp()
    # print(get_packages())
    # App.caps_info()
    # App.quit()