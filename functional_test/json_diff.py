#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json


with open(sys.argv[1], 'r') as f1:
    with open(sys.argv[2], 'r') as f2:
        if json.load(f1) != json.load(f2):
            sys.exit(1)