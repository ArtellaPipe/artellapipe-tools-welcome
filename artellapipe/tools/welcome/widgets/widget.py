#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget implementation
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, label


class WelcomeWidget(base.BaseWidget, object):
    def __init__(self, project, parent=None):

        self._project = project

        super(WelcomeWidget, self).__init__(parent=parent)

    def get_main_layout(self):
        return layouts.HorizontalLayout(spacing=2, margins=(2, 2, 2, 2))

    def ui(self):
        super(WelcomeWidget, self).ui()

        self.main_layout.addStretch()
        lbl = label.BaseLabel('Welcome to {}!'.format(self._project.name.title()), parent=self)
        lbl.setStyleSheet('font-size: 35px; font-family: "Montserrat";')
        self.main_layout.addWidget(lbl)
        self.main_layout.addStretch()
