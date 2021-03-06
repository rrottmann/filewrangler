# Keep organized with filewrangler

Define custom rules and filewrangler will do the organization.

## Usage

~~~
$ ./filewrangler.py --help
usage: filewrangler.py [-h] [--debug] [--execute] [--path PATH] [--quiet]
                       [--rules RULES]

Organize files according to tags and custom rulesets.

optional arguments:
  -h, --help     show this help message and exit
  --debug        Enable debug output.
  --execute      Execute the generated commands.
  --path PATH    Path to process. Default: .
  --quiet        Quiet mode.
  --rules RULES  Yaml file with rules. Default: rules.yml

Copyright 2017 by Reiner Rottmann <reiner@rottmann.it>. Released under GPLv3.
~~~

## Example: Move files according to tags

  * Add tags 'backup', 'perm', 'public', 'docs', 'websites' between '[' and ']'
    right before the file extension to a test file

~~~
$ ls -l
total 0
-rw-r--r--. 1 root root 0 Jan  6 02:56 170106-test-file [backup perm public docs websites].html
~~~ 

  * Create a file 'rules.yml' in the same directory with the following contents:

~~~
---
- rule: 3c2f5984-e006-4b92-9ea9-695e4acb4ff9
  description: 'Example: Move backup/perm/public/docs/websites'
  conditions:
    - condition: 25dda54e-bd3c-449a-8349-9981c07111ef
      type: 'regex'
      regex: '^.*\[.*backup.*\].*$'
    - condition: ada3c3c4-d016-4d7d-b11f-9851f2726cc6
      type: 'regex'
      regex: '^.*\[.*perm.*\].*$'
    - condition: 9a1469ec-4ddf-40a4-8701-e8ef83e93b37
      type: 'regex'
      regex: '^.*\[.*public.*\].*$'
    - condition: 6b8abc8e-d41a-4c48-ba87-b3a56e10fcaf
      type: 'regex'
      regex: '^.*\[.*docs.*\].*$'
    - condition: 6b6bd4be-d0ef-4dba-bf19-66a38dd37d67
      type: 'regex'
      regex: '^.*\[.*websites.*\].*$'
  actions:
    - action: a953af7c-bdc3-4ffe-aad0-41459f0d0afe
      type: 'cmd'
      cmd: '[ -d /tmp/backup/perm/public/docs/websites ] || mkdir -p /tmp/backup/perm/public/docs/websites'
    - action: 554c5975-23d3-42e4-ade8-b7b558bc228f
      type: 'cmd'
      cmd: 'mv "{}" "/tmp/backup/perm/public/docs/websites/{}"'
...
~~~

  * Run filewrangler with debug output

~~~
$ ~/filewrangler/filewrangler.py --debug
#DEBUG: Processing directory: .
#DEBUG: Processing rules from file: rules.yml
#INFO:  * Processing rule: Example: Move backup/perm/public/docs/websites
#DEBUG:   * Processing file: 170106-test-file [backup perm public docs websites].html
#DEBUG:     * Processing condition: 25dda54e-bd3c-449a-8349-9981c07111ef
#DEBUG:       * Processing regex: ^.*\[.*backup.*\].*$
#DEBUG:         * Condition matched.
#DEBUG:     * Processing condition: ada3c3c4-d016-4d7d-b11f-9851f2726cc6
#DEBUG:       * Processing regex: ^.*\[.*perm.*\].*$
#DEBUG:         * Condition matched.
#DEBUG:     * Processing condition: 9a1469ec-4ddf-40a4-8701-e8ef83e93b37
#DEBUG:       * Processing regex: ^.*\[.*public.*\].*$
#DEBUG:         * Condition matched.
#DEBUG:     * Processing condition: 6b8abc8e-d41a-4c48-ba87-b3a56e10fcaf
#DEBUG:       * Processing regex: ^.*\[.*docs.*\].*$
#DEBUG:         * Condition matched.
#DEBUG:     * Processing condition: 6b6bd4be-d0ef-4dba-bf19-66a38dd37d67
#DEBUG:       * Processing regex: ^.*\[.*websites.*\].*$
#DEBUG:         * Condition matched.
#DEBUG:   * Processing file: rules.yml
#DEBUG:     * Processing condition: 25dda54e-bd3c-449a-8349-9981c07111ef
#DEBUG:       * Processing regex: ^.*\[.*backup.*\].*$
#DEBUG:         * Condition did NOT match.
#DEBUG: Commands for file: 170106-test-file [backup perm public docs websites].html
[ -d /tmp/backup/perm/public/docs/websites ] || mkdir -p /tmp/backup/perm/public/docs/websites
mv "170106-test-file [backup perm public docs websites].html" "/tmp/backup/perm/public/docs/websites/170106-test-file [backup perm public docs websites].html"
~~~

  * Inspect the resulting shell commands whether they fit your purpose.
  * Run filewrangler again to execute the resulting shell commands:

~~~
$ filewrangler.py --quiet | sh -x
+ '[' -d /tmp/backup/perm/public/docs/websites ']'
+ mkdir -p /tmp/backup/perm/public/docs/websites
+ mv '170106-test-file\ \[backup\ perm\ public\ docs\ websites\].html' '/tmp/backup/perm/public/docs/websites/170106-test-file\ \[backup\ perm\ public\ docs\ websites\].html'
~~~

You can also append the commandline option '--execute' to run all the generated commands.

  * The file has now been organized according to the rule set.

~~~
$ ls -al /tmp/backup/perm/public/docs/websites/
total 0
drwxr-xr-x. 2 root root 76 Jan  6 03:06 .
drwxr-xr-x. 3 root root 21 Jan  6 03:06 ..
-rw-r--r--. 1 root root  0 Jan  6 02:56 170106-test-file\ \[backup\ perm\ public\ docs\ websites\].html
~~~

# Create your own rules with mkrule.py

While you could create your rules manually, you could also use the mkrule.py script for simple move operations

~~~
 ./mkrule.py  --description="Move files matching foo/bar/baz to /tmp/foo/bar/baz" --directory="/tmp/foo/bar/baz" --tags='foo,bar,baz'
---
- rule: 68c5f194-af1b-4e2b-a87e-b4df78b1211d
  description: 'Move files matching foo/bar/baz to /tmp/foo/bar/baz'
  conditions:
    - condition: f435fd85-760a-46b7-8ab3-49e7e94712f1
      type: 'regex'
      regex: '^.*\[.*foo.*\].*$
    - condition: c506875c-9315-4684-ad30-25629d5a30c9
      type: 'regex'
      regex: '^.*\[.*bar.*\].*$
    - condition: 68aed435-9583-4062-b3c5-7f5160a80335
      type: 'regex'
      regex: '^.*\[.*baz.*\].*$
   actions:
     - action: 587dbf76-eaa0-4967-93f3-e0b5fd521c78
       type: 'cmd'
       cmd: '[ -d /tmp/foo/bar/baz] || mkdir -p /tmp/foo/bar/baz'
     - action: 2759131d-0f61-41fd-9aaa-7da89b8a3ae4
       type: 'cmd'
       cmd: 'mv "{}" "/tmp/foo/bar/baz/{}"'
...
~~~

# Tipp: Exclude tags from rule

Maybe you want to exclude a specific tag from a rule. At least I use it a lot!
This is done very easily - even when you have zero knowledge of Python's regex.

E.g you do not want to do any actions on files with the tag 'doc'.

The necessary regular expression to invert the match is as follows:

~~~
'(?!^.*\[.*docs.*\].*)'
~~~

You simply have to add '(?!' at the beginning and ')' at the end of the regular expression.

# Tipp: Workarounds for the limited condition matching and actions

The script currently offers only regex matches and cmd for both conditions and actions.

While the regular expressions can be used for very complex scenarios, the cmd
action currently only supports expansion of the following variables:

 * {}:  original filename
 * {d}: processed directory (--path)

However as simple shell scriptlets are being executed, you could use shell
variables to your likings. Simply declare them, so that they are available for
the following command:

~~~
  actions:
    - action: 72bde999-40a4-40c8-8888-507bade035f1
      type: 'cmd'
      cmd: 'baz=foo;'
    - action: 368ee9e0-3a0c-443e-9a5b-5f9fa15c604f
      type: 'cmd'
      cmd: 'echo $baz'
~~~

Output:

~~~
./filewrangler.py --quiet| sh -x
+ baz=foo
+ echo foo
foo
~~~

This could be used for example to prepend the file's creation date:

~~~
- rule: 00b70fb6-d6b4-11e6-9d7e-cfc8c0b233a1
  description: 'Prepend file creation date to 7z|doc|docx|htm|html|md|mhtml|ods|odt|rst|txt|xls|xlsx|zip'
  conditions:
    - condition: 4d10e2ec-d6b4-11e6-89e9-471278e9b7c1
      type: 'regex'
      regex: '^.*\.(7z|doc|docx|htm|html|md|mhtml|ods|odt|rst|txt|xls|xlsx|zip)$'
    - condition: a357dbc2-d6b6-11e6-b1c0-973f85398267
      type: 'regex'
      regex: '(?!^\d{4}.*$)'
  actions:
    - condition: 18b86c44-d6b5-11e6-9513-9bb78cabf0b1
      type: 'atime'
      atime: 1
    - action: 96ffdcaa-d6b4-11e6-9e7a-9f3deaa37bb3
      type: 'cmd'
      cmd: 'ts=$(stat -c "%y" "{d}/{}" | tr -d "-" | cut -d" " -f1 | sed "s/^20//g")'
    - action: e2a24ee0-d6b4-11e6-8a5a-bbef2dff80dd
      type: 'cmd'
      cmd: 'mv "{d}/{}" "{d}/$ts-{}"' 
~~~

# Tipp: Add tags based on other tags / regular expressions

You could combine this script with https://github.com/rrottmann/managetags
That is also my major use case for the managetags tool.

E.g. you could tag bank statements automatically:

~~~
- rule: 4eba2a3a-d6fb-11e6-98a4-33d9c4753983
  description: 'Tag bank statements from DiBa'
  conditions:
    - condition: 549745f0-d6fb-11e6-8f57-e3459bf31d72
      type: 'atime'
      atime: 1
    - condition: 5b469f22-d6fb-11e6-9161-23258a155688
      type: 'regex'
      regex: '^Direkt_Depot_\d{10}_.*\.pdf'
  actions:
    - action: 60057cf4-d6fb-11e6-bf35-9340807a3666
      type: 'cmd'
      cmd: 'depot=$(echo -n "{}" | grep -Eo "_[0-9]{10}" | tr -d "_")'
    - action: 6453b104-d6fb-11e6-a5d1-635d61273ed2
      type: 'cmd'
      cmd: '/opt//managetags/managetags.py --path "{d}/{}" --addtags="backup,perm,secret,important,docs,finances,diba,depot$depot" | sh -x'
~~~

# Tipp: Use cmd condition for advanced rules

The cmd condition has been implemented. This allows more advanced conditions.

E.g. to match the mime type of a file:

~~~
    - condition: c9ca025e-dca1-4545-941e-0e251eeb59b9
      type: 'cmd'
      cmd: 'file -ib "{}" | cut -d \; -f1 | tr -d "\n"'
      stdout: 'video/mp4'
~~~

You could also grep for a given string in a text file:

~~~
    - condition: 330389fe-6d1a-4c8f-a492-014193531654
      type: 'cmd'
      cmd: 'file -ib "{}" | cut -d \; -f1 | tr -d "\n"'
      stdout: 'text/plain'
    - condition: 031ef121-7554-449b-affb-5fb27ea2c9fa
      type: 'cmd'
      cmd: 'grep -q "ABCD" "{}"'
      returncode: 0
~~~

And you may search even in PDF files:

~~~
    - condition: e4e73700-e228-4602-8531-83c8c26f944b
      type: 'cmd'
      cmd: 'file -ib "{}" | cut -d \; -f1 | tr -d "\n"'
      stdout: 'application/pdf'
    - condition: 3f3f132c-9878-458a-bfee-412962921fe9
      type: 'cmd'
      cmd: 'pdftotext "{}" - | grep -q "ABCD"'
      returncode: 0
~~~

pdf2text is part of poppler-utils package on Debian / CentOS

Please note: The above examples seem complex and use a lot of shell
scripting vodoo. However, in most cases you do not need to change
the commands later and may use them as a blueprint.

# Tipp: Use atime condition for advanced rules

The atime condition has been implemented. This allows more advanced conditions.

E.g. You could use this condition to check whether the file is settled and has not
been accessed some minutes before.

~~~
    - condition: 2a4ea45c-c400-4cdf-a3d1-a87d383018af
      type: 'atime'
      atime: 5
~~~

This is especially useful, if you intend to add tags to a file and thus you
are renaming it and then you intend to move the file. 

As the file has been renamed, later rules will not find the file with
it's original filename.

The filewrangler script usually gets invoked via cron. So the renamed file
will be picked up during the next run.

# Tipp: Use skip action for advanced rules

The skip action has been implemented. This allows more advanced rulesets.

When all conditions of a ruleset match, you could use the skip action to add
the filename to a skip list. This means, that it will be ignored for the rest
of the current execution phase.

E.g.:

~~~
- action: 84cb4a8d-c34e-425e-bbd5-1c8f953b12e5
  type: 'skip'
~~~

Resulting in:
~~~
...
#DEBUG:     * Processing action: 84cb4a8d-c34e-425e-bbd5-1c8f953b12e5
#DEBUG:       * Type: skip
#DEBUG:         * Adding file to the skip list.
#DEBUG:     * Processing action: 554c5975-23d3-42e4-ade8-b7b558bc228f
#DEBUG:       * Type: cmd
#DEBUG:          * cmd: 'echo $baz'
#DEBUG:            * File is on the skip list. Ignoring action.
..
~~~

# Tipp: You can comment out rules

Especially during the development of your ruleset, you may need to comment
out some rules or you want to add sample rules as a reference.
YAML supports comments. All lines that begin with '#' are ignored.

# Tipp: Works great on Windows!

While I use this tool mainly on Linux / BSD, the script works within Cygwin on
Windows (needed because of mv / bash).

However you will need to install a Python interpreter during Cygwin setup!

Cywin may be found here: http://cygwin.org/
