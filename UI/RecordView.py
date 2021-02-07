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
import logging

class HistoryDataSource (object):
	
	def __init__(self,app,father):
		self.app = app
		self.father = father
		
		self.logger = logging.getLogger(self.__class__.__name__)
		
	def tableview_number_of_sections(self,tableview):
		return 1
		
	def tableview_number_of_rows(self,tableview,section):
		return len(self.app.trans_history)
		
	def tableview_cell_for_row(self,tableview,section,row):
		cell = ui.TableViewCell('subtitle')
		cell.selectable=False
		history_len=len(self.app.trans_history)
		cell.text_label.text=self.app.trans_history[history_len-row-1][1]
		cell.detail_text_label.text=self.app.trans_history[history_len-row-1][0]
		
		return cell
	
	def tableview_did_select(self,tableview,section,row):
		history_len=len(self.app.trans_history)
		self.app.translateView.orgtext=self.app.trans_history[history_len-row-1][0]
		self.app.translateView.restext=self.app.trans_history[history_len-row-1][1]
		self.app.TranslateAct(None)
		self.logger.info("读取历史记录："+str(self.app.trans_history[history_len-row-1]))
		
	
class RecordView(ui.View):
	def __init__(self, app):
		self.app = app
		
		self.historyDataSource = HistoryDataSource(app,self)
		self.logger = logging.getLogger(self.__class__.__name__)
		
		self.name = '记录'
		self.background_color = 'white'
		self.frame = (0, 0, self.app.width, self.app.height)
		self.flex = 'WHLRTB'

		self.closeBtn = ui.ButtonItem()
		self.closeBtn.image = ui.Image.named('iob:close_round_24')
		self.closeBtn.action = self.app.CloseAct
		self.left_button_items = [self.closeBtn]
		
		self.historyTableView=ui.TableView()
		self.historyTableView.flex="WHLRTB"
		self.historyTableView.data_source = self.historyDataSource
		self.historyTableView.delegate = self.historyDataSource
		
		self.add_subview(self.historyTableView)
		
		self.LoadData()
		self.LoadUI()

	def LoadData(self):
		pass

	def LoadUI(self):
		self.historyTableView.frame=(0,0,self.width,self.height)
		self.historyTableView.reload()
		
	def layout(self):
		self.LoadUI()

	def updateData(self):
		self.LoadData()
		self.LoadUI()

