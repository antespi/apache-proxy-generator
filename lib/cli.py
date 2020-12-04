#! /usr/bin/env python
# -*- coding: utf-8 -*-
# © 2016 Antonio Espinosa - <antespi@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import sys
import textwrap
import traceback
import yaml
import collections
from optparse import OptionParser
try:
    from future.utils import iteritems
except:
    pass

from . import verbose


# http://stackoverflow.com/a/3233356/2868531
def dict_recursive_update(d, u):
    for k, v in iteritems(u):
        if isinstance(v, collections.Mapping):
            r = dict_recursive_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


class CliBase(object):
    program = ''
    version = '1.0'

    optparser = None
    options = None
    config = {}
    config_default = {
        'parent': False,
    }
    args = []

    def __init__(self, program, version):
        self.program = program
        self.version = version
        self.options_parse()
        self.config_parse()

    def banner(self, width=70):
        hline = '=' * width
        sys.stderr.write(hline + "\n")
        p = ("%s v.%s " % (self.program, self.version)).center(width) + "\n"
        sys.stderr.write(p)
        sys.stderr.write(hline + "\n")

    def usage(self, msg=None, width=70, pad=4, errno=0):
        lead_space = ' ' * (pad)
        w = width - pad
        err = ' ERROR '.center(w, '#').center(width)
        errbar = '#' * w
        errbar = errbar.center(width)
        hline = '=' * width
        if msg is not None:
            msg_list = str(msg).splitlines()
            msg = []
            for aline in msg_list:
                aline = lead_space + aline.rstrip()
                msg.append(aline)
            msg = '\n'.join(msg)
            print('\n'.join(('', err, msg, errbar, '')))
            print(hline)
        print("")
        if self.optparser:
            print(self.optparser.format_help())
        sys.exit(errno)

    def usage_get(self):
        # Born to be inherit
        program = os.path.basename(sys.argv[0])
        usg = """\
            usage: %s -h | [-c CONFIG] [-v VERBOSE] [-m MAX] [-s START]
                           [-d] file

        """
        usg = textwrap.dedent(usg) % program
        return usg

    def doopts(self):
        optparser = OptionParser(usage=self.usage_get())
        optparser.add_option('-c', '--config', dest='config',
                             metavar='CONFIG', default=None,
                             help="Config file for connecting to Odoo")
        optparser.add_option('-d', '--dry-run', dest='dry_run',
                             action='store_true', default=False,
                             help="Don't perform any write operation")
        optparser.add_option('-v', '--verbose', dest='verbose',
                             metavar='VERBOSE', default=1, type='int',
                             help='Verbose level: ERROR=1, INFO=2, DEBUG=3')
        optparser.add_option('-m', '--max', dest='max',
                             metavar='MAX', default=0, type='int',
                             help='Max number of items to process')
        optparser.add_option('-s', '--start', dest='start',
                             metavar='START', default=0, type='int',
                             help='Start from this item')
        return optparser

    def options_parse(self):
        self.optparser = self.doopts()
        if self.optparser:
            (self.options, self.args) = self.optparser.parse_args()

    def _config_read(self, filename):
        config = {}
        if os.path.exists(filename):
            f = open(filename)
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
        else:
            msg = ("ERROR : Config file '%s' does not exist." %
                   filename)
            self.usage(msg, errno=1)
        return config

    def _config_parse(self, filename):
        """Parse config recursive"""
        user_config = self._config_read(filename)
        if user_config.get('parent'):
            parent = user_config.get('parent').strip()
            if not os.path.isabs(parent):
                parent = os.path.abspath(
                    os.path.join(os.path.dirname(filename), parent))
            self._config_parse(parent)
        dict_recursive_update(self.config, user_config)

    def config_parse(self):
        self.config = self.config_default.copy()
        if self.options and self.options.config:
            filename = os.path.abspath(self.options.config)
            self._config_parse(filename)

    def run(self, obj, verbose_level=verbose.INFO):
        verbose.level = verbose_level
        if self.options and hasattr(self.options, 'verbose'):
            verbose.level = self.options.verbose
        if not (hasattr(obj, 'run') and
                hasattr(getattr(obj, 'run'), '__call__')):
            self.usage("Object has no 'run' method", errno=5)
        cleanup = False
        if (hasattr(obj, 'cleanup') and
                hasattr(getattr(obj, 'cleanup'), '__call__')):
            cleanup = getattr(obj, 'cleanup')

        run = getattr(obj, 'run')
        try:
            run()

        except KeyboardInterrupt:
            verbose.info('Stopped by user')

        except Exception:
            print(traceback.format_exc())
            if cleanup:
                cleanup()
            t, e = sys.exc_info()[:2]
            self.usage(e, errno=255)

        if cleanup:
            cleanup()
