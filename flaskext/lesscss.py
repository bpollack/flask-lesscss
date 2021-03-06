# -*- coding: utf-8 -*-
"""
    flaskext.lesscss
    ~~~~~~~~~~~~~

    A small Flask extension that makes it easy to use LessCSS with your Flask
    application.

    :copyright: (c) 2010 by Steve Losh.
    :license: MIT, see LICENSE for more details.
"""

import os
import subprocess


def lesscss(app):
    @app.before_request
    def _render_less_css():
        if not hasattr(app, 'static_url_path'):
            from warnings import warn
            warn(DeprecationWarning('static_path is called '
                                    'static_url_path since Flask 0.7'),
                 stacklevel=2)

            static_url_path = app.static_path

        else:
            static_url_path = app.static_url_path

        static_dir = app.root_path + static_url_path

        less_paths = []
        for path, subdirs, filenames in os.walk(static_dir):
            less_paths.extend([
                os.path.join(path, f)
                for f in filenames if os.path.splitext(f)[1] == '.less'
            ])

        for less_path in less_paths:
            css_path = os.path.splitext(less_path)[0] + '.css'
            if not os.path.isfile(css_path):
                css_mtime = -1
            else:
                css_mtime = os.path.getmtime(css_path)
            less_mtime = os.path.getmtime(less_path)
            if less_mtime >= css_mtime:
                subprocess.call(['lessc', less_path, css_path], shell=False)
