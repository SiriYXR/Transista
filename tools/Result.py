# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: Result.py
@time: 2019.12.25 12:43
@updateTime: 2021-02-06 20:28:06
@codeLines: 46
"""


class ResultEnum(object):
	"""
	返回结果枚举类型，积极结果使用偶数代码，消极结果使用奇数代码。
	"""

	# 基础
	UNKNOW_ERROR = (99999, "Unknow error")
	SUCCESS = (0, "Success")
	FAULT = (1, "Fault")

	# 翻译服务
	TRANSLATE_ERROR = (101, "翻译出错!")
	BAIDUAPPID_VOID = (111, "百度appID为空!")
	BAIDUKEY_VOID = (113, "百度Key为空!")

	# 网络
	URL_INVALID = (401, "这不是一个有效链接！")
	NET_TIME_OUT = (403, "连接超时！")


class Result(object):

	#Result code
	mCode = None

	#Result information
	mInfo = None

	#Result data
	mData = None

	def __init__(self, resultEnum, data=None):
		self.mCode = resultEnum[0]
		self.mInfo = resultEnum[1]			
		self.mData = data
		if data == None:
			self.mData = resultEnum[1]

	def __del__(self):
		pass

	def getCode(self):
		return self.mCode

	def setCode(self, code):
		self.mCode = code

	def getInfo(self):
		return self.mInfo

	def setInfo(self, info):
		self.mInfo = info

	def getData(self):
		return self.mData

	def setData(self, data):
		self.mData = data

	def equal(self, enum):
		return self.mCode == enum[0]

	def isPositive(self):
		if (self.mCode % 2 == 0):
			return True
		else:
			return False

	def toString(self):
		return "Error Code " + str(self.mCode) + " : " + self.mInfo


if __name__ == "__main__":
	res = Result(ResultEnum.SUCCESS)

	if (res.isPositive()):
		print(res.toString())

