#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains artellapipe-tools-welcome view implementation
"""

from __future__ import print_function, division, absolute_import

import os
import random
from functools import partial

from Qt.QtCore import Qt, QSize, QTimer, QByteArray, QBuffer
from Qt.QtWidgets import QSizePolicy, QLabel, QFrame, QGraphicsOpacityEffect, QRadioButton
from Qt.QtGui import QMovie

from tpDcc.managers import resources
from tpDcc.libs.qt.core import base, qtutils, animation
from tpDcc.libs.qt.widgets import layouts, buttons, stack

from artellapipe.tools.welcome.widgets import widget, frame, shortcuts, final


class WelcomeView(base.BaseWidget):
    def __init__(self, project, parent=None):

        self._radio_buttons = list()
        self._offset = 0
        self._project = project
        self._toolset = parent
        self._logo_gif_file = None
        self._logo_gif_byte_array = None
        self._logo_gif_buffer = None
        self._logo_movie = None

        super(WelcomeView, self).__init__(parent=parent)

        self._init()

    def ui(self):
        super(WelcomeView, self).ui()

        self.resize(685, 290)

        self.setAttribute(Qt.WA_TranslucentBackground)
        if qtutils.is_pyside2():
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        main_frame = frame.WelcomeFrame(pixmap=self._get_welcome_pixmap())
        frame_layout = layouts.VerticalLayout(spacing=2, margins=(10, 0, 10, 0))
        main_frame.setLayout(frame_layout)

        top_layout = layouts.HorizontalLayout(spacing=2, margins=(2, 2, 2, 2))
        frame_layout.addLayout(top_layout)

        self._close_btn = buttons.BaseButton('', parent=self)
        self._close_btn.setIcon(resources.icon('close', theme='window'))
        self._close_btn.setStyleSheet('QWidget {background-color: rgba(255, 255, 255, 0); border:0px;}')
        self._close_btn.setIconSize(QSize(25, 25))

        top_layout.addStretch()
        self._logo = QLabel('', parent=self)
        top_layout.addWidget(self._logo)
        top_layout.addStretch()
        top_layout.addWidget(self._close_btn)

        base_frame = QFrame()
        base_frame.setObjectName('baseFrame')
        base_frame.setFrameShape(QFrame.NoFrame)
        base_frame.setFrameShadow(QFrame.Plain)
        # base_frame.setAttribute(Qt.WA_TranslucentBackground)
        base_frame.setStyleSheet('QFrame#baseFrame { background-color: rgba(100, 100, 100, 80); }')
        base_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        base_layout = layouts.VerticalLayout(spacing=2, margins=(2, 2, 2, 2))
        base_frame.setLayout(base_layout)
        frame_layout.addWidget(base_frame)

        self._stack = stack.SlidingOpacityStackedWidget(parent=self)
        self._stack.setAutoFillBackground(False)
        self._stack.setAttribute(Qt.WA_TranslucentBackground)
        base_layout.addWidget(self._stack)

        bottom_layout = layouts.HorizontalLayout(spacing=2, margins=(2, 2, 2, 2))
        frame_layout.addLayout(bottom_layout)

        self._left_btn = buttons.BaseButton('Skip', parent=self)
        self._left_btn.setMinimumSize(QSize(100, 30))
        self._left_btn.setStyleSheet(
            """
            QPushButton\n{\n\nbackground-color: rgb(250,250,250,30);\ncolor: rgb(250, 250, 250);
            \nborder-radius: 5px;\nborder: 0px;\npadding-left: 15px;\npadding-right: 15px;\n}\n\nQPushButton:hover\n{\n
            background-color: rgb(250,250,250,20);\n}\n\nQPushButton:pressed\n{\n\nbackground-color: rgb(0,0,0,30);\n}
            """
        )
        self._right_btn = buttons.BaseButton('Next', parent=self)
        self._right_btn.setMinimumSize(QSize(100, 30))
        self._right_btn.setStyleSheet(
            """
            QPushButton\n{\n\nbackground-color: rgb(250,250,250,30);\ncolor: rgb(250, 250, 250);
            \nborder-radius: 5px;\nborder: 0px;\npadding-left: 15px;\npadding-right: 15px;\n}\n\nQPushButton:hover\n{\n
            background-color: rgb(250,250,250,20);\n}\n\nQPushButton:pressed\n{\n\nbackground-color: rgb(0,0,0,30);\n}
            """
        )

        self.setStyleSheet(
            "QRadioButton::indicator {\nbackground-color: rgb(250,250,250,120);\n}\n"
            "QRadioButton::indicator::unchecked {\nbackground-color: rgb(255,255,255,70);\nborder-radius: 4px;\n"
            "width: 8px;\n	height: 8px;\n}\nQRadioButton::indicator::checked {"
            "\nbackground: qlineargradient(x1: 0, y1: 1, x2: 1, y2: 1, stop: 0 rgba(" + self._project.dev_color0 + "), "
            "stop: 1 rgba(" + self._project.dev_color1 + "));\n	border-radius: 5px;\n	width: 10px;\n	height: 10px;\n}")

        self._radio_layout = layouts.HorizontalLayout(spacing=2, margins=(2, 2, 2, 2))

        bottom_layout.addStretch()
        bottom_layout.addWidget(self._left_btn)
        bottom_layout.addStretch()
        bottom_layout.addLayout(self._radio_layout)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self._right_btn)
        bottom_layout.addStretch()

        self.main_layout.addWidget(main_frame)

    def setup_signals(self):
        self._right_btn.clicked.connect(lambda: self._on_button_clicked(+1))
        self._left_btn.clicked.connect(lambda: self._on_button_clicked(-1))

    def mousePressEvent(self, event):
        """
        Overrides base ArtellaDialog mousePressEvent function
        :param event: QMouseEvent
        """

        self._offset = event.pos()

    def mouseMoveEvent(self, event):
        """
        Overrides base ArtellaDialog mouseMoveEvent function
        :param event: QMouseEvent
        """

        x = event.globalX()
        y = event.globalY()
        x_w = self._offset.x()
        y_w = self._offset.y()
        self._toolset.attacher.move(x - x_w, y - y_w)

    def _init(self):
        """
        Initializes Welcome dialog
        """

        self._tab_opacity_effect = QGraphicsOpacityEffect(self)
        self._tab_opacity_effect.setOpacity(0)
        self._stack.setGraphicsEffect(self._tab_opacity_effect)

        self._setup_logo()
        self._setup_pages()

        self._set_index(0)

    def _setup_logo(self):
        """
        Internal function that setup project logo
        """

        logo_gif = resources.get('images', '{}_logo.gif'.format(self._project.name.lower()))
        if not logo_gif or not os.path.isfile(logo_gif):
            return
        self._logo_gif_file = open(logo_gif, 'rb').read()
        self._logo_gif_byte_array = QByteArray(self._logo_gif_file)
        self._logo_gif_buffer = QBuffer(self._logo_gif_byte_array)
        self._logo_movie = QMovie()
        self._logo_movie.setDevice(self._logo_gif_buffer)
        self._logo_movie.setCacheMode(QMovie.CacheAll)
        self._logo_movie.setScaledSize(QSize(60, 60))
        self._logo_movie.setSpeed(100)
        self._logo_movie.jumpToFrame(0)
        self._logo_movie.start()
        self._logo.setAttribute(Qt.WA_NoSystemBackground)
        self._logo.setMovie(self._logo_movie)

    def _setup_pages(self):
        """
        Internal callback function that set the pages of the stack
        Overrides to add new pages
        """

        self._welcome_widget = widget.WelcomeWidget(project=self._project, parent=self)
        self._shortcuts_widget = shortcuts.ShortcutsWidget(project=self._project, parent=self)
        self._final_widget = final.FinalWidget(project=self._project, parent=self)

        self._final_widget.showChangelog.connect(self._on_show_changelog)

        self._add_page(self._welcome_widget)
        self._add_page(self._shortcuts_widget)
        self._add_page(self._final_widget)

    def _get_welcome_pixmap(self):
        """
        Returns pixmap to be used as splash background
        :return: Pixmap
        """

        welcome_path = resources.get('images', 'welcome.png', key='project')
        if not os.path.isfile(welcome_path):
            welcome_Dir = os.path.dirname(welcome_path)
            welcome_files = [
                f for f in os.listdir(welcome_Dir) if f.startswith('welcome') and os.path.isfile(
                    os.path.join(welcome_Dir, f))]
            if welcome_files:
                welcome_index = random.randint(0, len(welcome_files) - 1)
                welcome_name, splash_extension = os.path.splitext(welcome_files[welcome_index])
                welcome_pixmap = resources.pixmap(
                    welcome_name, extension=splash_extension[1:], key='project')
            else:
                welcome_pixmap = resources.pixmap('welcome')
        else:
            welcome_pixmap = resources.pixmap('welcome', key='project')

        return welcome_pixmap.scaled(QSize(800, 270))

    def _add_page(self, widget):
        """
        Adds a new widget into the stack
        :param widget: QWidget
        """

        total_pages = len(self._radio_buttons)
        new_radio = QRadioButton(parent=self)
        if total_pages == 0:
            new_radio.setChecked(True)
        new_radio.clicked.connect(partial(self._set_index, total_pages))

        self._stack.addWidget(widget)
        self._radio_layout.addWidget(new_radio)
        self._radio_buttons.append(new_radio)

    def _increment_index(self, input):
        """
        Internal function that increases index of the stack widget
        :param input: int
        """

        current = self._stack.currentIndex()
        self._set_index(current + input)

    def _set_index(self, index):
        """
        Internal function that updates stack index and UI
        :param index: int
        """

        animation.fade_animation(start='current', end=0, duration=400, object=self._tab_opacity_effect)

        if index <= 0:
            index = 0
        if index >= self._stack.count() - 1:
            index = self._stack.count() - 1

        self._radio_buttons[index].setChecked(True)

        self.props_timer = QTimer(singleShot=True)
        self.props_timer.timeout.connect(self._on_fade_up_tab)
        self.props_timer.timeout.connect(lambda: self._stack.setCurrentIndex(index))
        self.props_timer.start(450)

        prev_text = 'Previous'
        next_text = 'Next'
        skip_text = 'Skip'
        close_text = 'Finish'

        if index == 0:
            self._left_btn.setText(skip_text)
            self._right_btn.setText(next_text)
        elif index < self._stack.count() - 1:
            self._left_btn.setText(prev_text)
            self._right_btn.setText(next_text)
        elif index == self._stack.count() - 1:
            self._left_btn.setText(prev_text)
            self._right_btn.setText(close_text)

    def _launch_project(self):
        """
        Internal function that closes Welcome dialog and launches project tools
        """

        self._toolset.attacher.fade_close()

    def _on_fade_up_tab(self):
        """
        Internal callback function that is called when stack index changes
        """

        animation.fade_animation(start='current', end=1, duration=400, object=self._tab_opacity_effect)

    def _on_button_clicked(self, input):
        """
        Internal callback function that is called when Next and and Skip buttons are pressed
        :param input: int
        """

        current = self._stack.currentIndex()
        action = 'flip'
        if current == 0:
            if input == -1:
                action = 'close'
        elif current == self._stack.count() - 1:
            if input == 1:
                action = 'close'
        if action == 'flip':
            self._increment_index(input)
        elif action == 'close':
            self._launch_project()

    def _on_show_changelog(self, changelog_window):
        """
        Internal callback function that is called when show changelog button is pressed in the final widget
        """

        self.close_tool_attacher()
        # changelog_window.show()
