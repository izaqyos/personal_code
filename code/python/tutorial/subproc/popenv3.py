#!/usr/bin/env python3
import asyncio
import os

#cmds=[ "cf logs portal-cf-transport-service ",  "cf logs portal-cf-site-semantic-service"]
cmds=[ "ls -l", "ls -a", "./print_nums.sh"]
class SubprocessProtocol(asyncio.SubprocessProtocol):
    def pipe_data_received(self, fd, data):
        if fd == 1: # got stdout data (bytes)
            print(data)

    def connection_lost(self, exc):
        loop.stop() # end loop.run_forever()

if os.name == 'nt':
    loop = asyncio.ProactorEventLoop() # for subprocess' pipes on Windows
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(loop.subprocess_exec(SubprocessProtocol, "cf", "logs", "portal-cf-transport-service "))
    loop.run_forever()
finally:
    loop.close()
