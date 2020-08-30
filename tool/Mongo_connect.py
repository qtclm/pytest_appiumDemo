# -*- coding: utf-8 -*-
"""    
__author__ = qtclm
File Name：     Mongo_connect
date：          2020/4/17 13:12 
"""

import sys
sys.path.append('../')
from tool.Mongo_public import OperationMongo
from tool.OperationDatas import OperationYaml

class Config(object):
    def __init__(self):
        config=OperationYaml(file_path='Config.yaml').read_data()
        self.dataBaseConfig=config['config']

class Mongo_tencentcloud(OperationMongo,Config):
    def __init__(self):
        Config.__init__(self)
        host=self.dataBaseConfig['tencent_cloud_mongodb']['host']
        user=self.dataBaseConfig['tencent_cloud_mongodb']['user']
        password=self.dataBaseConfig['tencent_cloud_mongodb']['password']
        port=self.dataBaseConfig['tencent_cloud_mongodb']['port']
        db='creeper_test'
        super().__init__(host=host,user=user,password=password,port=port,db=db)
        # print('链接成功')

class Mongo_gld(OperationMongo,Config):
    def __init__(self):
        Config.__init__(self)
        host=self.dataBaseConfig['gld_mongodb']['host']
        user=self.dataBaseConfig['gld_mongodb']['user']
        password=self.dataBaseConfig['gld_mongodb']['password']
        port=self.dataBaseConfig['gld_mongodb']['port']
        db='calm_gateway_gld'
        super().__init__(host=host,user=user,password=password,port=port,db=db)
        # print('链接成功')

class Mongo_gldexp(OperationMongo,Config):
    def __init__(self):
        Config.__init__(self)
        host=self.dataBaseConfig['gldexp_mongodb']['host']
        user=self.dataBaseConfig['gldexp_mongodb']['user']
        password = self.dataBaseConfig['gldexp_mongodb']['password']
        port=self.dataBaseConfig['gldexp_mongodb']['port']
        db = 'calm_gateway_gld'
        super().__init__(host=host,user=user,password=password,port=port,db=db)
        # print('链接成功')

if __name__=='__main__':
    # gld=Mongo_gldexp()
    # print(gld.select_all_collection('dwd_gw_order_geo_dtl_i_d_1',{"commercial_id":810016429},{"trade_id":1,'brandId':1}))
    gld_exp=Mongo_gld()
    print(gld_exp.select_all_collection('partnerShopInfo',{"source":-92},{"shopId":0,'brandId':0,"_id":0} ,sort_col=[()]) )
    # Mongo_tencentcloud()