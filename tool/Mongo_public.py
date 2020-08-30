#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''@auther :mr.qin
@IDE:pycharm'''


import pymongo
import sys

class OperationMongo(object):
	def __init__(self,user=None,password=None,host=None,port=None,db=None):
		try:
			self.connect_client = pymongo.MongoClient(host=host, port=port)
			# 连接mydb数据库,账号密码认证
			self.mydb = self.connect_client[db]  # 先连接系统默认数据库admin
			# #下面一条更改是关键，我竟然尝试成功了，不知道为啥，先记录下踩的坑吧
			self.mydb.authenticate(user, password, mechanism='SCRAM-SHA-1')  # 让admin数据库去认证密码登录，好吧，既然成功了，
		except BaseException as e:
			raise BaseException("数据库连接失败，原因：{}".format(e))

	def insert_collection(self,collection_name,value):#单个插入
		if isinstance(collection_name,str) and isinstance(value,dict):
			mycol=self.mydb[collection_name]
			mycol_id=mycol.insert_one(value)
			return mycol_id.inserted_id #返回insert_id，即插入文档的id值
		else:
			return "{},{}:类型错误,类型必须为string与dict".format(collection_name,value)

	def insert_batch_collection(self,collection_name,value_list):#批量插入
		if isinstance(collection_name, str) and isinstance(value_list, list):
			mycol=self.mydb[collection_name]
			mycol_id=mycol.insert_many(value_list)
			return mycol_id.inserted_ids #返回insert_id集合，即插入文档的id值
		else:
			return "{},{}:类型错误,类型必须为string和list".format(collection_name,value_list)

	def select_one_collection(self,collection_name,search_col=None):#获取一条数据
		'''search_col：只能是dict类型,key大于等于一个即可，也可为空
		可使用修饰符查询：{"name": {"$gt": "H"}}#读取 name 字段中第一个字母 ASCII 值大于 "H" 的数据
		使用正则表达式查询：{"$regex": "^R"}#读取 name 字段中第一个字母为 "R" 的数据'''
		if isinstance(collection_name,str):
			my_col=self.mydb[collection_name]
			try:
				result = my_col.find_one(search_col)  # 这里只会返回一个对象，数据需要自己取
				return result
			except TypeError as e:
				print('查询条件只能是dict类型,具体错误信息：{}'.format(e))
				return None
		else:
			return "{}:类型错误,类型必须为string".format(collection_name)

	def select_all_collection(self,collection_name,search_col={},skip_col={},limit_num=sys.maxsize,sort_col=[()]):
		'''search_col：只能是dict类型,key大于等于一个即可，也可为空
		可使用修饰符查询：{"name": {"$gt": "H"}}#读取 name 字段中第一个字母 ASCII 值大于 "H" 的数据
		使用正则表达式查询：{"$regex": "^R"}#读取 name 字段中第一个字母为 "R" 的数据
		limit_num:返回指定条数记录，该方法只接受一个数字参数(sys.maxsize:返回一个最大的整数值)
		sort_col:排序字段，格式[("sort1":排序标识（1：升序，-1降序）),("sort2",排序标识)]'''
		if isinstance(sort_col,(list)):
			sort_col=sort_col
		elif isinstance(sort_col,(tuple)) and len(sort_col)<=1:
			sort_col=[sort_col]
		elif isinstance(sort_col,dict) and sort_col:
			sort_col=[k for k in sort_col.items()]
		else:
			sort_col=[()]
		if isinstance(collection_name,str):
			my_col=self.mydb[collection_name]
			try:
				if sort_col==False or sort_col==[()]:
					results=my_col.find(search_col,skip_col).limit(limit_num)#这里只会返回一个对象，数据需要自己取
				else:
					results = my_col.find(search_col,skip_col).sort(sort_col).limit(limit_num)  # 这里只会返回一个对象，数据需要自己取
				result_all=[i for i in results]#将获取到的数据添加至list
				return result_all
			except TypeError as e:
				print(e)
				print('查询条件只能是dict类型')
				return None
		else:
			return "{}:类型错误,类型必须为string".format(collection_name)

	def update_one_collecton(self,collection_name,search_col,update_col):
		'''该方法第一个参数为查询的条件，第二个参数为要修改的字段。
			如果查找到的匹配数据多余一条，则只会修改第一条。
			修改后字段的定义格式： { "$set": { "alexa": "12345" } }'''
		if isinstance(collection_name, str):
			my_col=self.mydb[collection_name]
			try:
				relust=my_col.update_one(search_col,update_col)
				return relust
			except TypeError as e:
				print('查询条件与需要修改的字段只能是dict类型')
				return None
		else:
			return "{}:类型错误,类型必须为string".format(collection_name)

	def update_batch_collecton(self,collection_name,search_col,update_col):
		# ,upsert=False, array_filters=True
		'''批量更新数据'''
		if isinstance(collection_name, str):
			my_col=self.mydb[collection_name]
			try:
				relust=my_col.update_many(search_col,update_col)
				return relust
			except TypeError as e:
				print(e)
				print('查询条件与需要修改的字段只能是dict类型')
				return None
		else:
			return "{}:类型错误,类型必须为string".format(collection_name)

	def delete_one_collection(self,collection_name,search_col):#删除集合中的文档
		if isinstance(collection_name, str):
			my_col = self.mydb[collection_name]
			try:
				relust=my_col.delete_one(search_col)
				return relust
			except TypeError as e:
				print('查询条件与需要修改的字段只能是dict类型')
				return None
		else:
			return "{}:类型错误,类型必须为string".format(collection_name)

	def delete_batch_collection(self,collection_name,search_col):#删除集合中的多个文档
		'''删除所有 name 字段中以 F 开头的文档:{ "name": {"$regex": "^F"} }
		删除所有文档：{}'''
		if isinstance(collection_name, str):
			my_col = self.mydb[collection_name]
			try:
				relust=my_col.delete_many(search_col)
				return relust
			except TypeError as e:
				print('查询条件与需要修改的字段只能是dict类型')
				return None
		else:
			return "{}:类型错误,类型必须为string".format(collection_name)

	def drop_collection(self,collection_name):
		'''删除集合，如果删除成功 drop() 返回 true，如果删除失败(集合不存在)则返回 false'''
		if isinstance(collection_name, str):
			my_col = self.mydb[collection_name]
			result=my_col.drop()
			return result
		else:
			return "{}:类型错误,类型必须为string".format(collection_name)

	def get_connections(self):#获取所有的connections
		return self.mydb.list_collection_names()

	def close_connect(self):
		self.connect_client.close()
		return 'mongo连接已关闭'



if __name__=="__main__":
	om=OperationMongo()
	om.select_one_collection('TestDataInfo')
