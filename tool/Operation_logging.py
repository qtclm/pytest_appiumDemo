import logging
import logging.handlers
import os
import threading
from datetime import datetime
import inspect, re

class logs(object):
    def __init__(self):
        self.logger = logging.getLogger()
        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        # 创建文件目录
        logs_dir = "../report/logging"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        # 修改log保存位置
        timestamp =str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S-out"))
        # timestamp='run'
        logfilename = '%s.log' %(timestamp)
        self.logfilepath = os.path.join(logs_dir, logfilename)

        if not self.logger.handlers:
            self.rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=self.logfilepath,
                                                                       maxBytes=1024 * 1024 * 50,
                                                                       backupCount=5,encoding='utf-8')
            # 设置输出格式
            formatter = logging.Formatter('''日志创建时间:%(asctime)s  - 进程id:%(process)d - 线程id:%(thread)d - 线程名称:%(threadName)s - 文件路径:%(pathname)s -
            代码行数:%(lineno)d - 运行函数名称:%(funcName)s - 日志等级:%(levelname)s - 日志内容:%(message)s''')
            self.rotatingFileHandler.setFormatter(formatter)
            # 控制台句柄
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(formatter)
            
            # 添加内容到日志句柄中
            # self.logger.addHandler(console)
            self.logger.addHandler(self.rotatingFileHandler)
            self.logger.setLevel(logging.INFO)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def out_varname(self,str_in):
        '''输入变量，返回变量名与值'''
        for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
            # out_varname:函数名称用于匹配
            m = re.search(r'\bout_varname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            key = m.group(1)  # 拿到变量名
            last_str = '{}:{}'.format(key, str_in)
            return last_str

    # #自动清理空日志文件
    def __del__(self):
        logging.shutdown()
        try:
            if os.stat(self.logfilepath).st_size == 0:
                os.remove(self.logfilepath)
        finally:
            return None


class MyLog(object):
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = logs()
            MyLog.mutex.release()

        return MyLog.log



if __name__ == '__main__':
    logger=MyLog.get_log()
    a=11
    # print(logger.out_varname(a))
    logger.get_logger().info("this is info")
    logs().get_logger().info("this is info")
    # logger.debug("this is debug")
    # logger.error("this is error")
    # logger.warning("this is warning")
