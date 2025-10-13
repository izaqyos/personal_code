#!/usr/bin/env python

# Backup files - As published in Python Cookbook
# by O'Reilly with some bug-fixes.

# Credit: Anand Pillai, Tiago Henriques, Mario Ruggier
import sys,os, shutil, filecmp

MAXVERSIONS=100

def backup_files(tree_top, bakdir_name='bak'):

    for dir, subdirs, files in os.walk(tree_top):
        backup_dir = os.path.join(dir, bakdir_name)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        # To avoid recursing into sub-directories
        subdirs[:] = [d for d in subdirs if d != bakdir_name]
        for f in files:
            filepath = os.path.join(dir, f)
            destpath = os.path.join(backup_dir, f)
            # Check existence of previous versions
            for index in xrange(MAXVERSIONS):
                backup = '%s.%2.2d' % (destpath, index)
                abspath = os.path.abspath(filepath)
                
                if index > 0:
                    # No need to backup if file and last version
                    # are identical
                    old_backup = '%s.%2.2d' % (destpath, index-1)
                    if not os.path.exists(old_backup): break
                    abspath = os.path.abspath(old_backup)
                    
                    try:
                        if os.path.isfile(abspath) and filecmp.cmp(abspath, filepath, shallow=False):
                            continue
                    except OSError:
                        pass
                
                try:
                    if not os.path.exists(backup):
                        print 'Copying %s to %s...' % (filepath, backup)
                        shutil.copy(filepath, backup)
                except (OSError, IOError), e:
                    pass

if __name__=="__main__":
    # run backup on specified directory
    try:
        tree_top = sys.argv[1]
    except IndexError:
        tree_top = '.'
    backup_files(tree_top)