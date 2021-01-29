#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains shortcuts widget implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt

from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, label, dividers


class ShortcutsWidget(base.BaseWidget, object):
    def __init__(self, project, parent=None):
        self._project = project

        super(ShortcutsWidget, self).__init__(parent=parent)

    def get_main_layout(self):
        return layouts.VerticalLayout(spacing=2, margins=(2, 2, 2, 2))

    def ui(self):
        super(ShortcutsWidget, self).ui()

        lbl = label.BaseLabel('{} Tools can be accessed through: '.format(self._project.name.title()), parent=self)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet('font-size: 14px; font-family: "Montserrat";')

        shelf_lbl = label.BaseLabel('{} Shelf'.format(self._project.name.title()), parent=self)
        shelf_lbl.setAlignment(Qt.AlignCenter)
        shelf_lbl.setStyleSheet('font-size: 18px; font-family: "Montserrat"; font-weight: bold')

        self.main_layout.addWidget(lbl)
        self.main_layout.addLayout(dividers.DividerLayout())
        self.main_layout.addWidget(shelf_lbl)
