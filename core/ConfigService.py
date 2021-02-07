# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: ConfigService.py
@createTime: 2021-01-22 21:33:45
@updateTime: 2021-02-07 19:03:52
@codeLines: 247
"""

import configparser
import logging
from datetime import datetime

from tools.Result import *


class ConfigService(object):
	def __init__(self, path):
		self.path = path
		self.conf = configparser.ConfigParser()
		self.logger = logging.getLogger(self.__class__.__name__)

	def Reset(self):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['runtimes'] = self.conf['default']['runtimes']
		self.conf['system']['trans_chart_sum'] = self.conf['default'][
			'trans_chart_sum']
		self.conf['system']['engine'] = self.conf['default']['engine']
		self.conf['system']['is_lestenning_clipbord'] = self.conf['default'][
			'is_lestenning_clipbord']
		self.conf['system']['last_trans_date'] = self.conf['default']['last_trans_date']
			
		self.conf['baidu_api']['terminology'] = str(False)
			
		self.conf['baidu_api']['common_trans_cahrt_today']="0"
		self.conf['baidu_api']['common_trans_cahrt_month']="0"
		self.conf['baidu_api']['common_trans_cahrt_sum']="0"
		self.conf['baidu_api']['field_trans_cahrt_today']="0"
		self.conf['baidu_api']['field_trans_cahrt_month']="0"
		self.conf['baidu_api']['field_trans_cahrt_sum']="0"

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("重置配置文件")

	def RunTimesAddOne(self):
		self.conf.read(self.path, encoding='utf-8')

		runtimes = self.conf.getint('system', 'runtimes')
		self.conf['system']['runtimes'] = str(runtimes + 1)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("更新程序运行次数：" + str(runtimes + 1))

	def GetRunTimes(self):
		self.conf.read(self.path, encoding='utf-8')

		runtimes = self.conf.getint('system', 'runtimes')

		return runtimes

	def TransChartSumAdd(self, v):
		self.conf.read(self.path, encoding='utf-8')

		trans_chart_sum = self.conf.getint('system', 'trans_chart_sum') + v
		self.conf['system']['trans_chart_sum'] = str(trans_chart_sum)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("更新累计翻译字符数：" + str(trans_chart_sum))
		
		self.UpdateLastTransDate()

	def GetTransChartSum(self):
		self.conf.read(self.path, encoding='utf-8')

		res = self.conf.getint('system', 'trans_chart_sum')

		return res

	def GetEngine(self):
		self.conf.read(self.path, encoding='utf-8')

		engine = self.conf['system']['engine']

		return engine

	def SetEngine(self, engine):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['engine'] = str(engine)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置翻译引擎为：" + engine)

	def SetEngineBaiduCommon(self):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['engine'] = "baidu_common"

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置翻译引擎为：百度API标准版")

	def SetEngineBaiduField(self):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['engine'] = "baidu_field"

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置翻译引擎为：百度API垂直领域版")

	def GetIsLestenningClipbord(self):
		self.conf.read(self.path, encoding='utf-8')

		is_lestenning_clipbord = self.conf.getboolean('system','is_lestenning_clipbord')

		return is_lestenning_clipbord

	def SetIsLestenningClipbord(self, v):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['is_lestenning_clipbord'] = str(v)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置剪贴板监听参数：" + str(v))
	
	def UpdateTransChartStatistic(self):
		self.logger.info("更新翻译字符数统计量...")
		self.conf.read(self.path, encoding='utf-8')
		
		last_date=self.conf['system']['last_trans_date']
		if(len(last_date)==0):
			self.logger.info("还未进行过翻译操作")
			return
		
		nowdate=datetime.now()
		lastdate=datetime.strptime(last_date,"%Y-%m-%d %H:%M:%S")
		
		same_day=True
		same_month=True
		
		if(nowdate.year!=lastdate.year):
			same_day=False
			same_month=False
		elif (nowdate.month!=lastdate.month):
			same_day=False
			same_month=False
		elif (nowdate.day!=lastdate.day):
			same_day=False
			
		if(not same_day):
			self.conf['baidu_api']['common_trans_cahrt_today']="0"	
			self.conf['baidu_api']['field_trans_cahrt_today']="0"
			self.logger.info("重置今日用量")
			
		if(not same_month):
			self.conf['baidu_api']['common_trans_cahrt_month']="0"	
			self.conf['baidu_api']['field_trans_cahrt_month']="0"
			self.logger.info("重置本月用量")
			
		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		
	def GetLastTransDate(self):
		self.conf.read(self.path, encoding='utf-8')

		res = self.conf['system']['last_trans_date']

		return res
		
	def SetLastTransDate(self,v):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['last_trans_date']=str(v)
		
		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置上一次翻译日期：" + str(v))
		
	def UpdateLastTransDate(self):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['last_trans_date'] = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("更新上一次翻译日期：" + self.conf['system']['last_trans_date'])
	
	#------------baidu_api-------------------

	def GetBaiduAppID(self):
		self.conf.read(self.path, encoding='utf-8')

		appid = self.conf['baidu_api']['appid']

		return appid

	def SetBaiduAppID(self, appid):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['appid'] = str(appid)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置百度AppID：" + appid)

	def GetBaiduKey(self):
		self.conf.read(self.path, encoding='utf-8')

		key = self.conf['baidu_api']['key']

		return key

	def SetBaiduKey(self, key):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['key'] = str(key)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置百度Key：" + key)

	def GetBaiduRequestMaxLen(self):
		self.conf.read(self.path, encoding='utf-8')

		res = self.conf.getint('baidu_api', 'request_maxlen')

		return res

	def SetBaiduRequestMaxLen(self, v):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['request_maxlen'] = str(v)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置百度接口单次请求最大长度为：" + str(v))

	def GetBaiduCommonAPI(self):
		self.conf.read(self.path, encoding='utf-8')

		common_api = self.conf['baidu_api']['common_api']

		return common_api

	def SetBaiduCommonAPI(self, common_api):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['common_api'] = str(common_api)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置百度common_api：" + common_api)

	def GetBaiduTerminology(self):
		self.conf.read(self.path, encoding='utf-8')

		res = self.conf.getboolean('baidu_api','terminology')

		return res

	def SetBaiduTerminology(self, v):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['terminology'] = str(v)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置百度terminology：" + str(v))

	def GetBaiduFieldAPI(self):
		self.conf.read(self.path, encoding='utf-8')

		field_api = self.conf['baidu_api']['field_api']

		return field_api

	def SetBaiduFieldAPI(self, field_api):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['field_api'] = str(field_api)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置百度field_api：" + field_api)

	def GetBaiduDomain(self):
		self.conf.read(self.path, encoding='utf-8')

		domain = self.conf['baidu_api']['domain']

		return domain

	def SetBaiduDomain(self, domain):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['domain'] = str(domain)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("设置百度domain：" + domain)
		
	def GetBaiduCommonTransChartUsed(self):
		self.conf.read(self.path, encoding='utf-8')

		res=[]
		res.append(self.conf.getint('baidu_api','common_trans_cahrt_today'))
		res.append(self.conf.getint('baidu_api','common_trans_cahrt_month'))
		res.append(self.conf.getint('baidu_api','common_trans_cahrt_sum'))

		return res
	
	def BaiduCommonTransChartAdd(self,v):
		self.conf.read(self.path, encoding='utf-8')

		res=[]
		res.append(self.conf.getint('baidu_api','common_trans_cahrt_today')+v)
		res.append(self.conf.getint('baidu_api','common_trans_cahrt_month')+v)
		res.append(self.conf.getint('baidu_api','common_trans_cahrt_sum')+v)

		self.conf['baidu_api']['common_trans_cahrt_today'] = str(res[0])
		self.conf['baidu_api']['common_trans_cahrt_month'] = str(res[0])
		self.conf['baidu_api']['common_trans_cahrt_sum'] = str(res[0])

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("更新百度通用接口翻译字符数：" + str(res))
		
		self.TransChartSumAdd(v)
		
	def GetBaiduFieldTransChartUsed(self):
		self.conf.read(self.path, encoding='utf-8')

		res=[]
		res.append(self.conf.getint('baidu_api','field_trans_cahrt_today'))
		res.append(self.conf.getint('baidu_api','field_trans_cahrt_month'))
		res.append(self.conf.getint('baidu_api','field_trans_cahrt_sum'))

		return res

	def BaiduFieldTransChartAdd(self,v):
		self.conf.read(self.path, encoding='utf-8')

		res=[]
		res.append(self.conf.getint('baidu_api','field_trans_cahrt_today')+v)
		res.append(self.conf.getint('baidu_api','field_trans_cahrt_month')+v)
		res.append(self.conf.getint('baidu_api','field_trans_cahrt_sum')+v)

		self.conf['baidu_api']['field_trans_cahrt_today'] = str(res[0])
		self.conf['baidu_api']['field_trans_cahrt_month'] = str(res[0])
		self.conf['baidu_api']['field_trans_cahrt_sum'] = str(res[0])

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

		self.logger.info("更新百度领域接口翻译字符数：" + str(res))
		
		self.TransChartSumAdd(v)

	def Content(self):
		content = ""
		with open(self.path, 'r', encoding="utf-8") as fp:
			content = fp.read()
			fp.close()
		return content


if __name__ == "__main__":
	conf = ConfigService("../data/config.ini")
	print(conf.Content())
	
	
