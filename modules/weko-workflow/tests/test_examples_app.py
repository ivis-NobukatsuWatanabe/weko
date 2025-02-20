# -*- coding: utf-8 -*-
#
# This file is part of WEKO3.
# Copyright (C) 2017 National Institute of Informatics.
#
# WEKO3 is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# WEKO3 is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WEKO3; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.

"""Test example app."""

import os
import signal
import subprocess
import time
from os.path import abspath, dirname, join

import pytest


# @pytest.yield_fixture
# def example_app():
#     """Example app fixture."""
#     current_dir = os.getcwd()
# 
#     # Go to example directory
#     project_dir = dirname(dirname(abspath(__file__)))
#     exampleapp_dir = join(project_dir, 'examples')
#     os.chdir(exampleapp_dir)
# 
#     # Setup application
#     assert subprocess.call('./app-setup.sh', shell=True) == 0
# 
#     # Setup fixtures
#     assert subprocess.call('./app-fixtures.sh', shell=True) == 0
# 
#     # Start example app
#     webapp = subprocess.Popen(
#         'FLASK_APP=app.py flask run --debugger -p 5000',
#         stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)
#     time.sleep(10)
#     yield webapp
# 
#     # Stop server
#     os.killpg(webapp.pid, signal.SIGTERM)
# 
#     # Tear down example app
#     subprocess.call('./app-teardown.sh', shell=True)
# 
#     # Return to the original directory
#     os.chdir(current_dir)
