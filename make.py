import argparse
import xml.etree.ElementTree as ET
import os
from pathlib import Path

def XMLtoTraining(xml, training):
    """
    Convert a xml to a training file
    """
    tree = ET.parse(xml)
    out = open(training,"w")
    root = tree.getroot()

    for word in root.iter():
        if word.tag in ["w", "c"]:
            s = ""
            try:
                s = "{} : {}\n".format(word.text.strip(), word.attrib["c5"].strip())
                out.write(s)
                continue
            except:
                s = ""
                
            out.write(s)

    out.close()

def TrainingtoTest(training, test):
    """
    Convert a training file to a test file
    """
    f = open(training, "r")
    w = open(test,"w")

    ret = []
    sentence = []

    for line in f:
        tokens = line.strip().split(' : ')
        
        s = "{}\n".format(tokens[0])
        w.write(s)

    f.close()
    w.close()

#################################################################
TYPES = ['aca', 'dem', 'fic', 'news']
if __name__ == '__main__':

    print("Removing old files")
    for type in TYPES:
        for file in os.listdir("training/"+type):
            os.remove("./training/"+type+"/"+file)

    for type in TYPES:
        for file in os.listdir("testing/"+type):
            os.remove("./testing/"+type+"/"+file)

    print("Generating")
    for type in TYPES:
        for xmlfile in os.listdir(type):
            XMLtoTraining("./"+type+"/"+xmlfile, "./training/"+type+"/" + Path(xmlfile).stem + ".txt")

    for type in TYPES:
        for trainingfile in os.listdir("training/"+type+"/"):
                TrainingtoTest("./training/"+type+"/"+trainingfile, "./testing/"+type+"/"+trainingfile)

