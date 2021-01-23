# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: RecordView.py
@createTime: 2021-01-22 18:11:56
@updateTime: 2021-01-22 20:57:47
@codeLines: 24
"""

import ui
import console


class RecordView(ui.View):
	def __init__(self, app):
		self.app = app

		self.name = '记录'
		self.background_color = 'white'
		self.frame = (0, 0, self.app.width, app.height)
		self.flex = 'WHLRTB'

		self.closeBtn = ui.ButtonItem()
		self.closeBtn.image = ui.Image.named('iob:close_round_24')
		self.closeBtn.action = self.app.CloseAct
		self.left_button_items = [self.closeBtn]

		self.LoadData()
		self.LoadUI()

	def LoadData(self):
		pass

	def LoadUI(self):
		pass

	def layout(self):
		self.LoadUI()

	def updateData(self):
		self.LoadData()
		self.LoadUI()

