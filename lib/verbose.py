#! /usr/bin/env python
# -*- coding: utf-8 -*-
# © 2016 Antonio Espinosa - <antespi@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

ERROR = 1
INFO = 2
DEBUG = 3
FULL = 4

level = 0


def show(l, msg, indent=0):
    if not enabled(l):
        return
    prefix = ''
    level_str = ''
    if indent > 0:
        prefix = ' ' * (indent * 3)
    if l >= ERROR:
        level_str = 'ERROR : '
    if l >= INFO:
        level_str = 'INFO  : '
    if l >= DEBUG:
        level_str = 'DEBUG : '
    if l >= FULL:
        level_str = 'FULL  : '
    print level_str + prefix + msg


def enabled(l):
    if level < l:
        return False
    return True


def error(msg, indent=0):
    show(ERROR, msg, indent)


def info(msg, indent=0):
    show(INFO, msg, indent)


def debug(msg, indent=0):
    show(DEBUG, msg, indent)


def full(msg, indent=0):
    show(FULL, msg, indent)
