#!/usr/bin/python
import sys
import subprocess
import re

#from action import run

PHASE = "prepush"
args = list()
i = 0
local_rsh = ''
remote_rsh = ''
arg_line = ''
for line in sys.stdin.xreadlines():
    arg_line = line

lines = arg_line.split(' ')

#Getting the local rsh and remote rsh
for line in lines:
    if i==1:
        local_rsh = line.rstrip()
    i = i+1


#Getting the remote rsh.
remote_rsh = subprocess.check_output(['git', 'rev-parse', 'remotes/origin/devel'])
remote_rsh = remote_rsh.rstrip()

# sprint_regex = '[0-9][0-9]*(:adhoc|:ssh)*'
# point_regex = '[0-9][0-9]*[\.]*[0-9]*'
# time_regex = '[0-9][0-9]*'
# trello_regex = '[\w\n]*trello.com'

total_regex = '^(change|add|fix)[\w\s,:;\n.\/-]*\([0-9][0-9]*(:adhoc|:ssh)*(\,[0-9][0-9]*(:adhoc|:ssh)*)*\)\[[0-9][0-9]*[\.]*[0-9]*(\,[0-9][0-9]*[\.]*[0-9]*)*]{[0-9][0-9]*(\.[0-9]+)*(\,[0-9][0-9]*(\.[0-9]+)*)*}[\w\s,:;\n.\/-]*https:\/\/trello\.com'
#reg_expression = '[(trello\.com)]\([0-9][0-9]*[:adhoc]*\)*\[[0-9][0-9]*[\.]*[0-9]*]{[0-9][0-9]*}'

git_refs = subprocess.check_output(['git', 'rev-list', remote_rsh + '..' + local_rsh])
git_refs = git_refs.rstrip()
git_refs = git_refs.split('\n')
total_no_refs = len(git_refs)


for each_git_ref in git_refs:
    message = subprocess.check_output(['git', 'log', '--format=%B', '-n 1', each_git_ref])
    #message = 'add author participation dashboard(163,164)[2]{3}. https://trello.com/c/llB9K5kZ'
    regex_match = re.search(total_regex, message)
    if regex_match == None:
        print 'Don\'t be lazy. Put the commit message in a proper format'
        sys.exit(1)

sys.exit(0)
