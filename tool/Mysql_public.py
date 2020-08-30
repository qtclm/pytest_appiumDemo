import pymysql
from threading import RLock,Lock
import sys
sys.path.append("../")
from tool.Operation_logging import MyLog
#Lock用于增加互斥锁，防止多线程执行sql报错
# lock和rlock（递归锁）的区别:
    # 这两种琐的主要区别是：RLock允许在同一线程中被多次acquire。而Lock却不允许这种情况。注意：如果使用RLock，那么acquire和release必须成对出现，
    # 即调用了n次acquire，必须调用n次的release才能真正释放所占用的琐。
# threading.Condition
    # 可以把Condiftion理解为一把高级的琐，它提供了比Lock, RLock更高级的功能，允许我们能够控制复杂的线程同步问题。threadiong.Condition在内部维护一个琐对象（默认是RLock），
# 可以在创建Condigtion对象的时候把琐对象作为参数传入。Condition也提供了acquire, release方法，其含义与琐的acquire, release方法一致，其实它只是简单的调用内部琐对象的对应的方法而已。
# Condition还提供了如下方法(特别要注意：这些方法只有在占用琐(acquire)之后才能调用，否则将会报RuntimeError异常。)：
    # Condition.wait([timeout]):
    # 　　wait方法释放内部所占用的琐，同时线程被挂起，直至接收到通知被唤醒或超时（如果提供了timeout参数的话）。当线程被唤醒并重新占有琐的时候，程序才会继续执行下去。
    # Condition.notify():#唤醒一个挂起的线程（如果存在挂起的线程）。注意：notify()方法不会释放所占用的琐。
    # Condition.notifyAll()　唤醒所有挂起的线程（如果存在挂起的线程）。注意：这些方法不会释放所占用的琐



class Mysql_operation(object):
    def __init__(self,*args, **kwargs):
        self.mylog=MyLog.get_log()
        self.log = self.mylog.get_logger()
        try:
            self.Mysql_operation=pymysql.connect(*args,**kwargs) #crm数据库配置
            self.cursor = self.Mysql_operation.cursor() #创建操作游标
            self.lock = RLock()#使用递归锁，防止同一线程内多次acquire造成死锁
        except Exception as error:
            self.log.error(self.mylog.out_varname(error))
            print("数据库连接失败，原因为%s"%(error))
            
    def sql_operation(self,sql_operation):
        '''整合数据库sql操作'''
        self.log.info(self.mylog.out_varname(sql_operation))
        if sql_operation:
            self.sql=sql_operation
            path='M'
            #这里得实例必须写为self.sql，写为其他得变量会导致调用错误
            try:
                self.lock.acquire()#加互斥锁
                # print('以上锁')
                self.cursor.execute(sql_operation) #执行sql
                # print('sql已执行')
                self.Mysql_operation.commit()#执行提交操作
                # print('sql已执行提交')
                self.lock.release()#解锁
                # print('已解锁')
                result=self.cursor.fetchall()#获取全部查询结果
                self.log.info(self.mylog.out_varname(result))
                return result
            except Exception as error:
                try:
                    self.Mysql_operation.rollback()#遇到异常执行数据回滚
                    temp='执行数据回滚'
                    self.log.info(self.mylog.out_varname(temp))
                except AttributeError as error:
                    self.log.error(self.mylog.out_varname(error))
                # print("sql执行失败，原因为%s"%(error))
        else:
            print('sql都没有,查询个鬼哦')
            return False
            
    def sql_operation_limit(self,sql_operation,limit=0,count=1):
        # '''limit:从第多条开始取数据，num结束位置确定最终返回的记录'''
        # '''默认只取执行结果的第一条记录,也可自定义'''
        result=self.sql_operation(sql_operation)
        if result:
            # count的值不能小于limit所以这里加
            if isinstance(limit,int) and isinstance(count,int):
                if count<=0:
                    count=1
                count+=limit
                if result:
                    if count==1:
                        return result[0]
                    elif len(result)>=count:
                        return result[limit:count]
                    elif len(result)<limit or len(result)<count:
                        return result
                else:
                    return result
            else:
                print("不要整些骚操作,数据都给你")
                return result
        else:
            return False

    def close_db(self):
        try:
            self.Mysql_operation.close() #关闭数据库连接
        except Exception as error:
            self.log.error(self.mylog.out_varname(error))
            # print("关闭数据库连接失败，原因为%s"%(error))

    def sql_batch(self,sql_select,data_list):
        if sql_select and data_list:
            '''数据批量操作'''
            try:
                self.lock.acquire()
                result=self.cursor.executemany(sql_select,(data_list)) #批量执行sql
                self.Mysql_operation.commit()# 执行提交操作
                self.lock.release()
                self.log.info(self.mylog.out_varname(result))
                return result
            except Exception as error:
                try:
                    self.Mysql_operation.rollback()#遇到异常执行数据回滚
                    temp='执行数据回滚'
                    self.log.info(self.mylog.out_varname(temp))
                except AttributeError as error:
                    self.log.error(self.mylog.out_varname(error))
        else:
            print('sql或list无效,请检查后在执行')
            return False



if __name__=="__main__":
    tencent_cloud_host='122.51.175.10'
    tencent_cloud_mysql_conf={"host": tencent_cloud_host, "port": 3306, "user": "root",
                               "passwd": "Test@20191113", "db": "",
                               "charset": "utf8", "use_unicode": True,
                               "cursorclass": pymysql.cursors.DictCursor}
    sql='''select *from nc_course'''
    tencent_cloud_mysql_conf['db']='test_datas'
    my=Mysql_operation(**tencent_cloud_mysql_conf)
    data=my.sql_operation_limit(sql)
    print(data)