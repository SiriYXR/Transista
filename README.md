# Transista
&emsp;&emsp;—— 基于Pythonista的iPad论文阅读翻译工具。

&emsp;&emsp;[GitHub项目地址](https://github.com/SiriYXR/AppWishList)

&emsp;&emsp;[详细使用文档与项目介绍](https://blog.siriyang.cn/posts/20210124124556id.html)

## 快速安装

&emsp;&emsp;直接在控制台输入以下命令运行或者创建一个新.py文件然后粘贴该命令运行。使用命令运行将会默认安装在根目录，即“`This iPad/iPhone`”目录下，安装好之后你可以再挪动文件夹位置。

```python
import requests as r;exec(r.get('http://img.siriyang.cn/source/Transista/installer.py').content)
```

## 快速开始

&emsp;&emsp;首先需要注册申请[百度翻译API账](https://fanyi-api.baidu.com/)号，[申请教程](https://blog.siriyang.cn/posts/20201013145557id.html)。

&emsp;&emsp;然后在`设置/百度翻译接口`中对应位置填上自己的`appid`和`key`。

&emsp;&emsp;然后运行文件夹下的`LunchMainWindow.py`即可。

---

## 更新日志

### 2021.02.09 v1.0.2
* 修复百度翻译接口用量统计BUG
* 优化代码

### 2021.02.08 v1.0.1
* 修复BUG
* 将粘贴按钮的操作由直接替换原文改为追加粘贴内容

### 2021.02.07 v1.0.0

* V1.0正式发布，主要功能基本完成。
* 加入翻译历史记录页面
* 加入剪贴板侦听控制按钮
* 加入术语表选项控制按钮
* 加入翻译量统计功能
* 加入数据清理功能
* 加入日志输出
* 完善各种细节

### 2021.01.24 v0.1.0

* 发布测试版，仅实现简单的翻译功能。
