#!/opt/homebrew/bin/python3
import os, sys, shlex, subprocess , time

apiendpoint="https://api.cf.sap.hana.ondemand.com"
loginssocmd="cf login --sso"
tokenurl="https://login.cf.sap.hana.ondemand.com/passcode"
args = shlex.split(loginssocmd)

print(f"running {args} on API endpoint {apiendpoint}. Please browse to {tokenurl} and copy the token then paste it to login.")
#output=subprocess.run(args, stdout=subprocess.PIPE)
proc = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
#print(proc.stdout.readline())
#print(proc.stdout.readline())
#print(proc.stdout.readline())
proc.stdin.write(b'1\n')
proc.stdin.flush()
time.sleep(10)


print(proc.stdout.readlines())
