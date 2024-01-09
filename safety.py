#################################################################
import os
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
            #try:
            if word.attrib["c5"] == None:
                continue
            if word.text == None:
                continue
            
            s = "{} : {}\n".format(word.text.strip(), word.attrib["c5"].strip())
            out.write(s)
                #continue
            #except:
                #s = ""
                
            #out.write(s)

    out.close()


if __name__ == '__main__':

    for filename in os.listdir("fic"):
        XMLtoTraining("./fic/"+filename, "TEZT.txt")
        
        