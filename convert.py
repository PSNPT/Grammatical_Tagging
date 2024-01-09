import argparse


def prepare(training, test):
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
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trainingfile",
        required=True,
        help="The training files."
    )
    parser.add_argument(
        "--testfile",
        type=str,
        required=True,
        help="One test file."
    )

    args = parser.parse_args()

    prepare(args.trainingfile, args.testfile)

