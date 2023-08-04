import os
import argparse
import time
from typing import List

################################################################
pos_tags = ["AJ0", "AJC", "AJS", "AT0", "AV0", "AVP", "AVQ", "CJC", "CJS", "CJT", "CRD",
        "DPS", "DT0", "DTQ", "EX0", "ITJ", "NN0", "NN1", "NN2", "NP0", "ORD", "PNI",
        "PNP", "PNQ", "PNX", "POS", "PRF", "PRP", "PUL", "PUN", "PUQ", "PUR", "TO0",
        "UNC", 'VBB', 'VBD', 'VBG', 'VBI', 'VBN', 'VBZ', 'VDB', 'VDD', 'VDG', 'VDI',
        'VDN', 'VDZ', 'VHB', 'VHD', 'VHG', 'VHI', 'VHN', 'VHZ', 'VM0', 'VVB', 'VVD',
        'VVG', 'VVI', 'VVN', 'VVZ', 'XX0', 'ZZ0', 'AJ0-AV0', 'AJ0-VVN', 'AJ0-VVD',
        'AJ0-NN1', 'AJ0-VVG', 'AVP-PRP', 'AVQ-CJS', 'CJS-PRP', 'CJT-DT0', 'CRD-PNI', 'NN1-NP0', 'NN1-VVB',
        'NN1-VVG', 'NN2-VVZ', 'VVD-VVN', 'AV0-AJ0', 'VVN-AJ0', 'VVD-AJ0', 'NN1-AJ0', 'VVG-AJ0', 'PRP-AVP',
        'CJS-AVQ', 'PRP-CJS', 'DT0-CJT', 'PNI-CRD', 'NP0-NN1', 'VVB-NN1', 'VVG-NN1', 'VVZ-NN2', 'VVN-VVD']

################################################################
TRAINDIR = "training"
TESTDIR = "testing"
OUTDIR = "output"

TAGS = set(pos_tags)
WORDS = set()
SORTEDTAGS = None
SORTEDWORDS = None

WORDTAG = {}

PUN = [".", "!", "?"]

I = {}
SENTENCES = 0
T = {}
TOCCUR = {}
M = {}
MOCCUR = {}

TINY = 10 ** -20

def tagging(filenames):
    """
    Parse training data
    """
    global SENTENCES
    for filename in filenames:
        f = open(os.path.join(TRAINDIR, filename), "r")

        prev = None

        for line in f:

            # Splitting into word-tag pair
            tokens = line.strip().split(' : ')
            if len(tokens) != 2:
                continue
            
            if tokens[1].strip().upper() not in TAGS:
                continue

            word = tokens[0].strip().lower()
            tag = tokens[1].strip().upper()

            # Updating all tags and all words
            WORDS.add(word)
            
            # Update wordtag
            if word not in WORDTAG:
                WORDTAG[word] = set()
            
            WORDTAG[word].add(tag)

            # First token
            if not prev:
                if tag not in I:
                    I[tag] = 1
                else:
                    I[tag] += 1

            # Not first
            else:
                pword = prev[0]
                ptag = prev[1]

                # Updating T
                if ptag not in T:
                    T[ptag] = {}

                if ptag not in TOCCUR:
                    TOCCUR[ptag] = 1
                else:
                    TOCCUR[ptag] += 1

                if tag not in T[ptag]:
                    T[ptag][tag] = 1
                else:
                    T[ptag][tag] += 1
                

            # Updating M
            if tag not in M:
                M[tag] = {}

            if tag not in MOCCUR:
                MOCCUR[tag] = 1
            else:
                MOCCUR[tag] += 1

            if word not in M[tag]:
                M[tag][word] = 1
            else:
                M[tag][word] += 1

            # Setting up for next iteration

            # Checking for End Of Sentence
            if word in PUN:
                prev = None
                SENTENCES += 1
            else:
                prev = tokens

        # Data read, now converting to probabilities
        f.close()

    # Converting I
    for tag in I:
        I[tag] = I[tag] / float(SENTENCES)
    
    # Setting unassigned I to 0
    for tag in TAGS:
        if tag not in I:
            I[tag] = 0

    # Converting T
    for ptag in T:
        for tag in T[ptag]:
            T[ptag][tag] = T[ptag][tag] / float(TOCCUR[ptag])

    # Setting unassigned T to 0
    for ptag in TAGS:

        if ptag not in T:
            T[ptag] = {}

        for tag in TAGS:
            if tag not in T[ptag]:
                T[ptag][tag] = 0

    # Converting M
    for tag in M:
        for word in M[tag]:
            M[tag][word] = M[tag][word] / float(MOCCUR[tag])

    # Setting unassigned M to 0
    for tag in TAGS:

        if tag not in M:
            M[tag] = {}

        for word in WORDS:
            if word not in M[tag]:
                M[tag][word] = 0

def write_to_file(filename: str, testfile: str, output: List):
    """
    Write the generated pairs to file
    """
    file = open(os.path.join(OUTDIR, filename), "w")
    test = open(os.path.join(TESTDIR, testfile), "r")
    
    for sentence in output:
        for tag in sentence:
            s = "{} : {}\n".format(test.readline().strip(), tag.strip().upper())
            file.write(s)
    
    file.close()
    test.close()

################################################################
DICTIONARY = {}

def post():
    """
    Initialize fixed word-tag dictionary or append to existing
    """
    for file in os.listdir("./tags"):

        file = open("./tags/"+file, "rb")

        for line in file:
            try:
                line = line.decode()
            except:
                continue
            
            # Splitting into word-tag pair
            tokens = line.strip().split(' : ')

            if len(tokens) != 2:
                continue
            
            if tokens[1].strip().upper() not in TAGS:
                continue

            word = tokens[0].strip().lower()
            tag = tokens[1].strip().upper()
            
            # Update dictionary
            if word not in DICTIONARY:
                DICTIONARY[word] = set()
            
            DICTIONARY[word].add(tag)
        
        file.close()

################################################################
def prepare(filename):
    """
    Prepare the test data for processing via separating into sentences and words
    """
    f = open(os.path.join(TESTDIR, filename), "r")

    ret = []
    sentence = []

    for line in f:
        word = line.strip().lower()

        sentence.append(word)
        
        if word in PUN:
            ret.append(sentence)
            sentence = []
    
    if sentence != []:
        ret.append(sentence)
        sentence = []
        
    f.close()

    return ret

################################################################
def viterbi(E):
    # Viterbi probability tables
    prob = {}
    prev = {}

    # Initializing
    for i in range(len(E)):
        prob[i] = {}
        prev[i] = {}

    # Time Step 0
    T0 = SORTEDTAGS

    unknown = True
    
    if E[0] in WORDS:
        T0 = list(WORDTAG[E[0]])
        T0.sort()
        unknown = False

    if unknown:
        if E[0] in DICTIONARY.keys():
            T0 = list(DICTIONARY[E[0]])
            T0.sort()

    for tag in T0:
        if unknown:
            prob[0][tag] = I[tag]
        else:
            prob[0][tag] = I[tag] * M[tag][E[0]]

        prev[0][tag] = None

    # Time Step 1 to len(E) - 1
    # Loop over the evidence
    for i in range(1, len(E)):
        #Reset check
        nonzero = False

        # Tags
        T1 = SORTEDTAGS

        unknown1 = True
        if E[i] in WORDS:
            T1 = list(WORDTAG[E[i]])
            T1.sort()
            unknown1 = False
        
        if unknown1:
            if E[i] in DICTIONARY.keys():
                T1 = list(DICTIONARY[E[i]])
                T1.sort()

        T2 = list(prob[i-1].keys())
        T2.sort()

        # Loop over the potential tags
        for tag in T1:
            # Previous tag, Maximum probability
            maxp = 0
            previous = None

            # Iterate over all possible ptags
            for ptag in T2:
                # Calculate probability
                p = 0

                if unknown1:
                    p = prob[i-1][ptag] * T[ptag][tag] 
                else:
                    p = prob[i-1][ptag] * T[ptag][tag] * M[tag][E[i]]

                # Found new max, update
                if p >= maxp:
                    maxp = p
                    previous = ptag

            # Set the max probability for this tag in this timestep, record which tag was previous
            if(maxp != 0):
                nonzero = True

            prob[i][tag] = maxp
            prev[i][tag] = previous

        # Prevent 0 Chain
        if not nonzero:

            for tag in T1:
                maxp = 0
                previous = None
                for ptag in T2:
                    if unknown1:
                        p = prob[i-1][ptag]
                    else:
                        p = prob[i-1][ptag] * M[tag][E[i]]

                    if p >= maxp:
                        maxp = p
                        previous = ptag
                    
                if maxp != 0:
                    nonzero = True

                prob[i][tag] = maxp
                prev[i][tag] = previous

        # Prevent 0 Chain, Looser
        if not nonzero:

            for tag in T1:
                maxp = 0
                previous = None
                for ptag in T2:
                    if unknown1:
                        p = T[ptag][tag]
                    else:
                        p = T[ptag][tag]

                    if p >= maxp:
                        maxp = p
                        previous = ptag
                    
                if maxp != 0:
                    nonzero = True

                prob[i][tag] = maxp
                prev[i][tag] = previous
    

    return prob, prev

#################################################################
def debug(mode: str):

    if "I" in mode:
    # DEBUG I
        sum = 0
        for tag in TAGS:
            p = 0
            if tag in I:
                p = I[tag]
                sum += p
            print("Initial Probability for tag {} is {}".format(tag, p))
        print("Sum of all initial probabilities is {}".format(sum))

    if "T" in mode:
    # DEBUG T
        for ptag in TAGS:
            sum = 0
            for tag in TAGS:
                p = 0
                if ptag in T:
                    if tag in T[ptag]:
                        p = T[ptag][tag]
                        sum += p
                print("Transition Probability from {} to {} is {}".format(ptag, tag, p))
            print("Sum of all transition probabilities from {} is {}".format(ptag, sum))

    if "M" in mode:
    # DEBUG M
        for tag in TAGS:
            sum = 0
            for word in WORDS:
                p = 0
                if tag in M:
                    if word in M[tag]:
                        p = M[tag][word]
                        sum += p
                print("Observation Probability from {} to {} is {}".format(tag, word, p))
            print("Sum of all observation probabilities from {} is {}".format(tag, sum))  

#################################################################
def diff(input: str, output: str):
    left = open(os.path.join(TRAINDIR, input), "r")
    right = open(os.path.join(OUTDIR, output), "r")

    total = 0
    correct = 0

    notintrain = 0
    
    invalid = []
    for lline in left:
        rline = right.readline()

        total += 1

        tokens = lline.strip().split(' : ')
        word = tokens[0].strip().lower()

        if lline.strip() == rline.strip():
            correct += 1
        else:
            invalid.append("Expected: {} Actual: {} | Word in training? {}\n".format(lline.strip(), rline.strip(), word in WORDS))
            if word not in WORDS:
                notintrain += 1

    print("Accuracy: {}".format(correct/float(total)))

    print("Percent of incorrect cases not in training: {}".format(notintrain/float(total - correct)))

    file = open("diff.txt", "w")
    
    for inv in invalid:
        file.write(inv)
    
    file.close()
    left.close()
    right.close()


#################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--diff",
        type=str,
        required=False,
        help="Flag to enable diff output."
    )
    parser.add_argument(
        "--truth",
        type=str,
        required=False,
        help="The truth file."
    )
    parser.add_argument(
        "--trainingfiles",
        action="append",
        nargs="+",
        required=True,
        help="The training files."
    )
    parser.add_argument(
        "--testfile",
        type=str,
        required=True,
        help="One test file."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file."
    )

    args = parser.parse_args()

    diflag = False

    if args.diff is not None:
        if (args.diff.lower() == "true"):
            print("enable diff output? {}".format("TRUE"))
            diflag = True

            if args.truth is None:
                print("Truth file required for diff")
                exit()

        elif (args.diff.lower() == "false"):
            print("enable diff output? {}".format("FALSE"))

        else:
            print("Invalid --diff option")
            exit()

    if args.truth is not None:
        print("truth file is {}".format(args.truth))

    training_list = args.trainingfiles[0]
    print("training files are {}".format(training_list))

    print("test file is {}".format(args.testfile))

    print("output file is {}\n".format(args.outputfile))


    print("Training")
    start = time.time()
    tagging(training_list)
    end = time.time()
    print("Finished Training")
    print("Time elapsed: {}\n".format(end-start))

    print("Initializing dictionary")
    start = time.time()
    post()
    end = time.time()
    print("Initialized dictionary")
    print("Time elapsed: {}\n".format(end-start))

    print("Preparing Test Data")
    start = time.time()
    sentences = prepare(args.testfile)
    end = time.time()
    print("Test Data Prepared")
    print("Time elapsed: {}\n".format(end-start))

    print("Executing Viterbi")
    start = time.time()
    output = []

    # Deterministic
    SORTEDTAGS = list(TAGS)
    SORTEDTAGS.sort()
    SORTEDWORDS = list(WORDS)
    SORTEDWORDS.sort()

    for sentence in sentences:
        prob, prev = viterbi(sentence)

        tag = None
        maxp = 0

        last = list(prob[len(sentence) - 1].keys())
        last.sort()

        for ftag in last:
            p = prob[len(sentence) - 1][ftag]

            if p >= maxp:
                maxp = p
                tag = ftag

        rev = []

        for step in range(len(sentence) - 1, -1, -1):
            rev.append(tag)
            tag = prev[step][tag]

        rev.reverse()
        output.append(rev)

    end = time.time()
    print("Viterbi Executed")
    print("Time elapsed: {}\n".format(end-start))

    print("Writing to file")
    start = time.time()
    write_to_file(args.outputfile, args.testfile, output)
    end = time.time()
    print("Written to file")
    print("Time elapsed: {}\n".format(end-start))

    if diflag:
        print("Generating diff")
        diff(args.truth, args.outputfile)
