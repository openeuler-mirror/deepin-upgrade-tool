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
QPushButton#close
{
    border-style:none;
    background-image: url(%s/window_close_normal_light.png);
    background-position:center;
    background-repeat:no-repeat;
}

QPushButton#close::hover
{
	background-color: #E6E6E6;

}

QPushButton#hide
{
    border-style:none;
    background-image: url(%s/window_min_normal_light.png);
    background-position:center;
    background-repeat:no-repeat;
}

QPushButton#hide::hover
{
	background-color: #E6E6E6;

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
}

QPushButton#update::hover
{
	background-color: #0081FF;
}

QPushButton#update::pressed
{
	background-color: #0000FF;

}

QPushButton#update::disabled
{
	background-color: #C0C0C0;

}

QPushButton[name~='select_btn']
{
    border-style:none;
}

QPushButton[name~='select_btn']::hover
{
	background-color: #E6E6E6;

}


QTextBrowser
{
    background: rgba(255,255,255,0.50);
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 8px;
    font-size: 12px;
    font-family: Droid Sans Mono;
}

QTableWidget
{
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 8px;
    alternate-background-color: rgb(244,244,244);text-align:right;
}

QHeaderView::section
{
    border-width:6;
}
''' % (PIXMAPS_PATH, PIXMAPS_PATH)
