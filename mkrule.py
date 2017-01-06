#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2017 by Reiner Rottmann <reiner@rottmann.it>.
Released under GPLv3 or later: https://www.gnu.org/licenses/gpl-3.0.txt
"""

import argparse
import uuid

__version__ = "0.1"

def _mkrule(description, directory, tags=None):
    '''
    Create a new move rule with given list of tags.
    Provide a description and a target directory for
    moving the matching files.
    '''
    rule = []
    rule.append('---')
    rule.append('- rule: ' + str(uuid.uuid4()))
    rule.append("  description: '" + description + "'")
    rule.append('  conditions:')
    for tag in tags:
        rule.append('    - condition: ' + str(uuid.uuid4()))
        rule.append("      type: 'regex'")
        rule.append("      regex: '^.*\[.*" + tag + ".*\].*$'")
    rule.append('  actions:')
    rule.append('     - action: ' + str(uuid.uuid4()))
    rule.append("       type: 'cmd'")
    rule.append("       cmd: '[ -d " + directory + "] || mkdir -p " + directory + "'")
    rule.append('     - action: ' + str(uuid.uuid4()))
    rule.append("       type: 'cmd'")
    rule.append("       cmd: 'mv " + '"{}" ' + '"' + directory + '/{}"' + "'")
    rule.append('...')
    return '\n'.join(rule)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--description',
                        help='Description for the rule..', required=True)
    parser.add_argument('--directory',
                        help='Target directory for matching files.', required=True)
    parser.add_argument('--tags',
                        help='Comma seperated list of tags to match', required=True)
    args = parser.parse_args()
    print _mkrule(args.description, args.directory, args.tags.split(','))
