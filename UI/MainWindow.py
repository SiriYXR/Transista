# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: MainWindow.py
@createTime: 2021-01-22 16:11:11
@updateTime: 2021-01-23 19:12:15
@codeLines: 164
"""

import ui
import console

from .TranslateView import TranslateView
from .RecordView import RecordView
from .SettingView import SettingView

from core.ConfigService import ConfigService


class MainWindow(ui.View):

	# 方向
	LANDSCAPE = 0
	PORTRAIT = 1

	# 测试
	NORMAL = 0
	TEST_1OF3 = 1

	# 页面
	TRANSLATE = 0
	RECORD = 1
	SETTING = 3
	
	# 剪贴板监听
	LESTENNING=0
	PAUSE=1
	STOP=2
			
	# 按钮颜色
	BTN_ON_COLOR = '#27a2f1'
	BTN_OFF_COLOR = '#8e8e8e'

	def __init__(self, rootpath, test_mod=0):
		self.name = 'IstaTranslator'
		self.rootpath = rootpath
		self.configService = ConfigService(rootpath + "config.ini")

		self.orientation = self.LANDSCAPE
		self.test_mod = test_mod

		self.viewKind = self.TRANSLATE
		self.translateDeep = 0
		self.recordDeep = 0
		self.settingDeep = 0
		
		self.isLestenningClipbord = self.configService.GetIsLestenningClipbord()
		if self.isLestenningClipbord :
			self.lesteningStatus = self.LESTENNING
		else:
			self.lesteningStatus = self.PAUSE
		
		# 状态指示器
		self.activity_indicator = ui.ActivityIndicator(flex='LTRB')
		self.activity_indicator.center = self.center
		self.activity_indicator.style = ui.ACTIVITY_INDICATOR_STYLE_GRAY

		# 中心导航视图
		self.translateView = TranslateView(self)
		self.recordView = RecordView(self)
		self.settingView = SettingView(self)
		
		self.translateNavi = ui.NavigationView(self.translateView)
		self.recordNavi = ui.NavigationView(self.recordView)
		self.settingNavi = ui.NavigationView(self.settingView)

		# 底部栏
		self.bottomView = ui.View()
		self.translateBtn = ui.Button()
		self.recordBtn = ui.Button()
		self.settingBtn = ui.Button()

		# 将按钮加入底部栏
		self.bottomView.add_subview(self.translateBtn)
		self.bottomView.add_subview(self.recordBtn)
		self.bottomView.add_subview(self.settingBtn)

		# 将所有视图加入主窗口
		self.add_subview(self.translateNavi)
		self.add_subview(self.recordNavi)
		self.add_subview(self.settingNavi)
		self.add_subview(self.bottomView)
		self.add_subview(self.activity_indicator)

		self.LoadUI()

		self.activity_indicator.bring_to_front()

	def LoadUI(self):
		self.recordNavi.hidden = True
		self.settingNavi.hidden = True

		self.bottomView.background_color = '#f1f1f1'

		self.translateBtn.image = ui.Image.named('iow:search_32')
		self.translateBtn.title = '翻译'
		self.translateBtn.action = self.TranslateAct
		self.translateBtn.tint_color = self.BTN_ON_COLOR

		self.recordBtn.image = ui.Image.named('iow:ios7_bookmarks_32')
		self.recordBtn.title = '记录'
		self.recordBtn.action = self.RecordAct
		self.recordBtn.tint_color = self.BTN_OFF_COLOR

		self.settingBtn.image = ui.Image.named('iow:ios7_gear_32')
		self.settingBtn.title = '设置'
		self.settingBtn.action = self.SettingAct
		self.settingBtn.tint_color = self.BTN_OFF_COLOR

	def layout(self):
		if self.width > self.height:
			self.orientation = self.LANDSCAPE
		else:
			self.orientation = self.PORTRAIT

		bottomView_h = 60

		self.translateNavi.frame = (0, 0, self.width, self.height - bottomView_h)
		self.recordNavi.frame = (0, 0, self.width, self.height - bottomView_h)
		self.settingNavi.frame = (0, 0, self.width, self.height - bottomView_h)

		self.bottomView.frame = (0, self.height - bottomView_h, self.width,
																											bottomView_h)

		btn_w = 100
		btn_margin = (self.width - btn_w * 3) / 4
		self.translateBtn.frame = (btn_margin, 0, btn_w, bottomView_h)
		self.recordBtn.frame = (btn_margin * 2 + btn_w, 0, btn_w, bottomView_h)
		self.settingBtn.frame = (btn_margin * 3 + btn_w * 2, 0, btn_w, bottomView_h)

	def launch(self):
		if self.test_mod == self.NORMAL:
			self.present(style='fullscreen', hide_title_bar=True)
		else:
			self.present(style='sheet', hide_title_bar=True)
		self.configService.RunTimesAddOne()

	def TranslateAct(self, sender):
		if self.viewKind == self.TRANSLATE:
			return
		self.activity_indicator.start()
		if self.isLestenningClipbord :
			self.lesteningStatus = self.LESTENNING
		else:
			self.lesteningStatus = self.PAUSE
			
		try:
			self.translateView.updateData()
			self.translateNavi.hidden = False
			self.recordNavi.hidden = True
			self.settingNavi.hidden = True
			for i in range(self.recordDeep):
				self.recordNavi.pop_view()
			for i in range(self.settingDeep):
				self.settingNavi.pop_view()
		except Exception as e:
			console.hud_alert('翻译页面加载失败！', 'error', 1.0)
		finally:
			self.viewKind = self.TRANSLATE
			self.translateBtn.tint_color = self.BTN_ON_COLOR
			self.recordBtn.tint_color = self.BTN_OFF_COLOR
			self.settingBtn.tint_color = self.BTN_OFF_COLOR
			self.activity_indicator.stop()

	def RecordAct(self, sender):
		if self.viewKind == self.RECORD:
			return
		self.activity_indicator.start()
		self.lesteningStatus = self.PAUSE
		try:
			self.recordView.updateData()
			self.translateNavi.hidden = True
			self.recordNavi.hidden = False
			self.settingNavi.hidden = True
			for i in range(self.translateDeep):
				self.recordNavi.pop_view()
			for i in range(self.settingDeep):
				self.settingNavi.pop_view()
		except Exception as e:
			console.hud_alert('记录页面加载失败！', 'error', 1.0)
		finally:
			self.viewKind = self.RECORD
			self.translateBtn.tint_color = self.BTN_OFF_COLOR
			self.recordBtn.tint_color = self.BTN_ON_COLOR
			self.settingBtn.tint_color = self.BTN_OFF_COLOR
			self.activity_indicator.stop()

	def SettingAct(self, sender):
		if self.viewKind == self.SETTING:
			return
		self.activity_indicator.start()
		self.lesteningStatus = self.PAUSE
		try:
			self.settingView.updateData()
			self.translateNavi.hidden = True
			self.recordNavi.hidden = True
			self.settingNavi.hidden = False
			for i in range(self.translateDeep):
				self.recordNavi.pop_view()
			for i in range(self.recordDeep):
				self.settingNavi.pop_view()
		except Exception as e:
			console.hud_alert('设置页面加载失败！', 'error', 1.0)
		finally:
			self.viewKind = self.SETTING
			self.translateBtn.tint_color = self.BTN_OFF_COLOR
			self.recordBtn.tint_color = self.BTN_OFF_COLOR
			self.settingBtn.tint_color = self.BTN_ON_COLOR
			self.activity_indicator.stop()

	def CloseAct(self, sender):
		self.lesteningStatus = self.STOP
		self.close()

