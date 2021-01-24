# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: TranslateService.py
@createTime: 2021-01-23 13:29:09
@updateTime: 2021-01-23 19:11:56
@codeLines: 91
"""

import http.client
import hashlib
import urllib
import random
import json

from .ConfigService import ConfigService

from tools.Result import *


class TranslateService(object):
	def __init__(self, rootpath):
		self.rootpath = rootpath
		self.configService = ConfigService(rootpath + "config.ini")

	def Translate(self, orgtext):
		engine = self.configService.GetEngine()

		if engine == "baidu_common":
			restext = self.BaiduCommonAPI(orgtext)

		if engine == "baidu_field":
			restext = self.BaiduFieldAPI(orgtext)

		return restext

	def BaiduCommonAPI(self, orgtext):
		appid = self.configService.GetBaiduAppID()  # 接口appid
		secretKey = self.configService.GetBaiduKey()  # 接口密钥

		httpClient = None
		myurl = self.configService.GetBaiduCommonAPI()

		fromLang = 'auto'  #原文语种
		toLang = 'zh'  #译文语种
		salt = random.randint(32768, 65536)
		q = orgtext
		sign = appid + q + str(salt) + secretKey
		sign = hashlib.md5(sign.encode()).hexdigest()
		myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
			q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
				salt) + '&sign=' + sign

		try:
			httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
			httpClient.request('GET', myurl)

			# response是HTTPResponse对象
			response = httpClient.getresponse()
			result_all = response.read().decode("utf-8")
			result = json.loads(result_all)

		except Exception as e:
			print(e)
		finally:
			if httpClient:
				httpClient.close()

			print(result)

			if ('error_code' in result):
				return Result(ResultEnum.TRANSLATE_ERROR, result)

			restext = ""
			for i in result['trans_result']:
				if len(restext) > 0:
					restext += "\n"
				restext += i['dst']

			return Result(ResultEnum.SUCCESS, restext)

	def BaiduFieldAPI(self, orgtext):
		appid = self.configService.GetBaiduAppID()  # 接口appid
		secretKey = self.configService.GetBaiduKey()  # 接口密钥

		httpClient = None
		myurl = self.configService.GetBaiduFieldAPI()

		fromLang = 'auto'  # 原语言
		toLang = 'zh'  # 目标语言
		salt = random.randint(32768, 65536)
		q = orgtext  # 原文
		domain = self.configService.GetBaiduDomain()
		sign = appid + q + str(salt) + domain + secretKey
		sign = hashlib.md5(sign.encode()).hexdigest()
		myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
			q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
				salt) + '&domain=' + domain + '&sign=' + sign

		try:
			httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
			httpClient.request('GET', myurl)

			response = httpClient.getresponse()
			result_all = response.read().decode("utf-8")
			result = json.loads(result_all)

			print(result)

		except Exception as e:
			print(e)
		finally:
			if httpClient:
				httpClient.close()

			if ('error_code' in result):
				return Result(ResultEnum.TRANSLATE_ERROR, result)

			restext = ""
			for i in result['trans_result']:
				if len(restext) > 0:
					restext += "\n"
				restext += i['dst']

			return Result(ResultEnum.SUCCESS, restext)


if __name__ == "__main__":
	transserv = TranslateService("../data/")
	res = transserv.Translate("apple")
	print(res)

