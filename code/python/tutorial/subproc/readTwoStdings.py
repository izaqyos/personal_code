#!/usr/bin/env python
import os
import shutil
import subprocess
import tempfile
import threading
from contextlib import contextmanager    
import pandas as pd

@contextmanager
def named_pipes(count):
    dirname = tempfile.mkdtemp()
    try:
        paths = []
        for i in range(count):
            paths.append(os.path.join(dirname, 'named_pipe' + str(i)))
            os.mkfifo(paths[-1])
        yield paths
    finally:
        shutil.rmtree(dirname)

def write_command_input(df, path):
    df.to_csv(path, header=False,index=False, sep="\t")

dfA = pd.DataFrame([[1,2,3],[3,4,5]], columns=["A","B","C"])
dfB = pd.DataFrame([[5,6,7],[6,7,8]], columns=["A","B","C"])

with named_pipes(2) as paths:
    p = subprocess.Popen(["cat"] + paths, stdout=subprocess.PIPE)
    with p.stdout:
        for df, path in zip([dfA, dfB], paths):
            t = threading.Thread(target=write_command_input, args=[df, path]) 
            t.daemon = True
            t.start()
        result = pd.read_csv(p.stdout, header=None, sep="\t")
p.wait()
