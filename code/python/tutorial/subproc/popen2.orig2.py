#!/usr/local/bin/python3
import subprocess, shlex
import sys, os
import select
import pdb

cmds=[ "ls -l", "ls -a", "./print_nums.sh"]
#cmds = [
#         "curl --location --request GET 'https://stackoverflow.com/questions/65869646/process-input-from-multiple-command-line-input-sources'",
#         "curl --location --request GET 'https://stackoverflow.com/help/minimal-reproducible-example'",
#         ]
#cmds=[ "cf logs portal-cf-transport-service ",  "cf logs portal-cf-site-semantic-service"]

procs = [ subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE) for cmd in cmds ]
streams = [p.stdout for p in procs]
streams2Cmds = {k:v for (k,v) in zip(streams, cmds)}

def handler(line, stream):
    print('{}:\n{}'.format(streams2Cmds[stream], line.decode('utf-8')))

while True:
    rstreams,_,_ = select.select(streams, [], [])
    for stream in rstreams:
        print('handle input from {}'.format(streams2Cmds[stream]))
        line = stream.readline()
        handler(line, stream)
    if all(p.poll is not None for p in procs):
        break

for stream in streams:
    handler(stream.read(), stream)



