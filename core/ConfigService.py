# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: ConfigService.py
@createTime: 2021-01-22 21:33:45
@updateTime: 2021-01-23 19:11:48
@codeLines: 101
"""

import configparser

from tools.Result import *

class ConfigService(object):
	def __init__(self, path):
		self.path = path
		self.conf = configparser.ConfigParser()

	def Reset(self):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['runtimes'] = self.conf['default']['runtimes']
		self.conf['system']['engine'] = self.conf['default']['engine']
		self.conf['system']['is_lestenning_clipbord'] = self.conf['default']['is_lestenning_clipbord']

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

	def RunTimesAddOne(self):
		self.conf.read(self.path, encoding='utf-8')

		runtimes = self.conf.getint('system', 'runtimes')
		self.conf['system']['runtimes'] = str(runtimes + 1)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)
	
	def GetRunTimes(self):
		self.conf.read(self.path, encoding='utf-8')

		runtimes = self.conf.getint('system', 'runtimes')
		
		return runtimes
	
	def GetEngine(self):
		self.conf.read(self.path, encoding='utf-8')

		engine = self.conf['system']['engine']

		return engine

	def SetEngine(self, engine):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['engine'] = str(engine)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

	def SetEngineBaiduCommon(self):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['engine'] = "baidu_common"

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

	def SetEngineBaiduField(self):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['engine'] = "baidu_field"

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

	def GetIsLestenningClipbord(self):
		self.conf.read(self.path, encoding='utf-8')

		is_lestenning_clipbord = self.conf.getboolean('system','is_lestenning_clipbord')

		return is_lestenning_clipbord

	def SetIsLestenningClipbord(self, v):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['system']['is_lestenning_clipbord'] = str(v)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

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

	def GetBaiduKey(self):
		self.conf.read(self.path, encoding='utf-8')

		key = self.conf['baidu_api']['key']

		return key

	def SetBaiduKey(self, key):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['key'] = str(key)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

	def GetBaiduCommonAPI(self):
		self.conf.read(self.path, encoding='utf-8')

		common_api = self.conf['baidu_api']['common_api']

		return common_api

	def SetBaiduCommonAPI(self, common_api):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['common_api'] = str(common_api)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

	def GetBaiduFieldAPI(self):
		self.conf.read(self.path, encoding='utf-8')

		field_api = self.conf['baidu_api']['field_api']

		return field_api

	def SetBaiduFieldAPI(self, field_api):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['field_api'] = str(field_api)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

	def GetBaiduDomain(self):
		self.conf.read(self.path, encoding='utf-8')

		domain = self.conf['baidu_api']['domain']

		return domain

	def SetBaiduDomain(self, domain):
		self.conf.read(self.path, encoding='utf-8')

		self.conf['baidu_api']['domain'] = str(domain)

		with open(self.path, 'w', encoding='utf-8') as fp:
			self.conf.write(fp)

	def Content(self):
		content = ""
		with open(self.path, 'r', encoding="utf-8") as fp:
			content = fp.read()
			fp.close()
		return content


if __name__ == "__main__":
	conf = ConfigService("../data/config.ini")
	print(conf.Content())
	
