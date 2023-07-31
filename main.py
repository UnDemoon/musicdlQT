"""
@Description:

@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-02-20 10:25:09
"""
#  基础模块
import logging
import os
import sys
import pyximport  # qt
pyximport.install()
import requests
from PyQt5 import QtWidgets, QtCore, QtGui
#   引入ui文件
from home import Ui_MainWindow as Ui
# 音乐搜索包
from musicdl import musicdl
#   工具引入
import utils as my_utils


logging.basicConfig(level=0)


class MyApp(QtWidgets.QMainWindow, Ui):
    def __init__(self):
        #   ui初始化
        QtWidgets.QMainWindow.__init__(self)
        Ui.__init__(self)
        self.setupUi(self)
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        self.music_api = musicdl.musicdl(config=my_utils.loadKeyJsonFile(config_file, 'music'))
        self.music_target = my_utils.loadKeyJsonFile(config_file, 'target')
        self.search_results = None
        self.check_boxes = []
        self.music_records = {}
        self.right_menu = QtWidgets.QMenu(self)
        self.action_download = QtWidgets.QAction('下载', self)  # 创建菜单选项对象
        self.__uiCustom()

    '''ui自定义补充'''

    def __uiCustom(self):
        self.tableWidget_reslist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 声明创建右键菜单
        self.tableWidget_reslist.customContextMenuRequested.connect(self.create_rightmenu)  # 连接到菜单显示函数
        self.action_download.triggered.connect(self.download)  # 将动作A触发时连接到槽函数 button
        self.checkBox_all.stateChanged.connect(self.check_change)  # 全选
        self.lineEdit_sreach.returnPressed.connect(self.search)  # 搜索
        self.pushButton_search.clicked.connect(self.search)  # 搜索
        for t_name, t_src in self.music_target.items():
            cb = QtWidgets.QCheckBox(t_name, self.centralwidget)
            cb.setCheckState(QtCore.Qt.Checked)
            self.check_boxes.append(cb)
            self.horizontalLayout_2.addWidget(cb)

    '''鼠标右键点击事件'''

    def create_rightmenu(self):
        # 菜单对象
        self.right_menu.addAction(self.action_download)  # 把动作A选项对象添加到菜单self.right_menu
        self.right_menu.popup(QtGui.QCursor.pos())  # 声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，

    '''全选/全不选'''

    def check_change(self, state):
        check_state = QtCore.Qt.Unchecked
        if state == QtCore.Qt.Checked:
            check_state = QtCore.Qt.Checked
        for cb in self.check_boxes:
            cb.setCheckState(check_state)

    '''音乐下载器'''

    def search(self):
        keyword = self.lineEdit_sreach.text()
        if not keyword:
            QtWidgets.QMessageBox().information(self, '提示', '关键词不能为空')
            return True
        selected_src_names = []
        for cb in self.check_boxes:
            if cb.isChecked():
                selected_src_names.append(cb.text())
        if len(selected_src_names) <= 0:
            QtWidgets.QMessageBox().information(self, '提示', '至少选择一个搜索源')
            return True
        target_srcs = [self.music_target.get(name) for name in selected_src_names]
        self.search_results = self.music_api.search(keyword, target_srcs)
        count, row = 0, 0
        for value in self.search_results.values():
            count += len(value)
        self.tableWidget_reslist.setRowCount(count)
        for _, (key, values) in enumerate(self.search_results.items()):
            for _, value in enumerate(values):
                for column, item in enumerate(
                        [value['singers'], value['songname'], value['filesize'], value['duration'],
                         value['album'], value['source']]):
                    self.tableWidget_reslist.setItem(row, column, QtWidgets.QTableWidgetItem(item))
                    self.music_records.update({str(row): value})
                row += 1
        return self.search_results

    '''下载'''

    def download(self):
        select_index = self.tableWidget_reslist.selectedItems()[0].row()
        songinfo = self.music_records.get(str(select_index))
        #   qq的属性名称不对 特殊处理
        if songinfo.get('source') == 'qqmusic':
            songinfo['source'] = 'qq'
        headers = musicdl.utils.Downloader(songinfo).headers
        musicdl.utils.checkDir(songinfo['savedir'])
        with requests.get(songinfo['download_url'], headers=headers, stream=True, verify=False) as response:
            if response.status_code == 200:
                total_size, chunk_size, download_size = int(response.headers.get('content-length', 102400)), 1024, 0
                with open(os.path.join(songinfo['savedir'], songinfo['savename'] + '.' + songinfo['ext']), 'wb') as fp:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            fp.write(chunk)
                            download_size += len(chunk)
                            self.progressBar.setValue(int(download_size / total_size * 100))
        QtWidgets.QMessageBox().information(self, '下载完成',
                                            '歌曲%s已经下载完成, 保存在当前路径的%s文件夹下' % (
                                                songinfo['savename'], songinfo['savedir']))
        self.progressBar.setValue(0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
