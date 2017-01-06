# Keep organized with filewrangler

Define custom rules and filewrangler will do the organization.

## Usage

~~~
$ ./filewrangler.py --help
usage: filewrangler.py [-h] [--debug] [--path PATH] [--quiet] [--rules RULES]

optional arguments:
  -h, --help     show this help message and exit
  --debug        Enable debug output.
  --path PATH    Path to process. Default: .
  --quiet        Quiet mode.
  --rules RULES  Yaml file with rules. Default: rules.yml
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

  * The file has now been organized according to the rule set.

~~~
$ ls -al /tmp/backup/perm/public/docs/websites/
total 0
drwxr-xr-x. 2 root root 76 Jan  6 03:06 .
drwxr-xr-x. 3 root root 21 Jan  6 03:06 ..
-rw-r--r--. 1 root root  0 Jan  6 02:56 170106-test-file\ \[backup\ perm\ public\ docs\ websites\].html
~~~
