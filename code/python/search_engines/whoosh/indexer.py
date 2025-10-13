import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import sys

def createSearchableData(rootdir):

    '''
    Schema definition: title(name of file), path(as ID), content(indexed
    but not stored),textdata (stored text content)
    '''
    schema = Schema(title=TEXT(stored=True),path=ID(stored=True),\
              content=TEXT,textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    # Creating a index writer to add document as per schema
    ix = create_in("indexdir",schema)
    writer = ix.writer()

    for root, subdirs, files in os.walk(rootdir):
        # for sub in subdirs:
        #     print(sub)

        for f in files:
            fpath = os.path.join(root, f)
            print('inexing', fpath)
            #with open(fpath, mode='r', encoding='utf-8') as currentfile:
            with open(fpath, mode='rb') as currentfile:
                text = currentfile.read().decode(errors='ignore')
                base, fname = os.path.split(fpath)
                try:
                    print('indexind document', fname)
                    writer.add_document(title=fname, path=fpath, content=text, textdata=text)
                except Exception as ex:
                    print('caught exception', type(ex).__name__)

    writer.commit()

rootdir = "/Users/i500695/work/kb1"
createSearchableData(rootdir)
