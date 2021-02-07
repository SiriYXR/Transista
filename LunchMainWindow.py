# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: LunchMainWindow.py
@createTime: 2021-01-22 16:05:58
@updateTime: 2021-01-22 16:10:36
@codeLines: 6
"""

import sys
sys.path.append('.')  # 将项目根目录加入模块搜索路径，这样其他模块才能成功导包

from UI.MainWindow import MainWindow

if __name__ == '__main__':
	mainWindow = MainWindow("./data/")
	mainWindow.launch()
