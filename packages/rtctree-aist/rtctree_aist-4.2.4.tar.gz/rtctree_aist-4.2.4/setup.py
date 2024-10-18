#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-

import setuptools
from setuptools.command.build import build
from setuptools.command.install import install

build.sub_commands.append(('build_idl', None))
install.sub_commands.append(('install_idl', None))

setuptools.setup()

