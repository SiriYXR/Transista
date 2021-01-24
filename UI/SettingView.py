# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: SettingView.py
@createTime: 2021-01-22 18:12:10
@updateTime: 2021-01-24 12:08:38
@codeLines: 189
"""

import ui
import console
import webbrowser

from core.ConfigService import ConfigService

from tools.Result import *


class CountDataSource(object):
	def __init__(self, app, father):
		self.app = app
		self.father = father

		self.data = [
			{
				"title": "程序运行次数",
				"detail": "",
				"accessory_type": "none"
			},
		]

	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.selectable = False
		cell.text_label.text = self.data[row]["title"]
		cell.text_label.text_color = self.father.FONTCOLOR_DEEP
		cell.detail_text_label.text = self.data[row]["detail"]
		cell.detail_text_label.text_color = self.father.FONTCOLOR_PASTAL
		cell.accessory_type = self.data[row]["accessory_type"]
		return cell


class SystemSettingDataSource(object):
	def __init__(self, app, father):
		self.app = app
		self.father = father

		self.data = [
			{
				"title": "监听剪贴板",
				"detail": "",
				"accessory_type": "none"
			},
		]

	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.selectable = False
		cell.text_label.text = self.data[row]["title"]
		cell.text_label.text_color = self.father.FONTCOLOR_DEEP
		cell.detail_text_label.text = self.data[row]["detail"]
		cell.detail_text_label.text_color = self.father.FONTCOLOR_PASTAL
		cell.accessory_type = self.data[row]["accessory_type"]
		return cell

	def tableview_did_select(self, tableview, section, row):
		title = self.data[row]["title"]
		try:
			pass
		except Exception as e:
			console.hud_alert('Failed to setting', 'error', 1.0)
		finally:
			pass


class ClaerDataSource(object):
	def __init__(self, app, father):
		self.app = app
		self.father = father
		self.data = [
			{
				"title": "初始化系统",
				"detail": "",
				"accessory_type": "disclosure_indicator"
			},
		]

	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.selectable = False
		cell.text_label.text = self.data[row]["title"]
		cell.text_label.text_color = self.father.FONTCOLOR_WARNNING
		cell.detail_text_label.text = self.data[row]["detail"]
		cell.detail_text_label.text_color = self.father.FONTCOLOR_PASTAL
		cell.accessory_type = self.data[row]["accessory_type"]
		return cell

	def tableview_did_select(self, tableview, section, row):
		title = self.data[row]["title"]
		try:
			if (title == "初始化系统"):
				self.reset_system_Act()

		finally:
			pass

	@ui.in_background
	def reset_system_Act(self):
		if (console.alert(
				"初始化系统", '你确定要删除所有数据并重置系统吗?', '确定', '取消', hide_cancel_button=True) != 1):
			return
		self.app.activity_indicator.start()
		try:
			self.app.configService.Reset()
			console.hud_alert('系统初始化成功！', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to reset', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()


class InfoDataSource(object):
	def __init__(self, app, father):
		self.app = app
		self.father = father

		self.data = [
			{
				"title": "关于app",
				"detail": "",
				"accessory_type": "none"
			},
			{
				"title": "SiriYang的博客",
				"detail": "blog.siriyang.cn",
				"accessory_type": "none"
			},
			{
				"title": "GitHub",
				"detail": "",
				"accessory_type": "none"
			},
		]

	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.selectable = False
		cell.text_label.text = self.data[row]["title"]
		cell.text_label.text_color = self.father.FONTCOLOR_DEEP
		cell.detail_text_label.text = self.data[row]["detail"]
		cell.detail_text_label.text_color = self.father.FONTCOLOR_PASTAL
		cell.accessory_type = self.data[row]["accessory_type"]
		return cell

	def tableview_did_select(self, tableview, section, row):
		title = self.data[row]["title"]
		try:
			if (title == "关于app"):
				webbrowser.open("safari-https://blog.siriyang.cn")
			elif (title == "SiriYang的博客"):
				webbrowser.open("safari-https://blog.siriyang.cn")
			elif (title == "GitHub"):
				webbrowser.open("safari-https://github.com/SiriYXR/IstaTranslator")
		except Exception as e:
			console.hud_alert('Failed to process info', 'error', 1.0)
		finally:
			pass


class SettingView(ui.View):

	# 字体颜色
	FONTCOLOR_PASTAL = "#999999"
	FONTCOLOR_DEEP = "#5a5a5a"
	FONTCOLOR_WARNNING = "#f41414"

	def __init__(self, app):
		self.app = app

		self.count_runtimes = 0
		self.setting_lesten = True

		self.name = '设置'
		self.background_color = 'white'
		self.frame = (0, 0, self.app.width, self.app.height)
		self.flex = 'WHLRTB'

		self.closeBtn = ui.ButtonItem()
		self.closeBtn.image = ui.Image.named('iob:close_round_24')
		self.closeBtn.action = self.app.CloseAct
		self.left_button_items = [self.closeBtn]

		self.scrollView = ui.ScrollView()

		self.count_titleLabel = ui.Label()
		self.count_tableView = ui.TableView()
		self.countDataSource = CountDataSource(self.app, self)

		self.count_runtimesLabel = ui.Label()

		self.count_tableView.add_subview(self.count_runtimesLabel)
		self.scrollView.add_subview(self.count_titleLabel)
		self.scrollView.add_subview(self.count_tableView)

		self.setting_titleLabel = ui.Label()
		self.setting_tableView = ui.TableView()
		self.settingDataSource = SystemSettingDataSource(self.app, self)

		self.setting_lestenBtn = ui.Switch()

		self.setting_tableView.add_subview(self.setting_lestenBtn)
		self.scrollView.add_subview(self.setting_titleLabel)
		self.scrollView.add_subview(self.setting_tableView)

		self.info_titleLabel = ui.Label()
		self.info_tableView = ui.TableView()
		self.infoDataSource = InfoDataSource(self.app, self)

		self.scrollView.add_subview(self.info_titleLabel)
		self.scrollView.add_subview(self.info_tableView)

		self.copyrightLabel = ui.Label()
		self.scrollView.add_subview(self.copyrightLabel)

		self.add_subview(self.scrollView)

		self.LoadData()
		self.LoadUI()

	def LoadData(self):
		self.count_runtimes = self.app.configService.GetRunTimes()

	def LoadUI(self):
		"""------------statistic-----------------"""
		self.count_titleLabel.frame = (20, 20, self.width - 40, 30)
		self.count_titleLabel.text = "数据统计"
		self.count_titleLabel.font = ("<System>", 15)
		self.count_titleLabel.text_color = self.FONTCOLOR_DEEP

		self.count_runtimesLabel.frame = (self.width - 140, 10, 100, 30)
		self.count_runtimesLabel.text = str(self.count_runtimes) + "次"
		self.count_runtimesLabel.font = ("<System>", 18)
		self.count_runtimesLabel.text_color = self.FONTCOLOR_PASTAL
		self.count_runtimesLabel.alignment = ui.ALIGN_RIGHT

		self.count_tableView.data_source = self.countDataSource
		self.count_tableView.delegate = self.countDataSource

		self.count_tableView.row_height = 50
		self.count_tableView.frame = (
			-1, self.count_titleLabel.y + 30, self.width + 2,
			len(self.countDataSource.data) * self.count_tableView.row_height)
		self.count_tableView.reload()
		"""------------------system setting------------------"""

		self.setting_titleLabel.frame = (
			20, self.count_tableView.y + self.count_tableView.height + 20,
			self.width - 40, 30)
		self.setting_titleLabel.text = "设置选项"
		self.setting_titleLabel.font = ("<System>", 15)
		self.setting_titleLabel.text_color = self.FONTCOLOR_DEEP

		self.setting_lestenBtn.frame = (self.width - 70, 10, 100, 30)
		self.setting_lestenBtn.tint_color = "#0987b4"
		self.setting_lestenBtn.value = self.app.isLestenningClipbord
		self.setting_lestenBtn.action = self.Lesten_ST_Act

		self.setting_tableView.data_source = self.settingDataSource
		self.setting_tableView.delegate = self.settingDataSource
		self.setting_tableView.row_height = 50
		self.setting_tableView.frame = (
			-1, self.setting_titleLabel.y + 30, self.width + 2,
			len(self.settingDataSource.data) * self.setting_tableView.row_height)
		self.setting_tableView.reload()
		"""------------------baidu api------------------"""
		"""------------------clear data------------------"""
		"""------------------info------------------"""
		self.info_titleLabel.frame = (
			20, self.setting_tableView.y + self.setting_tableView.height + 20,
			self.width - 40, 30)
		self.info_titleLabel.text = "更多信息"
		self.info_titleLabel.font = ("<System>", 15)
		self.info_titleLabel.text_color = self.FONTCOLOR_DEEP

		self.info_tableView.data_source = self.infoDataSource
		self.info_tableView.delegate = self.infoDataSource
		self.info_tableView.row_height = 50

		self.info_tableView.frame = (
			-1, self.info_titleLabel.y + 30, self.width + 2,
			len(self.infoDataSource.data) * self.info_tableView.row_height)
		self.info_tableView.reload()

		self.scrollView.frame = (0, 0, self.width, self.height)
		self.scrollView.content_size = (
			self.width, self.info_tableView.y + self.info_tableView.height + 60)
		self.scrollView.background_color = "#fafafa"

		self.copyrightLabel.frame = (
			0, self.info_tableView.y + self.info_tableView.height + 30, self.width, 20)
		self.copyrightLabel.alignment = ui.ALIGN_CENTER
		self.copyrightLabel.text = "Copyright © 2021 by SiriYang v0.1"
		self.copyrightLabel.font = ("<System>", 15)
		self.copyrightLabel.text_color = self.FONTCOLOR_PASTAL

	def layout(self):
		self.LoadUI()

	def updateData(self):
		self.LoadData()
		self.LoadUI()

	def Lesten_ST_Act(self, sender):
		self.app.isLestenningClipbord = self.setting_lestenBtn.value
		self.app.configService.SetIsLestenningClipbord(self.app.isLestenningClipbord)

