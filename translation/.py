#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
tmp_dir = '翻譯語料/tmp'
files = os.listdir(tmp_dir)
華_files = [f for f in files if f.endswith('華')]
閩_files = [f for f in files if f.endswith('閩')]

