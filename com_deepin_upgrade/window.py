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
        self.init_rpmdata()
        self.initUI()

    def init_rpmdata(self):
        self.rpmpkgs = get_available_update_rpmpkgs()

    def initUI(self):
        # 移动到屏幕中心
        self.center()
        # 无边框设置
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TintedBackground)
        self.setObjectName("pkgs_upgrade")
        self.resize(640, 561)
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.setMouseTracking(False)
        self.setWindowIcon(QIcon(LOGO))
        self.setWindowTitle(_("rpm upgrade window"))
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
        self.hidebutton.setGeometry(QRect(542, 0, 50, 50))
        self.hidebutton.setObjectName("hide")
        self.hidebutton.clicked.connect(self.hide)
        self.hidebutton.setToolTip(_("hide"))

        # 自定义关闭按钮
        self.closebutton = QPushButton(self)
        self.closebutton.setGeometry(QRect(592, 0, 50, 50))
        self.closebutton.setObjectName("close")
        self.closebutton.clicked.connect(self.close_event)
        self.closebutton.setToolTip(_("close"))

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
        # self.rpm_table_widget.setGeometry(QRect(10, 125, 620, 226))
        self.rpm_table_widget.setGeometry(QRect(10, 140, 620, 211))
        self.rpm_table_widget.setObjectName("rpm_table_widget")
        self.rpm_table_widget.viewport().installEventFilter(self)
        self.set_rpm_table_widget_header()
        self.init_rpm_info()

        # 输出口
        self.output_console = QTextBrowser(self)
        self.output_console.setGeometry(QRect(10, 362, 620, 103))
        self.output_console.setObjectName("output_console")
        self.output_console.setReadOnly(True)

        # 状态栏
        self.rpm_status = QLabel(self)
        self.rpm_status.setGeometry(QRect(19, 475, 601, 20))
        font = QFont()
        font.setPointSize(12)
        self.rpm_status.setFont(font)
        self.rpm_status.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.rpm_status.setObjectName("rpm_status")
        self.rpm_status.setText(_("0 updates selected"))

        # 更新按钮
        self.update = QPushButton(self)
        self.update.setGeometry(QRect(220, 512, 200, 36))
        self.update.setObjectName("update")
        self.update.setProperty("name", 'btn')
        self.update.setDisabled(True)
        self.update.clicked.connect(self.update_rpmpkges)
        self.update.setText(_("update"))

        # 安装rpm进程
        self.process = QProcess(self)
        self.process.readyRead.connect(self.output_display)
        self.process.finished.connect(self.stop_install)

        # 托盘区设置
        self.repo_tray()
        self.setStyleSheet(qss_style)
        QMetaObject.connectSlotsByName(self)

    def output_display(self):
        cursor = self.output_console.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str(self.process.readAll().data().decode()))
        self.output_console.ensureCursorVisible()

    def disable_install_pkgs_ck(self):
        for i in range(self.rpm_table_widget.rowCount()):
            if self.rpmpkgs_select_status[i][0].isChecked():
                self.rpmpkgs_select_status[i][0].setDisabled(True)

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
        # 四列数据
        self.rpm_table_widget.setColumnCount(5)
        # 设置头
        # header_checkbox = CheckBoxHeader()
        # self.rpm_table_widget.setHorizontalHeader(header_checkbox)
        self.rpm_table_widget.setHorizontalHeaderLabels(
            [_("Install"), _("Software"), _("Version"), _("Type"), _("Size")])
        # 设置表头显示方式
        self.rpm_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # header_checkbox.select_all_clicked.connect(self.select_all_action)

        # 前三列固定宽度
        self.rpm_table_widget.setColumnWidth(0, 60)
        self.rpm_table_widget.setColumnWidth(1, 236)
        self.rpm_table_widget.setColumnWidth(2, 165)
        self.rpm_table_widget.setColumnWidth(3, 80)
        # 最后一列自适应宽度
        self.rpm_table_widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

    @staticmethod
    def convert_type_to_i18n_str(type_list):
        if not len(type_list):
            return _("common")
        else:
            type_i18n_list = []
            for ptype in type_list:
                type_i18n_list.append(RpmType.i18n_type_dict.get(ptype))
            return ','.join(type_i18n_list)

    def init_rpm_info(self):

        self.rpmpkgs_select_status = []
        self.clean_rpm_info()
        for pkginfo in self.rpmpkgs:
            rpmpkg_type = self.convert_type_to_i18n_str(pkginfo["type"])
            ck = self.add_rpm_item("{name}({arch})".format(name=pkginfo["name"], arch=pkginfo["arch"]),
                                   "{version}-{release}".format(version=pkginfo["version"], release=pkginfo["release"]),
                                   rpmpkg_type, pkginfo["downloadsize_human_readable"])
            self.rpmpkgs_select_status.append([ck, pkginfo["name"], pkginfo["type"]])

    def clean_rpm_info(self):
        self.rpm_table_widget.clearContents()
        self.rpm_table_widget.setRowCount(0)

    def select_all_action(self, event):
        if event:
            # 设置安全更新为否
            self.select_security.setCheckState(Qt.Unchecked)
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
            rpminfo = get_rpm_info(self.rpmpkgs[row])
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

    # 实现窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    # 实现窗口拖动
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    # 实现窗口拖动
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


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
