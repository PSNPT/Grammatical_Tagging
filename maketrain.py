import argparse
import xml.etree.ElementTree as ET

def prepare(xml, training):
    """
    Convert a xml to a training file
    """
    tree = ET.parse(xml)
    out = open(training ,"w")
    root = tree.getroot()

    for word in root.iter():
        if word.tag in ["w", "c"]:    
            s = "{} : {}\n".format(word.text.strip(), word.attrib["c5"].strip())
            out.write(s)

    out.close()

#################################################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
    "--xmlfile",
    type=str,
    required=True,
    help="One xml file."
    )
    parser.add_argument(
        "--trainingfile",
        required=True,
        help="The training files."
    )

    args = parser.parse_args()

    prepare(args.xmlfile, args.trainingfile)

