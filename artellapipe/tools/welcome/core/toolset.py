#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains artellapipe-tools-welcome toolset implementation
"""

from __future__ import print_function, division, absolute_import


from artellapipe.core import tool
from artellapipe.widgets import dialog


class WelcomeToolset(tool.ArtellaToolset, object):

    ATTACHER_CLASS = dialog.ArtellaDialog

    def __init__(self, *args, **kwargs):
        super(WelcomeToolset, self).__init__(*args, **kwargs)

        self._title_frame.setVisible(False)

    def set_attacher(self, attacher):
        super(WelcomeToolset, self).set_attacher(attacher)

        # attacher.logo_view.setVisible(False)

        attacher.statusBar().hide()
        attacher._dragger.hide()
        attacher.logo_view.hide()
        attacher.resize(650, 300)
        self._welcome_view._close_btn.clicked.connect(attacher.fade_close)

    def contents(self):

        from artellapipe.tools.welcome.core import view

        self._welcome_view = view.WelcomeView(project=self._project, parent=self)
        return [self._welcome_view]
