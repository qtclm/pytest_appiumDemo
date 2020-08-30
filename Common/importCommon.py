from logging import Logger
from tool.Operation_logging import MyLog
from tool.Send_email import SendEmail
from tool.OperationDatas import OperationYaml
from tool.Mongo_connect import Mongo_gld,Mongo_gldexp
from tool.Mysql_connect import Mysql_gld,Mysql_gldexp

class log(object):
    def __init__(self):
        self.mylog = MyLog.get_log()  # 日志
        self.log = self.mylog.get_logger()  # 获取日志创建对象

# '''基础方法'''
class Tool(log):
    def __init__(self,path,file_path):
        super().__init__()
        self.send_mail=SendEmail()#邮件发送
        self.gld_mongo=Mongo_gld()
        self.gldexp_mongo=Mongo_gldexp()
        self.gld_mysql=Mysql_gld()
        self.gldexp_mysql=Mysql_gldexp()
        # 默认读取config，此文件只读不写
        self.yaml=OperationYaml(path=path,file_path=file_path)


