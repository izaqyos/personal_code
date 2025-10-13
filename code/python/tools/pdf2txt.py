#!/usr/local/bin/python3
# coding: utf-8

import os, sys

#To install Quartz, $pip3 install pyobjc-framework-Quartz
from Quartz import PDFDocument
from CoreFoundation import (NSURL, NSString)
NSUTF8StringEncoding = 4

def pdf2txt(printToScreen=True):
    for filename in sys.argv[1:]:   
        inputfile =filename
        shortName = os.path.splitext(filename)[0]
        outputfile = shortName+".txt"
        print(inputfile, shortName)
        pdfURL = NSURL.fileURLWithPath_(inputfile)
        pdfDoc = PDFDocument.alloc().initWithURL_(pdfURL)
        if pdfDoc :
            pdfString = NSString.stringWithString_(pdfDoc.string())
            pdfString.writeToFile_atomically_encoding_error_(outputfile, True, NSUTF8StringEncoding, None)
        if printToScreen:
            print(outputfile)
            with open(outputfile, 'r') as output:
                lines = output.readlines()
                print(lines)

if __name__ == "__main__":
    pdf2txt(True)
