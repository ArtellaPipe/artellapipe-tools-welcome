#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains frame widget implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt
from Qt.QtWidgets import QSizePolicy, QFrame
from Qt.QtGui import QPainter, QPainterPath


class WelcomeFrame(QFrame, object):
    def __init__(self, pixmap, parent=None):
        super(WelcomeFrame, self).__init__(parent)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self._pixmap = pixmap
        self.setStyleSheet('QFrame { border-radius: 10px; }')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        """
        Override base QFrame paintEvent function
        :param event: QPaintEvent
        """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.width(), self.height(), self._pixmap)
