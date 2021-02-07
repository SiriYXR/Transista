# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: SettingView.py
@createTime: 2021-01-22 18:12:10
@updateTime: 2021-02-07 19:45:03
@codeLines: 316
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
			{
				"title": "累计翻译字符数",
				"detail": "",
				"accessory_type": "none"
			},
			{
				"title": "百度通用接口用量",
				"detail": "",
				"accessory_type": "none"
			},
			{
				"title": "百度领域接口用量",
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
				"detail": "自动翻译剪贴板中的文本，同时会清空剪贴板",
				"accessory_type": "none"
			},
			{
				"title": "切换翻译引擎",
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
		cell.text_label.text_color = self.father.FONTCOLOR_DEEP
		cell.detail_text_label.text = self.data[row]["detail"]
		cell.detail_text_label.text_color = self.father.FONTCOLOR_PASTAL
		cell.accessory_type = self.data[row]["accessory_type"]
		return cell

	def tableview_did_select(self, tableview, section, row):
		title = self.data[row]["title"]
		try:
			if (title == "切换翻译引擎"):
				self.father.SetEngineAct(None)
		except Exception as e:
			console.hud_alert('系统设置失败！', 'error', 1.0)
		finally:
			pass


class BaiduAPIDataSource(object):
	def __init__(self, app, father):
		self.app = app
		self.father = father

		self.data = [
			{
				"title": "appID",
				"detail": "",
				"accessory_type": "disclosure_indicator"
			},
			{
				"title": "Key",
				"detail": "",
				"accessory_type": "disclosure_indicator"
			},
			{
				"title": "自定义术语表",
				"detail": '仅开通了"我的术语库"的用户才可使用',
				"accessory_type": "none"
			},
			{
				"title": "百度翻译API主页",
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
			if (title == "appID"):
				self.set_appID_Act()
				
			if (title == "Key"):
				self.set_key_Act()
				
			if (title == "百度翻译API主页"):
				webbrowser.open("safari-https://fanyi-api.baidu.com")
				
		finally:
			pass
	
	@ui.in_background
	def set_appID_Act(self):
		try:
			appid=console.input_alert("设置百度appID","",self.father.baiduapi_appid,"保存")
			self.app.configService.SetBaiduAppID(appid)
			self.father.updateData()
			console.hud_alert('appID设置成功！', 'success', 1.0)
		except Exception as e:
			pass
		finally:
			pass
			
	@ui.in_background
	def set_key_Act(self):
		try:
			key=console.input_alert("设置百度Key","",self.father.baiduapi_key,"保存")
			self.app.configService.SetBaiduKey(key)
			self.father.updateData()
			console.hud_alert('Key设置成功！', 'success', 1.0)
		except Exception as e:
			pass
		finally:
			pass

class ClearDataSource(object):
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
			self.app.trans_history=[]
			self.father.updateData()
			console.hud_alert('系统初始化成功！', 'success', 1.0)
		except Exception as e:
			console.hud_alert('系统初始化失败！', 'error', 1.0)
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
				webbrowser.open(
					"safari-https://blog.siriyang.cn/posts/20210124124556id.html")
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
		self.count_transChartSum = 0
		self.count_baiduCommonTransChartUsed=[0,0,0]
		self.count_baiduFieldTransChartUsed=[0,0,0]
		
		self.setting_lesten = True
		self.setting_engine = "baidu_common"
		self.engineDic = {"baidu_common": "百度通用翻译", "baidu_field": "百度领域翻译"}
		
		self.baiduapi_appid=""
		self.baiduapi_key=""
		self.baiduapi_terminology=False

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
		self.count_transChartSumLabel = ui.Label()

		self.count_tableView.add_subview(self.count_runtimesLabel)
		self.count_tableView.add_subview(self.count_transChartSumLabel)
		self.scrollView.add_subview(self.count_titleLabel)
		self.scrollView.add_subview(self.count_tableView)

		self.setting_titleLabel = ui.Label()
		self.setting_tableView = ui.TableView()
		self.settingDataSource = SystemSettingDataSource(self.app, self)

		self.setting_lestenBtn = ui.Switch()
		self.setting_engineBtn = ui.Button()

		self.setting_tableView.add_subview(self.setting_lestenBtn)
		self.setting_tableView.add_subview(self.setting_engineBtn)
		self.scrollView.add_subview(self.setting_titleLabel)
		self.scrollView.add_subview(self.setting_tableView)

		self.baiduapi_titleLabel = ui.Label()
		self.baiduapi_tableView = ui.TableView()
		self.baiduapiDataSource = BaiduAPIDataSource(self.app, self)

		self.baiduapi_terminologyBtn = ui.Switch()
		
		self.baiduapi_tableView.add_subview(self.baiduapi_terminologyBtn)
		self.scrollView.add_subview(self.baiduapi_titleLabel)
		self.scrollView.add_subview(self.baiduapi_tableView)
		
		self.clear_titleLabel = ui.Label()
		self.clear_tableView = ui.TableView()
		self.clearDataSource = ClearDataSource(self.app, self)

		self.scrollView.add_subview(self.clear_titleLabel)
		self.scrollView.add_subview(self.clear_tableView)
		
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
		self.count_transChartSum = self.app.configService.GetTransChartSum()
		
		self.count_baiduCommonTransChartUsed=self.app.configService.GetBaiduCommonTransChartUsed()
		self.count_baiduFieldTransChartUsed=self.app.configService.GetBaiduFieldTransChartUsed()

		self.setting_engine = self.app.configService.GetEngine()
		
		self.baiduapi_appid=self.app.configService.GetBaiduAppID()
		self.baiduapi_key=self.app.configService.GetBaiduKey()
		self.baiduapi_terminology=self.app.configService.GetBaiduTerminology()
		

	def LoadUI(self):
		"""------------statistic-----------------"""
		self.count_titleLabel.frame = (20, 20, self.width - 40, 30)
		self.count_titleLabel.text = "数据统计"
		self.count_titleLabel.font = ("<System>", 15)
		self.count_titleLabel.text_color = self.FONTCOLOR_DEEP

		self.count_runtimesLabel.frame = (self.width - 240, 10, 200, 30)
		self.count_runtimesLabel.text = str(self.count_runtimes) + "次"
		self.count_runtimesLabel.font = ("<System>", 18)
		self.count_runtimesLabel.text_color = self.FONTCOLOR_PASTAL
		self.count_runtimesLabel.alignment = ui.ALIGN_RIGHT

		self.count_transChartSumLabel.frame = (self.width - 240, 60, 200, 30)
		self.count_transChartSumLabel.text = str(self.count_transChartSum) + "字符"
		self.count_transChartSumLabel.font = ("<System>", 18)
		self.count_transChartSumLabel.text_color = self.FONTCOLOR_PASTAL
		self.count_transChartSumLabel.alignment = ui.ALIGN_RIGHT
		
		self.countDataSource.data[2]['detail']="今日：{}；本月：{}；总计：{}".format(
			self.count_baiduCommonTransChartUsed[0],
			self.count_baiduCommonTransChartUsed[1],
			self.count_baiduCommonTransChartUsed[2])
			
		self.countDataSource.data[3]['detail']="今日：{}；本月：{}；总计：{}".format(
			self.count_baiduFieldTransChartUsed[0],
			self.count_baiduFieldTransChartUsed[1],
			self.count_baiduFieldTransChartUsed[2])
				
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
		self.setting_lestenBtn.action = self.SetLestenAct

		self.setting_engineBtn.frame = (self.width - 160, 60, 150, 30)
		self.setting_engineBtn.title = self.engineDic[self.setting_engine]
		self.setting_engineBtn.font = ("<System>", 16)
		self.setting_engineBtn.tint_color = self.FONTCOLOR_PASTAL
		self.setting_engineBtn.alignment = ui.ALIGN_RIGHT
		self.setting_engineBtn.action = self.SetEngineAct

		self.setting_tableView.data_source = self.settingDataSource
		self.setting_tableView.delegate = self.settingDataSource
		self.setting_tableView.row_height = 50
		self.setting_tableView.frame = (
			-1, self.setting_titleLabel.y + 30, self.width + 2,
			len(self.settingDataSource.data) * self.setting_tableView.row_height)
		self.setting_tableView.reload()
		"""------------------baidu api------------------"""
		self.baiduapi_titleLabel.frame = (
			20, self.setting_tableView.y + self.setting_tableView.height + 20,
			self.width - 40, 30)
		self.baiduapi_titleLabel.text = "百度翻译接口"
		self.baiduapi_titleLabel.font = ("<System>", 15)
		self.baiduapi_titleLabel.text_color = self.FONTCOLOR_DEEP
		
		self.baiduapiDataSource.data[0]['detail']=self.baiduapi_appid
		self.baiduapiDataSource.data[1]['detail']=self.baiduapi_key
		
		self.baiduapi_terminologyBtn.frame = (self.width - 70, 110, 100, 30)
		self.baiduapi_terminologyBtn.tint_color = "#0987b4"
		self.baiduapi_terminologyBtn.value = self.baiduapi_terminology
		self.baiduapi_terminologyBtn.action = self.SetBaiduTerminologyAct
		
		self.baiduapi_tableView.data_source = self.baiduapiDataSource
		self.baiduapi_tableView.delegate = self.baiduapiDataSource
		self.baiduapi_tableView.row_height = 50
		self.baiduapi_tableView.frame = (
			-1, self.baiduapi_titleLabel.y + 30, self.width + 2,
			len(self.baiduapiDataSource.data) * self.baiduapi_tableView.row_height)
		self.baiduapi_tableView.reload()
		
		"""------------------clear data------------------"""
		self.clear_titleLabel.frame = (
			20, self.baiduapi_tableView.y + self.baiduapi_tableView.height + 20,
			self.width - 40, 30)
		self.clear_titleLabel.text = "数据清理"
		self.clear_titleLabel.font = ("<System>", 15)
		self.clear_titleLabel.text_color = self.FONTCOLOR_WARNNING

		self.clear_tableView.data_source = self.clearDataSource
		self.clear_tableView.delegate = self.clearDataSource
		self.clear_tableView.row_height = 50
		self.clear_tableView.frame = (
			-1, self.clear_titleLabel.y + 30, self.width + 2,
			len(self.clearDataSource.data) * self.clear_tableView.row_height)
		self.clear_tableView.reload()
		
		"""------------------info------------------"""
		self.info_titleLabel.frame = (
			20, self.clear_tableView.y + self.clear_tableView.height + 20,
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
		self.copyrightLabel.text = "Copyright © 2021 by SiriYang v1.0"
		self.copyrightLabel.font = ("<System>", 15)
		self.copyrightLabel.text_color = self.FONTCOLOR_PASTAL

	def layout(self):
		self.LoadUI()

	def updateData(self):
		self.LoadData()
		self.LoadUI()

	def SetLestenAct(self, sender):
		self.app.isLestenningClipbord = self.setting_lestenBtn.value
		self.app.configService.SetIsLestenningClipbord(self.app.isLestenningClipbord)
	
	def SetBaiduTerminologyAct(self,sender):
		self.app.configService.SetBaiduTerminology(self.baiduapi_terminologyBtn.value)
	
	@ui.in_background
	def SetEngineAct(self, sender):

		try:
			index = console.alert("翻译引擎", "选择翻译时使用的引擎", "百度通用翻译", "百度领域翻译")
			self.setting_engineBtn.title = list(self.engineDic.values())[index - 1]
			self.setting_engine = list(self.engineDic.keys())[index - 1]
			self.app.configService.SetEngine(self.setting_engine)
		except Exception as e:
			pass
		finally:
			pass

