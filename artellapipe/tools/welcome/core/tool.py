#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool that allow artists to work with Artella local and server files
"""

from __future__ import print_function, division, absolute_import

import os
import sys

from artellapipe.core import tool

from artellapipe.tools.welcome.core import consts, toolset


class WelcomeTool(tool.ArtellaTool, object):

    ID = consts.TOOL_ID
    TOOLSET_CLASS = toolset.WelcomeToolset

    def __init__(self, *args, **kwargs):
        super(WelcomeTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.ArtellaTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Welcome',
            'id': cls.ID,
            'logo': 'welcome_logo',
            'icon': 'artella',
            'tooltip': 'Tool that shows useful information for the current Artella project',
            'tags': ['artella', 'welcome', 'project'],
            'sentry_id': '',
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Welcome', 'load_on_startup': False, 'color': '', 'background_color': ''},
        }
        base_tool_config.update(tool_config)

        return base_tool_config


if __name__ == '__main__':
    import tpDcc.loader
    import solstice.loader
    from artellapipe.managers import tools

    tool_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    if tool_path not in sys.path:
        sys.path.append(tool_path)

    tpDcc.loader.init(dev=True)
    solstice.loader.init(dev=True)
    tools.run_tool(WelcomeTool.ID, project_name='solstice')
