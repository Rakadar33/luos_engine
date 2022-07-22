# -*- coding: utf-8 -*-
import argparse
import os
import sys
import time
import subprocess
from pathlib import Path


def luos_test(args):
    print('\nParameters\n--------------\n')
    print(f'Platform:\t {args.platform}')
    print(f'Scenario:\t {args.test}')
    print(f'Scenario parameters:\t {args.parameters}\n')

    command=f"python3 platforms\\{args.platform}\\{args.test}\\scenario.py"
    if args.parameters:
        for param in args.parameters:
            command+=f" {param}"            
    #print(f'\n\t**** Running: \r{command} ****\n\n')
    subprocess.run(command, shell=True)


def get_test_status(args):
    print(f'Get status for test {args.id}')
    print(f"[TODO] Feature Get Status")
    pass


def ci_options():
    parser = argparse.ArgumentParser(description='Continuous integration CLI')
    subparsers = parser.add_subparsers()

    # Subcommand "test"
    test_parser = subparsers.add_parser('test', help='launch a test on a QA platform')
    test_parser.add_argument('platform',
                              help='platform name')
    test_parser.add_argument('test',
                              help='scenario test name')
    test_parser.add_argument('-p', '--parameters',
                              nargs='*',
                              help='optionnal parameters for scenario')
    test_parser.set_defaults(func=luos_test)

    # Subcommand "status"
    status_parser = subparsers.add_parser('status',help='get test current status')
    status_parser.add_argument('id',
                                help='test ID ')
    status_parser.set_defaults(func=get_test_status)
    return parser


def main():
    parser = ci_options()
    args = parser.parse_args()

    # print help
    if len(sys.argv) < 2:
        print(f"\nFor help, type:\n\tpython {sys.argv[0]} -h\n")
        time.sleep(0.05)
        sys.exit()

    # run CLI subcommands
    args.func(args)


if __name__ == '__main__':
    sys.exit(main())
