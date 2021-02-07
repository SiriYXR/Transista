# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: TranslateView.py
@createTime: 2021-01-22 17:59:04
@updateTime: 2021-02-07 14:43:18
@codeLines: 188
"""

import ui
import console
import clipboard
import time
import logging

from core.TranslateService import TranslateService

from tools.Result import *


class OrgTextViewDelegate(object):
	def __init__(self, fwind):
		self.fwind = fwind

	def textview_did_change(self, textview):
		text = textview.text.strip()
		if (len(text) == 0):
			self.fwind.orgtextlenLabel.text = ""
		else:
			self.fwind.orgtextlenLabel.text = str(len(text)) + "字符"


class TranslateView(ui.View):

	# 按钮颜色
	BTN_ON_COLOR = '#27a2f1'
	BTN_OFF_COLOR = '#8e8e8e'

	def __init__(self, app):
		self.app = app
		self.transserv = TranslateService(app.rootpath)
		self.logger = logging.getLogger(self.__class__.__name__)

		self.orgtext = ""
		self.restext = ""

		self.name = '翻译'
		self.background_color = '#f1f1f1'
		self.frame = (0, 0, self.app.width, self.app.height)
		self.flex = 'WHLRTB'

		self.closeBtn = ui.ButtonItem()
		self.closeBtn.image = ui.Image.named('iob:close_round_24')
		self.closeBtn.action = self.app.CloseAct
		self.left_button_items = [self.closeBtn]

		self.orgLabel = ui.Label()
		self.orgLabel.text = '原文'
		self.lestenBtn = ui.Button()
		self.orgtextlenLabel = ui.Label()
		self.orgTextView = ui.TextView()

		self.resLabel = ui.Label()
		self.resLabel.text = '译文'
		self.transtimeLabel = ui.Label()
		self.resTextView = ui.TextView()

		# 底部栏
		self.bottomView = ui.View()
		self.translateBtn = ui.Button()
		self.pasteBtn = ui.Button()
		self.cleanBtn = ui.Button()

		# 将按钮加入底部栏
		self.bottomView.add_subview(self.translateBtn)
		self.bottomView.add_subview(self.pasteBtn)
		self.bottomView.add_subview(self.cleanBtn)

		# 将所有视图加入主窗口
		self.add_subview(self.orgLabel)
		self.add_subview(self.lestenBtn)
		self.add_subview(self.orgtextlenLabel)
		self.add_subview(self.orgTextView)
		self.add_subview(self.resLabel)
		self.add_subview(self.transtimeLabel)
		self.add_subview(self.resTextView)
		self.add_subview(self.bottomView)

		self.LoadData()
		self.LoadUI()

		self.LestenningClipbord()

	def LoadData(self):
		pass

	def LoadUI(self):

		self.orgLabel.font = ("<system>", 20)
		self.resLabel.font = ("<system>", 20)

		self.orgtextlenLabel.text = ""
		self.orgtextlenLabel.font = ("<system>", 16)
		self.orgtextlenLabel.alignment = ui.ALIGN_RIGHT
		self.orgtextlenLabel.text_color = self.BTN_OFF_COLOR

		self.transtimeLabel.text = ""
		self.transtimeLabel.font = ("<system>", 16)
		self.transtimeLabel.alignment = ui.ALIGN_RIGHT
		self.transtimeLabel.text_color = self.BTN_OFF_COLOR

		self.orgTextView.text = self.orgtext
		self.orgTextView.font = ("<system>", 16)
		self.orgTextView.delegate = OrgTextViewDelegate(self)
		self.orgTextView.delegate.textview_did_change(self.orgTextView)

		self.resTextView.text = self.restext
		self.resTextView.font = ("<system>", 16)

		self.bottomView.background_color = "#fff"

		self.translateBtn.image = ui.Image.named('iow:loop_32')
		self.translateBtn.title = '重新翻译'
		self.translateBtn.action = self.TranslateAct
		self.translateBtn.tint_color = self.BTN_OFF_COLOR

		self.pasteBtn.image = ui.Image.named('iow:clipboard_32')
		self.pasteBtn.action = self.PasteAct
		self.pasteBtn.tint_color = self.BTN_OFF_COLOR

		self.cleanBtn.image = ui.Image.named('iow:trash_a_32')
		#self.cleanBtn.title = '清理'
		self.cleanBtn.action = self.CleanAct
		self.cleanBtn.tint_color = self.BTN_OFF_COLOR

		self.lestenBtn.image = ui.Image.named('iow:ios7_eye_32')
		self.lestenBtn.action = self.LestenAct
		if self.app.isLestenningClipbord:
			self.lestenBtn.tint_color = self.BTN_ON_COLOR
		else:
			self.lestenBtn.tint_color = self.BTN_OFF_COLOR

	def layout(self):

		bottomView_h = 50
		labe_h = 30
		labe_w = 100
		textView_h = (self.height - labe_h * 2 - bottomView_h) / 2
		self.resLabel.frame = (10, 0, labe_w, labe_h)
		self.transtimeLabel.frame = (self.width - 210, 0, 200, labe_h)
		self.resTextView.frame = (0, labe_h, self.width, textView_h)
		self.orgLabel.frame = (10, self.resTextView.y + self.resTextView.height,
																									labe_w, labe_h)
		self.lestenBtn.frame = (55, self.orgLabel.y, labe_h, labe_h)
		self.orgtextlenLabel.frame = (self.width - 210, self.orgLabel.y, 200, labe_h)
		self.orgTextView.frame = (0, self.orgLabel.y + self.orgLabel.height,
																												self.width, textView_h)
		self.bottomView.frame = (0, self.height - bottomView_h, self.width,
																											bottomView_h)

		self.pasteBtn.frame = (20, 0, 30, bottomView_h)
		self.cleanBtn.frame = (self.pasteBtn.x + self.pasteBtn.width + 10, 0, 30,
																									bottomView_h)
		self.translateBtn.frame = (self.width - 20 - 100, 0, 100, bottomView_h)

	def updateData(self):
		self.LoadData()
		self.LoadUI()

		self.LestenningClipbord()

	def TranslateAct(self, sender):
		self.app.activity_indicator.start()
		self.orgtext = self.orgTextView.text.strip()
		if len(self.orgtext) == 0:
			console.hud_alert("原文为空！", "error", 1)
			self.logger.warning("原文为空！")
			return

		start = time.clock()
		res = self.transserv.Translate(self.orgtext)
		transtime = time.clock() - start
		self.transtimeLabel.text = str(transtime)[:4] + "s"
		self.logger.info("翻译用时：" + self.transtimeLabel.text)

		if (res.isPositive()):
			self.resTextView.text = res.getData()
			self.restext = res.getData()
			self.app.trans_history.append([self.orgtext,self.restext])
		else:
			console.hud_alert(res.getInfo(), "error", 1)
			self.logger.error(res.getInfo() + " - " + str(res.getData()))
		self.app.activity_indicator.stop()

	def CleanAct(self, sender):
		self.orgTextView.text = ""
		self.resTextView.text = ""
		self.orgtext = ""
		self.restext = ""
		self.orgtextlenLabel.text = ""
		self.transtimeLabel.text = ""
		self.logger.info("清空文本框")

	def PasteAct(self, sender):
		text = clipboard.get()
		if len(text) > 0:
			clipboard.set("")
			self.orgTextView.text = text
			self.orgtext = text
			self.resTextView.text = ""
			self.transtimeLabel.text = ""
			self.orgTextView.delegate.textview_did_change(self.orgTextView)
			self.logger.info("从剪贴板粘贴内容：" + text)

	def LestenAct(self, sender):
		if (self.app.isLestenningClipbord):
			self.app.isLestenningClipbord = False
			self.app.lesteningStatus = self.app.STOP
			self.lestenBtn.tint_color = self.BTN_OFF_COLOR
			console.hud_alert("停止侦听剪贴板", "success", 1)
		else:
			self.app.isLestenningClipbord = True
			self.app.lesteningStatus = self.app.LESTENNING
			self.lestenBtn.tint_color = self.BTN_ON_COLOR
			self.LestenningClipbord()
			console.hud_alert("开启侦听剪贴板", "success", 1)
		self.app.configService.SetIsLestenningClipbord(self.app.isLestenningClipbord)

	@ui.in_background
	def LestenningClipbord(self):

		while True:
			time.sleep(0.1)
			if self.app.lesteningStatus == self.app.LESTENNING:
				text = clipboard.get()
				if len(text) > 0:
					clipboard.set("")
					self.orgTextView.text = text
					self.orgtext = text
					self.resTextView.text = ""
					self.transtimeLabel.text = ""
					self.orgTextView.delegate.textview_did_change(self.orgTextView)
					self.logger.info("侦听到剪贴板内容：" + text)
					self.TranslateAct(None)
			elif self.app.lesteningStatus == self.app.STOP:
				break


