#!/usr/local/bin/python3

import subprocess
import os
import time
import shlex #for simple cmd line parsing
import logging
logging.basicConfig(level = logging.INFO)

def removeFinishedProcesses(processes):
    """ given a list of (commandString, process), 
        remove those that have completed and return the result 
    """
    newProcs = []
    for pollCmd, pollProc in processes:
        retCode = pollProc.poll()
        if retCode==None:
            # still running
            newProcs.append((pollCmd, pollProc))
        elif retCode!=0:
            # failed
            raise Exception("Command %s failed" % pollCmd)
        else:
            logging.info("Command %s completed successfully" % pollCmd)
    return newProcs

def runCommands(commands, maxCpu):
            processes = []
            for command in commands:
                logging.info("Starting process %s" % command)
                proc =  subprocess.Popen(shlex.split(command))
                procTuple = (command, proc)
                processes.append(procTuple)
                while len(processes) >= maxCpu:
                    time.sleep(.2)
                    processes = removeFinishedProcesses(processes)

            # wait for all processes
            while len(processes)>0:
                time.sleep(0.5)
                processes = removeFinishedProcesses(processes)
            logging.info("All processes completed")

preCmd = [ "node_modules/.bin/grunt getUrlTemplate" ]
cmds = [ "npm run uiveri5-mock-contentManager","npm run uiveri5-mock-businessapp","npm run uiveri5-mock-catalog","npm run uiveri5-mock-role","npm run uiveri5-mock-group","npm run uiveri5-mock-assignmentPanel","npm run uiveri5-mock-menuEditor","npm run uiveri5-mock-site-directory","npm run uiveri5-mock-siteSetting"] 
postCmd = []

def main():
    runCommands(preCmd, 6)
    runCommands(cmds, 6)
    runCommands(postCmd, 6)


if __name__ == "__main""__":
    main()
