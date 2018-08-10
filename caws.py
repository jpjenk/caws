#!/usr/bin/env python3
"""Interactavly upgrade Python packages."""

import json
import subprocess
import sys

VERSION = '0.5.3'
APP_NAME = 'caws'
PIP_X = 'pip3'


def pip_upgrade(ask):
    """External call to the pip package manager."""
    syscall = subprocess.run([PIP_X, 'list', '--outdated',
                              '--format=json'], stdout=subprocess.PIPE)

    outdated = json.loads(syscall.stdout)

    if not outdated:

        print('All Python packages are up to date.')

    else:

        to_upgrade = list()
        for rec in outdated:
            to_upgrade.append(rec.get('name'))
        print('\nOutdated packages: {0:s}'.format(', '.join(to_upgrade)))

        for rec in outdated:

            choice = str()
            if ask:
                choice = input('\nUpdate {0:s} from {1:s} to {2:s}? [Y/n]  '
                               .format(rec.get('name'),
                                       rec.get('version'),
                                       rec.get('latest_version')))

            if choice.lower() == 'y' or choice == '' or not ask:
                pkg = rec.get('name')
                try:
                    syscall = subprocess.run([PIP_X, 'install', '-U', pkg])
                except subprocess.SubprocessError:
                    sys.exit()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        switch = sys.argv[1]
    else:
        switch = None

    if switch == '-h' or switch == '--help':

        print('usage: caws [option]\n')
        print('optional arguments:')
        print('-h, --help       Help on commandline switches')
        print('-v, --version    Print version string')
        print('-l, --list       Show outdated packages')
        print('-u, --update     Interactive updater')
        print('-a, --all        Batch uprgade all packages')

    elif switch == '-v' or switch == '--version':

        syscall = subprocess.run([PIP_X, '--version'], stdout=subprocess.PIPE)

        print('The Cheese Shop Updater (version {0:s})'.format(VERSION))
        print('(c) 2018 YarraRiver\n')
        print(syscall.stdout.decode('utf-8'))

    elif switch == '-l' or switch == '--list':

        syscall = subprocess.run([PIP_X, 'list', '--outdated',
                                  '--format=columns'], stdout=subprocess.PIPE)

        outdated = syscall.stdout.decode('utf-8')

        if not outdated:
            print('All Python packages are up to date.')
        else:
            print(outdated)

    elif switch == '-u' or switch == '--upgrade' or not switch:

        pip_upgrade(ask=True)

    elif switch == '-a' or switch == '--all':

        pip_upgrade(ask=False)

    else:

        print('{0:s}: illegal option {1:s}'.format(APP_NAME, switch))
