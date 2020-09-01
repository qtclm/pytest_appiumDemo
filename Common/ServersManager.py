import os
import re
import subprocess
import tempfile
import time
from sys import platform
from tool.OperationDatas import OperationYaml


def get_data(file_path='Commands.yaml'):
    yaml=OperationYaml(file_path=file_path)
    commands=yaml.read_data()
    return commands

commands=get_data()
#获取系统的名称，使用对应的指令
# 1.获取系统类型和命令类型
def getsystemType():
    system=platform
    if system in commands['windows_platform']:
        local_system=system
    else:
        local_system=commands['linux']
    return  local_system

# 重启adb-server
def restart_adbServer():
    excuteCommand(commands['adb_kill'])
    time.sleep(1)
    excuteCommand(commands['adb_start'])

# 2.获取已连接的设备列表：# 获取设备列表
def get_device_list():
    devices = []
    # os.system()、os.popen()和subprocess的区别（一）:https://www.cnblogs.com/yu97271486/p/12497622.html
    result = excuteCommand(commands['get_deivces'])
    result.reverse()
    # print(result)
    for line in result[1:]:
        if "attached" not in line.strip():
            if "offline" in line.strip():
                time.sleep(5)
                devices.append(line.split()[0])
            elif '127.0.0.1:5555' in devices:
                pass
            else:
                devices.append(line.split()[0])

        else:
            break
    return devices

# 3.获取模拟器列表
def get_emulator_list():
    command="emulator -list-avds"
    result=excuteCommand(command,commandType='popen')
    return result

 # 4.根据系统和端口来启动appium server
def start_appiumServer(port_01=4723, port_02=4724):
    systemstr = getsystemType()
    if systemstr in commands['windows_platform']:
        # os.system默认阻塞当前程序执行，在cmd命令前加入start可不阻塞当前程序执行
        command=commands['windows_start_appiumServer'].format(port_01,port_02)
        excuteCommand(command,commandType='system',join_start=True)

    else:
        command=commands['linux_start_appiumServer'].format(port_01,port_02)
        excuteCommand(command,commandType='system',join_start=True)
    time.sleep(2)
    print("appium-server started")

# 5.启动模拟器
def start_emulator(emulatorName):
    command=commands['start_emulator'].format(emulatorName)
    excuteCommand(command,join_start=True)

# 检测appiumServer是否启动
def appiumServercheck(port=4723):
    systemstr = getsystemType()
    if systemstr in commands['windows_platform']:
        cmd_find =commands['windows_find_port'].format(port)
        # print(cmd_find)
        text = excuteCommand(cmd_find)
        text = [i for i in text if ':{} '.format(port) in i]  # 过滤端口中包含4723的信息，以免造成程序误判
        if text:
            pid = re.search('\d+$',text[0].strip())
            if pid :
                pid=pid.group()
                # 执行被占用端口的pid
                # print(pid)
                if int(pid)>0:
                    return pid
                return False
            return False
        return False
    else:
        cmd_find = commands['linux_find_port'].format(port)
        # print(cmd_find)
        text = excuteCommand(cmd_find)
        text = [i for i in text if ':{} '.format(port) in i]  # 过滤端口中包含4723的信息，以免造成程序误判
        if text != "":
            pid = re.search('\d+$',text[0].strip())
            if pid:
                pid=pid.group()
                # 执行被占用端口的pid
                if int(pid) > 0:
                    return pid
                return False
            return False
        return False



# 6.根据系统和端口号关闭appium server
def kill_appiumServer(port=4723):
    # 查找对应端口的pid
    time.sleep(5)
    systemstr = getsystemType()
    if systemstr in commands['windows_platform']:
        pid=appiumServercheck(port)
        if pid:
            cmd_kill =commands['windows_kill_port'] .format(pid)
            # print(cmd_kill)
            excuteCommand(cmd_kill)
            print("apppium-server killed")
        else:
            print("The appium-server port is not occupied and is available")

    else:
        pid = appiumServercheck(port)
        if pid:
            cmd_kill = commands['linux_kill_port'] .format(pid)
            excuteCommand(cmd_kill)
            print("apppium-server killed")
        else:
            print("The appium-server port is not occupied and is available")

# 获取所有packages
def get_packages():
    command=get_data()['get_packges']
    packages=excuteCommand(command=command,commandType='popen')
    return [i.strip()[len("package:"):] for i in packages]


# 命令执行封装
def excuteCommand(command,commandType='subPopen',join_start=False):
    # join_start:将start字符串拼接在命令前，防止程序运行阻塞，默认为阻塞
    # commandType：指定命令类型
    if join_start==True:
        command='start {}'.format(command)
    try:
        if commandType=='system':
            result=os.system(command)
        elif commandType=='popen':
            result = os.popen(command)
        elif commandType=='popen2':
            result = os.popen2(command)
        elif commandType=='popen3':
            result = os.popen3(command)
        elif commandType=='popen4':
            result = os.popen4(command)
        #Python中使用subprocess执行一系列cmd命令时，偶尔会出现阻塞情况，命令没有继续执行完毕。
        # 原因：
        #     #subprocess的PIPE是有大小的。在python2.6.11之前，PIPE的大小为文件页的大小（i386上是4096），# 2.6.11之后变为65536.因此当输出内容超过65536，会引起阻塞
        # 解决：
        #     1.使用临时文件tempfile扩展缓存区；2.去掉不必要输出，以减少输出量的大小
        elif commandType=='subPopen':
            out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000)
            fileno = out_temp.fileno()
            if join_start==True:
                subprocess.Popen(command, shell=True, stdout=fileno,
                                          stderr=subprocess.PIPE)  # stdout=subprocess.PIPE
                result = None
            else:
                result=subprocess.Popen(command,shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE).stdout.readlines()#stdout=subprocess.PIPE

            # 在decode方法中加入ignore忽略解码错误
            if result and isinstance(result,list):
                result=[i.decode("utf8","ignore").strip() for i in result]
        else:
            print("暂不支持的命令执行方式")
            return None
        return result
    except Exception as e:
        print(e)
        return None

if __name__=="__main__":
    # pass
    # get_command()
    # print(getsystemType())
    # print(get_device_list())
    print(appiumServercheck())
    # start_appiumServer()
    # kill_appiumServer()
    # device_list=get_emulator_list()
    # for i in list(device_list)[1:]:
    #     start_emulator(i)
    # pa=get_packages()
    # print(pa)
    # for i in pa:
    #     print(i)