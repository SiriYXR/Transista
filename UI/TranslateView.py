# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: TranslateView.py
@createTime: 2021-01-22 17:59:04
@updateTime: 2021-01-23 17:09:09
@codeLines: 120
"""

import ui
import console
import clipboard
import time

from core.TranslateService import TranslateService

from tools.Result import *


class TranslateView(ui.View):

	# 按钮颜色
	BTN_ON_COLOR = '#27a2f1'
	BTN_OFF_COLOR = '#8e8e8e'

	def __init__(self, app):
		self.app = app
		self.transserv = TranslateService(app.rootpath)

		self.orgtext = ""
		self.restext = ""

		self.name = '翻译'
		self.background_color = '#f1f1f1'
		self.frame = (0, 0, self.app.width, app.height)
		self.flex = 'WHLRTB'

		self.closeBtn = ui.ButtonItem()
		self.closeBtn.image = ui.Image.named('iob:close_round_24')
		self.closeBtn.action = self.app.CloseAct
		self.left_button_items = [self.closeBtn]

		self.orgLabel = ui.Label()
		self.orgLabel.text = '原文'
		self.orgTextView = ui.TextView()

		self.resLabel = ui.Label()
		self.resLabel.text = '译文'
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
		self.add_subview(self.orgTextView)
		self.add_subview(self.resLabel)
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

		self.orgTextView.text = self.orgtext
		self.orgTextView.font = ("<system>", 16)

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

	def layout(self):

		bottomView_h = 50
		labe_h = 30
		labe_w = 100
		textView_h = (self.height - labe_h * 2 - bottomView_h) / 2
		self.orgLabel.frame = (10, 0, labe_w, labe_h)
		self.orgTextView.frame = (0, labe_h, self.width, textView_h)
		self.resLabel.frame = (10, self.orgTextView.y + self.orgTextView.height,
																									labe_w, labe_h)
		self.resTextView.frame = (0, self.resLabel.y + self.resLabel.height,
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
	
	def TranslateAct(self, sender):
		self.app.activity_indicator.start()
		self.orgtext = self.orgTextView.text
		if len(self.orgtext) == 0:
			console.hud_alert("原文为空！", "error", 1)
			return
		res = self.transserv.Translate(self.orgtext)
		if (res.isPositive()):
			self.restext = res.getData()
			self.resTextView.text = self.restext
		else:
			print(res.toString())
			console.hud_alert(res.getInfo(), "error", 1)
		self.app.activity_indicator.stop()

	def CleanAct(self, sender):
		self.orgTextView.text = ""
		self.resTextView.text = ""
		self.orgtext = ""
		self.restext = ""

	def PasteAct(self, sender):
		text = clipboard.get()
		if len(text) > 0:
			clipboard.set("")
			self.orgTextView.text = text
			self.orgtext = text

	@ui.in_background
	def LestenningClipbord(self):

		while True:
			time.sleep(0.1)
			if self.app.lesteningStatus == self.app.LESTENNING:
				text = clipboard.get()
				if len(text) > 0:
					clipboard.set("")
					self.orgTextView.text = text
					self.TranslateAct(None)

			elif self.app.lesteningStatus == self.app.PAUSE:
				continue
			elif self.app.lesteningStatus == self.app.STOP:
				break

