#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2017 by Reiner Rottmann <reiner@rottmann.it>.
Released under GPLv3 or later: https://www.gnu.org/licenses/gpl-3.0.txt
"""

__version__ = "0.1"

import os
import re
import sys
import yaml
import time
import logging
import argparse
import datetime
import subprocess


def _execute(cmds=None):
    '''Execute a list of commands.'''
    for cmd in cmds:
        logging.debug('* Executing cmd: ' + cmd) 
        process = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        if stdout:
            for line in stdout.splitlines():
                logging.debug('  * STDOUT: ' + line) 
        if stderr:
            for line in stderr.splitlines():
                logging.debug('  * STDERR: ' + line) 


def _load_rules(path='rules.yml'):
    '''Load rules yaml file from path.'''
    fd = open(path, 'r')
    yml = yaml.safe_load(fd)
    fd.close()
    return yml


def _load_skiplist(path='skip.yml'):
    fd = open(path, 'r')
    yml = yaml.safe_load(fd)
    fd.close()
    return yml


def _save_skiplist(skiplist, path='skip.yml'):
    yml = yaml.dump(skiplist, default_flow_style = False, allow_unicode = True, encoding = None)
    fd = open(path, 'w')
    fd.write(yml)
    fd.close()


def _rules_engine(path, rules=None):
    '''Processes all files in given path. Requires rules dict.'''
    files = os.listdir(path)
    targets = []
    actions = {}
    if os.path.exists('skip.yml'):
        skip = _load_skiplist()
    else:
        skip = {}
    for rule in rules:
        logging.info(' * Processing rule: ' + rule['description'])
        for elem in ['rule', 'description', 'conditions', 'actions']:
            if elem not in rule:
                logging.warning('Missing element in rule definition: ' + elem)
                continue
        for fname in files:
            brk = False
            logging.debug(' '*2+'* Processing file: ' + fname)
            if fname not in actions.keys():
                actions[fname] = {}
            for condition in rule['conditions']:
                for elem in ['condition', 'type']:
                    if elem not in condition:
                        logging.warning(
                                'Missing element in condition definition: ' +
                                elem)
                        continue
                logging.debug('    * Processing condition: ' +
                              condition['condition'])
                match = False
                if condition['type'] == 'atime':
                    if 'atime' in condition.keys():
                        minutes = condition['atime']
                        logging.debug(' '*6+'* Processing atime: ' +
                                      'last access before ' +
                                      str(minutes) + ' minute(s)')
                        if _condition_atime(os.path.join(path, fname), minutes):
                            match = True
                        else:
                            match = False
                if condition['type'] == 'cmd':
                    if 'cmd' in condition.keys():
                        cmd = condition['cmd']
                        cmd = _replace_variables(cmd, fname, path)
                        logging.debug(' '*6+'* Processing cmd: ' +
                                      condition['cmd'])
                        process = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
                        stdout, stderr = process.communicate()
                        if 'stdout' in condition.keys():
                            logging.debug(' '*8+'* Checking for stdout: ' +
                                          condition['stdout'])
                            if stdout == condition['stdout']:
                                match = True
                            else:
                                match = False
                        if 'returncode' in condition.keys():
                            logging.debug(' '*8+'* Checking for returncode: ' +
                                          str(condition['returncode']))
                            if process.returncode == condition['returncode']:
                                match = True
                            else:
                                match = False
                    else:
                        logging.warning('Missing element in' +
                                        'condition definition: cmd')
                        continue
                if condition['type'] == 'regex':
                    if 'regex' in condition.keys():
                        logging.debug(' '*6+'* Processing regex: ' +
                                      condition['regex'])
                        regex = re.compile(condition['regex'])
                        if regex.match(fname):
                            match = True
                    else:
                        logging.warning('Missing element in' +
                                        'condition definition: regex')
                        continue
                if match:
                    logging.debug(' '*8+'* Condition matched.')
                    if fname not in targets:
                        targets.append(fname)
                    continue
                else:
                    logging.debug(' '*8+'* Condition did NOT match.')
                    if fname in targets:
                        targets.remove
                    brk = True
                    break
            if brk:
                continue
            for action in rule['actions']:
                logging.debug('    * Processing action: ' +
                        action['action'])
                if 'type' in action.keys():
                    type = action['type']
                    logging.debug(' '*6+'* Type: ' + type)
                    if type in action.keys():
                        logging.debug(' '*8+' * ' + type + ': \'' + action[type] + "'")
                if fname in skip.keys():
                    logging.debug(' '*11+'* File is on the skip list. Ignoring action.')
                    skip[fname] -= 1
                    if skip[fname] <= 0:
                        del skip[fname]
                    continue
                if 'type' not in action.keys():
                    continue
                if action['type'] == 'cmd':
                    if 'cmd' in action.keys():
                        cmd = action['cmd']
                        cmd = _replace_variables(cmd, fname, path)
                        if 'cmds' not in actions[fname].keys():
                            actions[fname]['cmds'] = []
                        actions[fname]['cmds'].append(cmd)
                if action['type'] == 'skip':
                    if not fname in skip.keys():
                        skip[fname] = 0
                    skip[fname] += 1
    _save_skiplist(skip)
    return actions


def _condition_atime(path, minutes):
    '''Check whether the file has not been accessed for the given minutes.'''
    fmt = "%s"
    now = datetime.datetime.now()
    now = now.strftime(fmt)
    atime = datetime.datetime.strptime(time.ctime(os.path.getatime(path)), "%c").strftime(fmt)
    logging.debug(' '*8 + '* File access time: ' + str((int(now)-int(atime))/60) + ' minute(s) ago')
    if int(atime) > int(now) - 60 * minutes:
        return False
    else:
        return True


def _execute_actions(actions, dryrun=True):
    '''Output given actions dict to stdout.'''
    for fname in actions.keys():
        for action in actions[fname].keys():
            if not type(actions[fname]) == dict:
                continue
            for elem in actions[fname].keys():
                if elem == 'cmds':
                    logging.debug('Commands for file: ' + fname)
                    for cmd in actions[fname][elem]:
                        if dryrun:
                            print cmd
                        else:
                            _execute([cmd])


def _replace_variables(strinput, fname, path):
    '''Conditions and actions can use program internal variables.'''
    if '{}' in strinput:
        strinput = strinput.replace('{}', fname)
    if '{d}' in strinput:
        strinput = strinput.replace('{d}', path)
    return strinput


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
    Organize files according to tags and custom rulesets.''',
    epilog='''
    Copyright 2017 by Reiner Rottmann <reiner@rottmann.it>.
    Released under GPLv3.
    ''')
    parser.add_argument('--debug', help='Enable debug output.', action='store_true')
    parser.add_argument('--execute', help='Execute the generated commands.', action='store_true')
    parser.add_argument('--path',
                        help='Path to process. Default: .',
                        default='.')
    parser.add_argument('--quiet', help='Quiet mode.', action='store_true')
    parser.add_argument('--rules',
                        help='Yaml file with rules. Default: rules.yml',
                        default='rules.yml')
    args = parser.parse_args()
    if args.quiet:
        logging.basicConfig(level=logging.CRITICAL, format='#%(levelname)s: %(message)s')
    else:
        if args.debug:
            logging.basicConfig(level=logging.DEBUG, format='#%(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='#%(levelname)s: %(message)s')
    logging.debug('Processing directory: ' + args.path)
    logging.debug('Processing rules from file: ' + args.rules)
    if args.execute is False:
        logging.debug('Running in dryrun mode.')

    if not os.path.exists(args.path) or not os.path.isdir(args.path):
        logging.error('No such dir: ' + args.path)
        sys.exit(1)
    if not os.path.exists(args.rules) or not os.path.isfile(args.rules):
        logging.error('No such file: ' + args.rules)
        sys.exit(1)
    rules = _load_rules(args.rules)
    if not rules:
        logging.error('No rules found.')
        sys.exit(1)
    actions = _rules_engine(args.path, rules)
    if args.execute is True:
        _execute_actions(actions, dryrun=False)
    else:
        _execute_actions(actions)
