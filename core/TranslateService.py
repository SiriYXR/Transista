# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: TranslateService.py
@createTime: 2021-01-23 13:29:09
@updateTime: 2021-02-07 19:04:01
@codeLines: 125
"""

import http.client
import hashlib
import urllib
import random
import json
import logging

from .ConfigService import ConfigService

from tools.Result import *


class TranslateService(object):
	def __init__(self, rootpath):
		self.rootpath = rootpath
		self.configService = ConfigService(rootpath + "config.ini")
		self.logger = logging.getLogger(self.__class__.__name__)

	def Translate(self, orgtext):
		engine = self.configService.GetEngine()

		self.logger.info("使用" + engine + "引擎进行翻译...")

		if engine == "baidu_common":
			res = self.BaiduCommonAPI(orgtext)

		if engine == "baidu_field":
			res = self.BaiduFieldAPI(orgtext)

		return res

	def BaiduCommonAPI(self, orgtext):
		appid = self.configService.GetBaiduAppID()  # 接口appid
		if (len(appid) == 0):
			self.logger.error("百度appID为空！")
			return Result(ResultEnum.BAIDUAPPID_VOID)
		secretKey = self.configService.GetBaiduKey()  # 接口密钥
		if (len(secretKey) == 0):
			self.logger.error("百度secretKey为空！")
			return Result(ResultEnum.BAIDUKEY_VOID)

		maxlen = self.configService.GetBaiduRequestMaxLen()
		terminology="0"
		if(self.configService.GetBaiduTerminology()):
			terminology="1"

		httpClient = None
		myurl = self.configService.GetBaiduCommonAPI()

		# 配置请求URL
		fromLang = 'auto'  #原文语种
		toLang = 'zh'  #译文语种
		salt = random.randint(32768, 65536)
		# 检测翻译文本是否超过5000字符
		q = orgtext
		if len(q) > maxlen:
			q = q[:maxlen]
			self.logger.warning("原始文本长度超过字符上限，截断超出部分：" + orgtext[maxlen:])

		sign = appid + q + str(salt) + secretKey
		sign = hashlib.md5(sign.encode()).hexdigest()
		myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
			q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
				salt) + '&sign=' + sign+'&action='+terminology

		try:
			httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
			httpClient.request('GET', myurl)

			# response是HTTPResponse对象
			response = httpClient.getresponse()
			result_all = response.read().decode("utf-8")
			result = json.loads(result_all)

		except Exception as e:
			self.logger.error(str(e))
		finally:
			if httpClient:
				httpClient.close()

			if ('error_code' in result):
				self.logger.error("翻译出错！- " + str(result))
				return Result(ResultEnum.TRANSLATE_ERROR, result)

			self.logger.info("百度通用翻译结果：" + str(result))
			self.configService.BaiduCommonTransChartAdd(len(q))

			restext = ""
			for i in result['trans_result']:
				if len(restext) > 0:
					restext += "\n"
				restext += i['dst']

			if (len(orgtext) > maxlen):
				restext += "【已截断超出长度上限部分】"

			return Result(ResultEnum.SUCCESS, restext)

	def BaiduFieldAPI(self, orgtext):
		appid = self.configService.GetBaiduAppID()  # 接口appid
		if (len(appid) == 0):
			self.logger.error("百度appID为空！")
			return Result(ResultEnum.BAIDUAPPID_VOID)
		secretKey = self.configService.GetBaiduKey()  # 接口密钥
		if (len(secretKey) == 0):
			self.logger.error("百度secretKey为空！")
			return Result(ResultEnum.BAIDUKEY_VOID)

		maxlen = self.configService.GetBaiduRequestMaxLen()

		httpClient = None
		myurl = self.configService.GetBaiduFieldAPI()

		# 配置请求URL
		fromLang = 'auto'  # 原语言
		toLang = 'zh'  # 目标语言
		salt = random.randint(32768, 65536)
		# 检测翻译文本是否超过5000字符
		q = orgtext
		if len(q) > maxlen:
			q = q[:maxlen]
			self.logger.warning("原始文本长度超过字符上限，截断超出部分：" + orgtext[maxlen:])
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

		except Exception as e:
			self.logger.error(str(e))
		finally:
			if httpClient:
				httpClient.close()

			if ('error_code' in result):
				self.logger.error("翻译出错！- " + str(result))
				return Result(ResultEnum.TRANSLATE_ERROR, result)

			self.logger.info("百度领域翻译结果：" + str(result))
			self.configService.BaiduFieldTransChartAdd(len(q))

			restext = ""
			for i in result['trans_result']:
				if len(restext) > 0:
					restext += "\n"
				restext += i['dst']

			if (len(orgtext) > maxlen):
				restext += "【已截断超出长度上限部分】"

			return Result(ResultEnum.SUCCESS, restext)


if __name__ == "__main__":
	transserv = TranslateService("../data/")
	res = transserv.Translate("apple")
	print(res)

