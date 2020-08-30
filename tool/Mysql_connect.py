import sys
sys.path.append('../')
from tool.Mysql_public import Mysql_operation
from tool.OperationDatas import OperationYaml
import pymysql

class Config(object):
    def __init__(self):
        config=OperationYaml(file_path='Config.yaml').read_data()
        self.dataBaseConfig=config['config']

class Mysql_tencentcloud(Mysql_operation,Config):
    def __init__(self):
        Config.__init__(self)
        tencent_cloud_mysql_conf=self.dataBaseConfig['tencent_cloud_mysql_conf']
        tencent_cloud_mysql_conf['db'] = 'test_datas'
        tencent_cloud_mysql_conf["cursorclass"]=pymysql.cursors.DictCursor
        super().__init__(**tencent_cloud_mysql_conf)

class Mysql_gld(Mysql_operation,Config):
    def __init__(self):
        Config.__init__(self)
        gld_mysql_conf=self.dataBaseConfig['gld_mysql_conf']
        gld_mysql_conf['db'] = 'calm_gld'
        gld_mysql_conf["cursorclass"]=pymysql.cursors.DictCursor
        super().__init__(**gld_mysql_conf)

class Mysql_gldexp(Mysql_operation,Config):
    def __init__(self):
        Config.__init__(self)
        gldexp_mysql_conf=self.dataBaseConfig['gldexp_mysql_conf']
        gldexp_mysql_conf['db'] = 'exp_calm_gld'
        gldexp_mysql_conf["cursorclass"]=pymysql.cursors.DictCursor
        super().__init__(**gldexp_mysql_conf)


if __name__=="__main__":
    # gldexp=Mysql_gldexp()
    # print(gldexp.sql_operation("""select *from partner_shop_biz where shop_identy='810109299' ;"""))
    gld=Mysql_gld()
    print(gld.sql_operation("""select *from partner_shop_biz where shop_identy='810109299' ;"""))
