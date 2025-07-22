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

from com_deepin_upgrade.config import PIXMAPS_PATH

qss_style = '''
/* 标题栏区域样式 */
QWidget#title_bar
{
    background: transparent;
}

/* 主窗口样式 */
QMainWindow#pkgs_upgrade
{
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 8px;
}

QPushButton#close
{
    border-style: none;
    background-image: url(%s/window_close_normal_light.png);
    background-position: center;
    background-repeat: no-repeat;
    border-radius: 6px;
}

QPushButton#close::hover
{
    background-color: #FF5A52;
    background-image: url(%s/window_close_normal_light.png);
}

QPushButton#close::pressed
{
    background-color: #E04B44;
    background-image: url(%s/window_close_normal_light.png);
}

QPushButton#hide
{
    border-style: none;
    background-image: url(%s/window_min_normal_light.png);
    background-position: center;
    background-repeat: no-repeat;
    border-radius: 6px;
}

QPushButton#hide::hover
{
    background-color: #E6E6E6;
    background-image: url(%s/window_min_normal_light.png);
}

QPushButton#hide::pressed
{
    background-color: #CCCCCC;
    background-image: url(%s/window_min_normal_light.png);
}

/* 标题和描述样式 */
QLabel#title
{
    color: #333333;
    background: transparent;
}

QLabel#desc
{
    color: #666666;
    background: transparent;
}

QLabel#logo
{
    background: transparent;
}

QPushButton[name~='btn']
{
    width: 170px;
    height: 36px;
    background: rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.03);
    border-radius: 8px;
    box-shadow: 0px 4px 4px 0px rgba(0,145,255,0.30); 
}

QPushButton#cancle
{
    background-color: #E6E6E6;
}

QPushButton#cancle::hover
{
    background-color: #C0C0C0;
}

QPushButton#update
{
    background-color: #0091FF;
    color: #FFFFFF;
    font-weight: bold;
}

QPushButton#update::hover
{
    background-color: #0081FF;
}

QPushButton#update::pressed
{
    background-color: #0070E0;
}

QPushButton#update::disabled
{
    background-color: #C0C0C0;
    color: #999999;
}

QPushButton[name~='select_btn']
{
    border-style: none;
}

QPushButton[name~='select_btn']::hover
{
    background-color: #E6E6E6;
}

/* 复选框样式 */
QCheckBox
{
    spacing: 8px;
    color: #333333;
}

QCheckBox::indicator
{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid #CCCCCC;
    background-color: #FFFFFF;
}

QCheckBox::indicator:hover
{
    border: 1px solid #0091FF;
}

QCheckBox::indicator:checked
{
    background-color: #0091FF;
    border: 1px solid #0091FF;
    image: url(%s/checkbox_checked_insensitive.png);
}

QCheckBox::indicator:disabled
{
    background-color: #F5F5F5;
    border: 1px solid #DDDDDD;
}

QTextBrowser
{
    background: rgba(255,255,255,0.50);
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 8px;
    font-size: 12px;
    font-family: Droid Sans Mono;
    color: #333333;
    padding: 8px;
}

QTableWidget
{
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 8px;
    alternate-background-color: rgb(248,248,248);
    text-align: left;
    selection-background-color: rgba(0,145,255,0.20);
    gridline-color: rgba(0,0,0,0.05);
}

QHeaderView::section
{
    border: none;
    background-color: #F8F8F8;
    padding: 8px;
    font-weight: bold;
    color: #333333;
    border-bottom: 1px solid rgba(0,0,0,0.10);
}

QHeaderView::section:first
{
    border-top-left-radius: 8px;
}

QHeaderView::section:last
{
    border-top-right-radius: 8px;
}

/* 滚动条样式 */
QScrollBar:vertical
{
    background: #F5F5F5;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical
{
    background: #CCCCCC;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover
{
    background: #AAAAAA;
}

/* 状态标签样式 */
QLabel#rpm_status
{
    color: #666666;
    background: transparent;
}
''' % (PIXMAPS_PATH, PIXMAPS_PATH, PIXMAPS_PATH, PIXMAPS_PATH, PIXMAPS_PATH, PIXMAPS_PATH, PIXMAPS_PATH)
