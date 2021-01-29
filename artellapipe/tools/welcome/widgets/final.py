#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains final widget implementation
"""

from __future__ import print_function, division, absolute_import

import logging

from Qt.QtCore import Qt, Signal, QSize
from Qt.QtWidgets import QToolButton

from tpDcc.managers import resources
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, label, buttons

from artellapipe.managers import tools

from artellapipe.tools.welcome.core import consts

logger = logging.getLogger(consts.TOOL_ID)


class FinalWidget(base.BaseWidget, object):

    showChangelog = Signal(object)

    def __init__(self, project, parent=None):
        self._project = project

        super(FinalWidget, self).__init__(parent=parent)

    def get_main_layout(self):
        return layouts.VerticalLayout(spacing=2, margins=(2, 2, 2, 2))

    def ui(self):
        super(FinalWidget, self).ui()

        ready_lbl = label.BaseLabel('You are ready to go!', parent=self)
        ready_lbl.setAlignment(Qt.AlignCenter)
        ready_lbl.setStyleSheet('font-size: 24px; font-family: "Montserrat"; font-weight: bold;')

        more_info_lbl = label.BaseLabel('You can find more info in the following links', parent=self)
        more_info_lbl.setAlignment(Qt.AlignCenter)
        more_info_lbl.setStyleSheet('font-size: 18px; font-family: "Montserrat";')

        icons_layout = layouts.HorizontalLayout(spacing=2, margins=(2, 2, 2, 2))

        doc_icon = resources.icon('manual')
        change_icon = resources.icon('document')

        self._documentation_btn = QToolButton(parent=self)
        self._documentation_btn.setText('Open Documentation')
        self._documentation_btn.setIcon(doc_icon)
        self._documentation_btn.setIconSize(QSize(64, 64))
        self._documentation_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self._changelog_btn = QToolButton(parent=self)
        self._changelog_btn.setText('Show Changelog')
        self._changelog_btn.setIcon(change_icon)
        self._changelog_btn.setIconSize(QSize(64, 64))
        self._changelog_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        icons_layout.addWidget(self._documentation_btn)
        icons_layout.addWidget(self._changelog_btn)

        self.main_layout.addWidget(ready_lbl)
        self.main_layout.addWidget(more_info_lbl)
        self.main_layout.addLayout(icons_layout)

    def setup_signals(self):
        self._documentation_btn.clicked.connect(self._on_open_documentation)
        self._changelog_btn.clicked.connect(self._on_open_changelog)

    def _on_open_documentation(self):
        """
        Internal callback function that is called when Opening Documentation button is pressed
        """

        self._project.open_documentation()

    def _on_open_changelog(self):
        """
        Internal callback function that is called when Show Changelog button is pressed
        """

        try:
            changelog_tool = tools.run_tool('changelog', project_name=self._project)
            self.showChangelog.emit(changelog_tool)
        except ImportError:
            logger.warning('Changelog Tool is not available!')
