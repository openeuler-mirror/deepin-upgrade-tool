"""
Copyright (C) 2022 Uniontech Software Technology Co., Ltd.

This program is free software; you can redistribute it and/or modify it under the terms of version 3 of the GNU General
 Public License as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; If not,
see <https://www.gnu.org/licenses/gpl-3.0.html&gt;.

To contact us about this file by physical or electronic mail, you may find current contact information at
 https://www.uniontech.com/.
"""

import sys
import datetime
import gettext
import logging
from PyQt5.QtWidgets import QApplication, QCheckBox, QTextBrowser, QHeaderView, QPushButton, QLabel, QWidget, \
    QTableWidgetItem, QTableWidget, QDesktopWidget, QMainWindow, QAbstractItemView, QHBoxLayout, QStyle, \
    QStyleOptionButton, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QFont, QPixmap, QCursor, QIcon
from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication, QEvent, QObject, pyqtSignal, QProcess, QTimer
from com_deepin_upgrade.config import LOGO, TRAY_INTERVAL, I18N_DOMAIN, LOCALE_PATH
from com_deepin_upgrade.utils import get_available_update_rpmpkgs
from com_deepin_upgrade.qss import qss_style
from com_deepin_upgrade.dnf import RpmType

locale_path = LOCALE_PATH
gettext.bindtextdomain(I18N_DOMAIN, locale_path)
gettext.textdomain(I18N_DOMAIN)
_ = gettext.gettext


class Ui_pkgs_upgrade(QMainWindow):
    sucess_code = 0
    cancle_code = 126
    wrong_password_code = 127

    def __init__(self):
        super().__init__()
        # 初始化拖动相关变量
        self.m_drag = False
        self.m_DragPosition = None
        
        # 初始化按钮区域矩形（稍后会被更新）
        self.hide_button_rect = QRect()
        self.close_button_rect = QRect()
        
        self.init_rpmdata()
        self.initUI()

    def calculate_adaptive_window_size(self):
        """根据桌面分辨率计算自适应窗口大小"""
        # 基准分辨率和窗口大小
        base_screen_width = 1023
        base_screen_height = 768
        base_window_width = 640
        base_window_height = 561
        
        # 获取当前桌面可用区域
        desktop = QDesktopWidget()
        screen_geometry = desktop.availableGeometry()
        current_screen_width = screen_geometry.width()
        current_screen_height = screen_geometry.height()
        
        # 计算基准比例
        base_width_ratio = base_window_width / base_screen_width   # ≈ 0.626 (62.6%)
        base_height_ratio = base_window_height / base_screen_height # ≈ 0.730 (73.0%)
        
        # 计算当前分辨率下的理论窗口大小
        theoretical_width = int(current_screen_width * base_width_ratio)
        theoretical_height = int(current_screen_height * base_height_ratio)
        
        # 设置最大比例限制（不超过基准比例）
        max_width_ratio = base_width_ratio
        max_height_ratio = base_height_ratio
        
        # 计算实际窗口大小，确保不超过最大比例
        actual_width = min(theoretical_width, int(current_screen_width * max_width_ratio))
        actual_height = min(theoretical_height, int(current_screen_height * max_height_ratio))
        
        # 确保不小于基准大小（最小尺寸保护）
        actual_width = max(actual_width, base_window_width)
        actual_height = max(actual_height, base_window_height)
        
        # 确保不超过屏幕的80%（安全边界）
        safe_max_width = int(current_screen_width * 0.8)
        safe_max_height = int(current_screen_height * 0.8)
        actual_width = min(actual_width, safe_max_width)
        actual_height = min(actual_height, safe_max_height)
        
        return actual_width, actual_height

    def init_rpmdata(self):
        self.rpmpkgs = get_available_update_rpmpkgs()

    def initUI(self):
        # 计算自适应窗口大小
        adaptive_width, adaptive_height = self.calculate_adaptive_window_size()
        
        # 无边框设置
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TintedBackground)
        self.setObjectName("pkgs_upgrade")
        
        # 使用自适应计算的窗口大小
        self.resize(adaptive_width, adaptive_height)
        
        # 设置窗口最小尺寸为基准大小，不允许缩放到更小
        self.setMinimumSize(640, 561)
        
        # 移动到屏幕中心（在设置大小后）
        self.center()
        
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.setMouseTracking(False)
        self.setWindowIcon(QIcon(LOGO))
        self.setWindowTitle(_("rpm upgrade window"))
        
        # 添加标题栏区域用于拖动
        self.title_bar = QWidget(self)
        self.title_bar.setGeometry(0, 0, 640, 101)  # 覆盖logo和title区域
        self.title_bar.setObjectName("title_bar")
        
        # 左上角logo设置
        self.logo = QLabel(self)
        self.logo.setGeometry(15, 25, 80, 76)
        self.logo.setObjectName("logo")
        logo_pic = QPixmap(LOGO)
        self.logo.setPixmap(logo_pic.scaled(80, 76, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # title 设置
        self.title = QLabel(self)
        self.title.setGeometry(QRect(113, 26, 396, 25))
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.title.setText(_("There are some updates available"))

        # 描述设置
        self.desc = QLabel(self)
        self.desc.setGeometry(QRect(113, 61, 396, 40))
        self.desc.setTextFormat(Qt.AutoText)
        self.desc.setScaledContents(False)
        self.desc.setWordWrap(True)
        self.desc.setObjectName("desc")
        self.desc.setText(
            _("Software updates correct errors，eliminate security vulnerabilities and provide new features"))

        # 自定义隐藏按钮
        self.hidebutton = QPushButton(self)
        self.hidebutton.setObjectName("hide")
        self.hidebutton.clicked.connect(self.hide)
        self.hidebutton.setToolTip(_("hide"))
        # 确保按钮在顶层
        self.hidebutton.raise_()

        # 自定义关闭按钮
        self.closebutton = QPushButton(self)
        self.closebutton.setObjectName("close")
        self.closebutton.clicked.connect(self.close_event)
        self.closebutton.setToolTip(_("close"))
        # 确保按钮在顶层
        self.closebutton.raise_()
        
        # 设置按钮位置（相对于窗口右上角）
        self.update_window_buttons_position()

        # 全选按钮
        self.select_all = QCheckBox(self)
        self.select_all.setGeometry(QRect(34, 110, 99, 26))
        self.select_all.setObjectName("select_all")
        self.select_all.clicked.connect(self.select_all_action)
        self.select_all.setText(_("Select All"))

        # 安全更新按钮
        self.select_security = QCheckBox(self)
        self.select_security.setGeometry(QRect(150, 110, 141, 26))
        self.select_security.setObjectName("select_security")
        self.select_security.clicked.connect(self.select_security_action)
        self.select_security.setText(_("Select security"))

        # rpm包信息展示
        self.rpm_table_widget = QTableWidget(self)
        self.rpm_table_widget.setObjectName("rpm_table_widget")
        self.rpm_table_widget.viewport().installEventFilter(self)
        self.set_rpm_table_widget_header()
        self.init_rpm_info()

        # 输出口
        self.output_console = QTextBrowser(self)
        self.output_console.setObjectName("output_console")
        self.output_console.setReadOnly(True)

        # 状态栏
        self.rpm_status = QLabel(self)
        font = QFont()
        font.setPointSize(12)
        self.rpm_status.setFont(font)
        self.rpm_status.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.rpm_status.setObjectName("rpm_status")
        self.rpm_status.setText(_("0 updates selected"))

        # 更新按钮
        self.update = QPushButton(self)
        self.update.setObjectName("update")
        self.update.setProperty("name", 'btn')
        self.update.setDisabled(True)
        self.update.clicked.connect(self.update_rpmpkges)
        self.update.setText(_("update"))
        
        # 更新所有控件的位置和大小
        self.update_widget_layout()

        # 安装rpm进程
        self.process = QProcess(self)
        self.process.readyRead.connect(self.output_display)
        self.process.finished.connect(self.stop_install)

        # 托盘区设置
        self.repo_tray()
        self.setStyleSheet(qss_style)
        QMetaObject.connectSlotsByName(self)
        
        # 延迟更新表格列比例（确保窗口已正确显示）
        QTimer.singleShot(100, self.update_table_columns_proportion)

    def output_display(self):
        cursor = self.output_console.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str(self.process.readAll().data().decode()))
        self.output_console.ensureCursorVisible()

    def disable_install_pkgs_ck(self):
        install_pkgs_id = []
        for i in range(self.rpm_table_widget.rowCount()):
            if self.rpmpkgs_select_status[i][0].isChecked():
                self.rpmpkgs_select_status[i][0].setDisabled(True)
                install_pkgs_id.append(self.rpmpkgs_select_status[i][3])
        # pkgs内部移除已安装的软件包
        install_pkgs = [self.rpmpkgs[i] for i in install_pkgs_id]
        for pkg in install_pkgs:
            self.rpmpkgs.remove(pkg)

    def stop_install(self):
        self.rpm_table_widget.setEnabled(True)
        if self.process.exitCode() == self.sucess_code:
            self.disable_install_pkgs_ck()
            self.rpm_status.setText(_("Upgrade successed"))
        elif self.process.exitCode() == self.cancle_code:
            self.rpm_status.setText(_("Cancel upgrade"))
            # 更新失败，打开按钮
            self.update.setEnabled(True)
        elif self.process.exitCode() == self.wrong_password_code:
            self.rpm_status.setText(_("Wrong privilege escalation password"))
            # 更新失败，打开按钮
            self.update.setEnabled(True)
        # TODO: 增加更多异常
        else:
            self.rpm_status.setText(_("Upgrade failed"))
            # 更新完，升级按钮保持disable
            self.update.setEnabled(True)
        # TODO: 是否需要刷新cli的msg.txt

    def close_event(self):
        if self.process.state() == 0:
            QApplication.instance().quit()
        else:
            QMessageBox.about(self, "Warning",
                              _("During the upgrade process, it is forbidden to exit the program"))

    def set_rpm_table_widget_header(self):
        # 取消选中单元格的特效
        self.rpm_table_widget.setFocusPolicy(Qt.NoFocus)
        # 将表格变为禁止编辑
        self.rpm_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 设置表格为整行选择
        self.rpm_table_widget.setSelectionMode((QAbstractItemView.SingleSelection))
        self.rpm_table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 设置交替色
        self.rpm_table_widget.setAlternatingRowColors(True)

        # 不显示表格单元格的分割线
        self.rpm_table_widget.setShowGrid(False)
        # 不显示垂直表头
        self.rpm_table_widget.verticalHeader().setVisible(False)
        # 设置行高36
        self.rpm_table_widget.verticalHeader().setDefaultSectionSize(36)
        # 设置表格高度
        self.rpm_table_widget.horizontalHeader().setFixedHeight(36)
        # 设置表头显示方式
        self.rpm_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # 设置列数
        self.rpm_table_widget.setColumnCount(5)
        
        # 设置表头标签
        self.rpm_table_widget.setHorizontalHeaderLabels(
            [_("Install"), _("Software"), _("Version"), _("Type"), _("Size")])
        
        # 设置表头，不因点击而变化
        self.rpm_table_widget.horizontalHeader().setHighlightSections(False)

        # 初始化列宽将在update_widget_layout中设置
        # 这里不再设置固定宽度，改为在update_table_columns_proportion中按比例设置

    @staticmethod
    def convert_type_to_i18n_str(type_list):
        if not len(type_list):
            return _("common")
        else:
            type_i18n_list = []
            for ptype in type_list:
                type_i18n_list.append(RpmType.i18n_type_dict.get(ptype))
            return ','.join(type_i18n_list)

    def init_rpm_info(self, type=None):
        # 定义所有widget的状态记录列表，单独定义此列表是为了方便解析操作
        self.rpmpkgs_select_status = []
        self.clean_rpm_info()
        for pkg_id in range(len(self.rpmpkgs)):
            pkginfo = self.rpmpkgs[pkg_id]
            pkginfo_type = pkginfo["type"]
            pkginfo_type_i18n = self.convert_type_to_i18n_str(pkginfo_type)
            if type is None:
                ck = self.add_rpm_item("{name}({arch})".format(name=pkginfo["name"], arch=pkginfo["arch"]),
                                       "{version}-{release}".format(version=pkginfo["version"],
                                                                    release=pkginfo["release"]),
                                       pkginfo_type_i18n, pkginfo["downloadsize_human_readable"])
                self.rpmpkgs_select_status.append([ck, pkginfo["name"], pkginfo["type"], pkg_id])
            else:
                if type in pkginfo_type:
                    ck = self.add_rpm_item("{name}({arch})".format(name=pkginfo["name"], arch=pkginfo["arch"]),
                                           "{version}-{release}".format(version=pkginfo["version"],
                                                                        release=pkginfo["release"]),
                                           pkginfo_type_i18n, pkginfo["downloadsize_human_readable"])
                    self.rpmpkgs_select_status.append([ck, pkginfo["name"], pkginfo["type"], pkg_id])

    def clean_rpm_info(self):
        self.rpm_table_widget.clearContents()
        self.rpm_table_widget.setRowCount(0)

    def select_all_action(self, event):
        if event:
            # 设置安全更新为否
            self.select_security.setCheckState(Qt.Unchecked)
            self.init_rpm_info()

            # 将所有checkbox设置为是
            for i in self.rpmpkgs_select_status:
                # 只修改可编辑按钮的状态
                if i[0].isEnabled():
                    i[0].setCheckState(Qt.Checked)
        else:
            # 将所有的checkbox 设置否
            for i in self.rpmpkgs_select_status:
                # 只修改可编辑按钮的状态
                if i[0].isEnabled():
                    i[0].setCheckState(Qt.Unchecked)

    def select_security_action(self, event):
        if event:
            # 设置选择全部为否
            self.select_all.setCheckState(Qt.Unchecked)
            # 重新渲染tablewidgets
            self.init_rpm_info(RpmType.sec)
            # 将所有checkbox设置为是
            for i in self.rpmpkgs_select_status:
                # 只修改可编辑按钮的状态
                if i[0].isEnabled():
                    if RpmType.sec in i[2]:
                        i[0].setCheckState(Qt.Checked)
                    else:
                        i[0].setCheckState(Qt.Unchecked)

        else:
            # 将所有的checkbox 设置否
            for i in self.rpmpkgs_select_status:
                # 只修改可编辑按钮的状态
                if i[0].isEnabled():
                    i[0].setCheckState(Qt.Unchecked)

    def add_rpm_item(self, name, version, rpmpkgtype, size):
        row = self.rpm_table_widget.rowCount()
        self.rpm_table_widget.setRowCount(row + 1)
        ck = QCheckBox()
        ck.toggled.connect(self.update_rpm_status)
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(ck)
        w = QWidget()
        w.setLayout(h)
        self.rpm_table_widget.setCellWidget(row, 0, w)
        self.rpm_table_widget.setItem(row, 1, QTableWidgetItem(name))
        self.rpm_table_widget.setItem(row, 2, QTableWidgetItem(version))
        self.rpm_table_widget.setItem(row, 3, QTableWidgetItem(rpmpkgtype))
        self.rpm_table_widget.setItem(row, 4, QTableWidgetItem(size))
        return ck

    def update_rpmpkges(self):
        logging.info("Begin install rpmpkgs")
        self.update.setDisabled(True)
        self.rpm_table_widget.setDisabled(True)
        self.rpm_status.setText(_("Start upgrade..."))
        select_rpm_list = []
        for i in range(self.rpm_table_widget.rowCount()):
            if self.rpmpkgs_select_status[i][0].isChecked():
                select_rpm_list.append(self.rpmpkgs_select_status[i][1])
                # self.rpmpkgs_select_status[i][0].setDisabled(True)
        self.output_console.clear()
        self.process.start("pkexec", ["pkgs_install_tool", "-l", " ".join(select_rpm_list)])

    def eventFilter(self, source, event):
        if self.rpm_table_widget.selectedIndexes() != []:
            if event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
                    row = self.rpm_table_widget.currentRow()
                    self.show_rpm_info(row)
        return QObject.event(source, event)

    def show_rpm_info(self, row):
        def format_changelog(changelog):
            """Return changelog formatted as in spec file"""
            chlog_str = '* %s %s\n%s\n' % (
                datetime.datetime.strptime(changelog['timestamp'], '%Y-%m-%d').strftime("%a %b %d %Y"),
                changelog['author'],
                changelog['text'])
            return chlog_str

        def get_rpm_info(rpmpkg):
            output_list = []
            name = "{0:<12}: {1}".format("Name", rpmpkg["name"])
            output_list.append(name)
            version = "{0:<12}: {1}".format("Version", rpmpkg["version"])
            output_list.append(version)
            release = "{0:<12}: {1}".format("Release", rpmpkg["release"])
            output_list.append(release)
            arch = "{0:<12}: {1}".format("Arch", rpmpkg["arch"])
            output_list.append(arch)
            size = "{0:<12}: {1}".format("Size", rpmpkg["downloadsize_human_readable"])
            output_list.append(size)
            srpm = "{0:<12}: {1}".format("Srpm", rpmpkg["srpm"])
            output_list.append(srpm)
            repo = "{0:<12}: {1}".format("Repository", rpmpkg["repo"])
            output_list.append(repo)
            summary = "{0:<12}: {1}".format("Summary", rpmpkg["summary"])
            output_list.append(summary)
            url = "{0:<12}: {1}".format("URL", rpmpkg["url"])
            output_list.append(url)
            license = "{0:<12}: {1}".format("License", rpmpkg["license"])
            output_list.append(license)
            desc = "{0:<12}: {1}".format("Description", rpmpkg["desc"])
            output_list.append(desc)
            chlog = "{0:<12}:".format("Changelogs")
            output_list.append(chlog)
            for ch in rpmpkg["last_changelogs"]:
                output_list.append(format_changelog(ch))
            return "\n".join(output_list)

        self.output_console.clear()
        try:
            # 增加安全筛选后，需要准确匹配到具体包
            rpminfo = get_rpm_info(self.rpmpkgs[self.rpmpkgs_select_status[row][3]])

        except Exception as e:
            print(e)
        self.output_console.clear()
        self.output_console.append(rpminfo)

    def update_rpm_status(self):
        select_count = 0
        available_select_count = 0
        for i in range(self.rpm_table_widget.rowCount()):
            if self.rpmpkgs_select_status[i][0].isChecked():
                select_count += 1
                if self.rpmpkgs_select_status[i][0].isEnabled():
                    available_select_count += 1
        if available_select_count == 0:
            self.update.setDisabled(True)
        else:
            self.update.setEnabled(True)
        self.rpm_status.setText(
            gettext.ngettext("{0} update selected", "{0} updates selected", select_count).format(str(select_count)))

    # 清空rpm信息展示列表
    def cancle_process(self):
        self.process.kill()
        # self.rpm_table_widget.clearContents()
        # self.rpm_table_widget.setRowCount(0)

    def repo_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            QIcon(LOGO))

        '''
            Define and add steps to work with the system tray icon
            show - show window
            hide - hide window
            exit - exit from application
        '''
        show_action = QAction(_("Show"), self)
        quit_action = QAction(_("Exit"), self)
        hide_action = QAction(_("Hide"), self)
        reload_action = QAction(_("Reload"), self)
        show_action.triggered.connect(self.hide)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close_event)
        reload_action.triggered.connect(self.reload)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        # tray_menu.addAction(reload_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip(gettext.ngettext("There is {} update available", "There are {} updates available",
                                                   len(self.rpmpkgs)).format(str(len(self.rpmpkgs))))
        self.tray_icon.activated.connect(self.show)
        self.tray_icon.show()
        self.tray_timer()

    def reload(self):
        try:
            pass
        except Exception as e:
            print(e)
        self.update_tray()

    def tray_timer(self, interval=TRAY_INTERVAL):
        timer = QTimer(self)

        timer.timeout.connect(self.update_tray)
        timer.start(interval)

    def update_tray(self):
        if self.isHidden():
            self.init_rpmdata()
            self.tray_icon.setToolTip(gettext.ngettext("There is {} update available", "There are {} updates available",
                                                       len(self.rpmpkgs)).format(str(len(self.rpmpkgs))))
            self.init_rpm_info()

    # 移动到屏幕中心
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_window_buttons_position(self):
        """更新窗口控制按钮位置（相对于窗口右上角）"""
        button_size = 50  # 按钮大小
        button_margin = 0  # 按钮与窗口边缘的间距
        
        # 隐藏按钮位置（右上角第二个按钮）
        hide_x = self.width() - (button_size * 2) - button_margin
        hide_y = button_margin
        self.hidebutton.setGeometry(QRect(hide_x, hide_y, button_size, button_size))
        
        # 关闭按钮位置（右上角第一个按钮）
        close_x = self.width() - button_size - button_margin  
        close_y = button_margin
        self.closebutton.setGeometry(QRect(close_x, close_y, button_size, button_size))
        
        # 同时更新拖动区域检测中的按钮位置
        self.update_draggable_area_rects()
        
    def update_draggable_area_rects(self):
        """更新可拖动区域的矩形范围"""
        self.hide_button_rect = QRect(self.width() - 100, 0, 50, 50)
        self.close_button_rect = QRect(self.width() - 50, 0, 50, 50)

    def update_widget_layout(self):
        """更新所有控件的位置和大小，支持动态调整"""
        # 获取当前窗口尺寸
        window_width = self.width()
        window_height = self.height()
        
        # 边距设置
        margin = 10
        
        # === 固定位置的组件（纵向位置不变） ===
        
        # 标题栏区域（保持固定高度）
        self.title_bar.setGeometry(0, 0, window_width, 101)
        
        # 左上角logo（固定位置）
        self.logo.setGeometry(15, 25, 80, 76)
        
        # 标题（固定位置，但可以调整最大宽度以避免与按钮重叠）
        title_max_width = window_width - 113 - 120  # 留出按钮空间
        self.title.setGeometry(QRect(113, 26, min(396, title_max_width), 25))
        
        # 描述（同样调整最大宽度）
        self.desc.setGeometry(QRect(113, 61, min(396, title_max_width), 40))
        
        # 全选按钮（固定位置）
        self.select_all.setGeometry(QRect(34, 110, 99, 26))
        
        # 安全更新按钮（固定位置）
        self.select_security.setGeometry(QRect(150, 110, 141, 26))
        
        # === 动态纵向组件计算 ===
        
        # 固定的组件位置定义
        table_start_y = 140  # 表格开始位置（固定）
        console_end_to_status = 10  # 控制台到状态栏的间距（固定）
        status_height = 20  # 状态栏高度（固定）
        status_to_button = 17  # 状态栏到按钮的间距（固定）
        button_height = 36  # 按钮高度（固定）
        button_to_bottom = 13  # 按钮到窗口底部的间距（固定）
        
        # 计算状态栏和按钮的固定位置（从底部向上计算）
        button_y = window_height - button_to_bottom - button_height
        status_y = button_y - status_to_button - status_height
        console_end_y = status_y - console_end_to_status
        
        # 计算可用于表格和控制台的总高度
        available_height = console_end_y - table_start_y
        
        # 定义表格和控制台的纵向占比（基于原始设计）
        # 原始：table=211, console=103, 总计=314
        # 占比：table=67.2%, console=32.8%
        table_ratio = 211 / (211 + 103)  # 约 67.2%
        console_ratio = 103 / (211 + 103)  # 约 32.8%
        
        # 计算新的高度
        table_height = int(available_height * table_ratio)
        console_height = int(available_height * console_ratio)
        
        # 确保最小高度
        table_height = max(table_height, 150)  # 表格最小高度
        console_height = max(console_height, 80)  # 控制台最小高度
        
        # 计算控制台开始位置
        console_start_y = table_start_y + table_height + 11  # 11是原始间距
        
        # === 应用动态布局 ===
        
        # rpm包信息展示（横向跟随窗口，纵向动态调整）
        table_width = window_width - 2 * margin
        self.rpm_table_widget.setGeometry(QRect(margin, table_start_y, table_width, table_height))
        
        # 输出控制台（横向跟随窗口，纵向动态调整）
        console_width = window_width - 2 * margin
        self.output_console.setGeometry(QRect(margin, console_start_y, console_width, console_height))
        
        # === 底部固定组件 ===
        
        # 状态栏（横向跟随窗口，纵向位置相对底部固定）
        status_width = window_width - 2 * margin - 9  # 额外调整对齐
        self.rpm_status.setGeometry(QRect(19, status_y, status_width, status_height))
        
        # 更新按钮（横向居中，纵向位置相对底部固定）
        button_width = 200
        button_x = (window_width - button_width) // 2
        self.update.setGeometry(QRect(button_x, button_y, button_width, button_height))
        
        # 更新表格列的比例
        self.update_table_columns_proportion()
    
    def update_table_columns_proportion(self):
        """更新表格列的比例，保持当前比例同步缩放"""
        if not hasattr(self.rpm_table_widget, 'horizontalHeader'):
            return
            
        # 获取表格当前宽度
        table_width = self.rpm_table_widget.width()
        
        # 预留滚动条宽度
        scrollbar_width = 20
        available_width = table_width - scrollbar_width
        
        # 定义列的比例（基于原始设计的比例）
        # 原始宽度：Install(60), Software(236), Version(165), Type(80), Size(自适应)
        # 原始总固定宽度: 541px，剩余给Size列: 620-541=79px
        # 计算比例
        total_original_width = 620
        column_proportions = [
            60 / total_original_width,    # Install: ~9.7%
            236 / total_original_width,   # Software: ~38.1% 
            165 / total_original_width,   # Version: ~26.6%
            80 / total_original_width,    # Type: ~12.9%
            79 / total_original_width     # Size: ~12.7%
        ]
        
        # 应用新的列宽
        for i, proportion in enumerate(column_proportions):
            new_width = int(available_width * proportion)
            self.rpm_table_widget.setColumnWidth(i, max(new_width, 30))  # 最小宽度30
        
        # 确保最后一列能够自适应剩余空间
        self.rpm_table_widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

    def resizeEvent(self, event):
        """窗口大小改变时更新按钮位置"""
        super().resizeEvent(event)
        self.update_window_buttons_position()
        self.update_widget_layout()

    def is_in_draggable_area(self, pos):
        """判断鼠标位置是否在可拖动区域内"""
        # 标题栏区域，但排除按钮区域
        title_bar_rect = QRect(0, 0, self.width(), 101)
        
        return (title_bar_rect.contains(pos) and 
                not self.hide_button_rect.contains(pos) and 
                not self.close_button_rect.contains(pos))

    def update_cursor_for_position(self, pos):
        """根据鼠标位置更新光标"""
        if not self.m_drag:
            if self.is_in_draggable_area(pos):
                self.setCursor(QCursor(Qt.OpenHandCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

    # 实现窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_in_draggable_area(event.pos()):
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
        else:
            super().mousePressEvent(event)

    # 实现窗口拖动
    def mouseMoveEvent(self, event):
        if self.m_drag and self.m_DragPosition is not None:
            if event.buttons() == Qt.LeftButton:
                # 限制窗口移动范围，避免移出屏幕
                new_pos = event.globalPos() - self.m_DragPosition
                screen_geometry = QDesktopWidget().availableGeometry()
                
                # 确保窗口不会完全移出屏幕
                new_pos.setX(max(0, min(new_pos.x(), screen_geometry.width() - self.width())))
                new_pos.setY(max(0, min(new_pos.y(), screen_geometry.height() - self.height())))
                
                self.move(new_pos)
                event.accept()
        else:
            # 更新光标状态
            self.update_cursor_for_position(event.pos())
            super().mouseMoveEvent(event)

    # 实现窗口拖动
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = False
            # 根据当前鼠标位置设置合适的光标
            self.update_cursor_for_position(event.pos())
        super().mouseReleaseEvent(event)
        
    def enterEvent(self, event):
        """鼠标进入窗口时的事件"""
        self.update_cursor_for_position(self.mapFromGlobal(QCursor.pos()))
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """鼠标离开窗口时的事件"""
        # 重置拖动状态
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        super().leaveEvent(event)


# 更新设计，暂时不使用自定义表头
class CheckBoxHeader(QHeaderView):
    """自定义表头类"""

    # 自定义 复选框全选信号
    select_all_clicked = pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 23
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2.)

        if logicalIndex == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
                if self.isOn:
                    self.isOn = False
                else:
                    self.isOn = True
                    # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.isOn)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)


def main():
    app = QApplication(sys.argv)
    # 使用fusion，规避dtk bug
    app.setStyle("fusion")
    ex = Ui_pkgs_upgrade()
    # 设置窗口透明度，目前在dde上显示有异常
    ex.setWindowOpacity(0.5)
    ex.show()
    app.exec_()


if __name__ == "__main__":
    main()
