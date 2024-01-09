import os
TYPES = ['aca', 'dem', 'fic', 'news']
TAGS = set(["AJ0", "AJC", "AJS", "AT0", "AV0", "AVP", "AVQ", "CJC", "CJS", "CJT", "CRD",
        "DPS", "DT0", "DTQ", "EX0", "ITJ", "NN0", "NN1", "NN2", "NP0", "ORD", "PNI",
        "PNP", "PNQ", "PNX", "POS", "PRF", "PRP", "PUL", "PUN", "PUQ", "PUR", "TO0",
        "UNC", 'VBB', 'VBD', 'VBG', 'VBI', 'VBN', 'VBZ', 'VDB', 'VDD', 'VDG', 'VDI',
        'VDN', 'VDZ', 'VHB', 'VHD', 'VHG', 'VHI', 'VHN', 'VHZ', 'VM0', 'VVB', 'VVD',
        'VVG', 'VVI', 'VVN', 'VVZ', 'XX0', 'ZZ0', 'AJ0-AV0', 'AJ0-VVN', 'AJ0-VVD',
        'AJ0-NN1', 'AJ0-VVG', 'AVP-PRP', 'AVQ-CJS', 'CJS-PRP', 'CJT-DT0', 'CRD-PNI', 'NN1-NP0', 'NN1-VVB',
        'NN1-VVG', 'NN2-VVZ', 'VVD-VVN', 'AV0-AJ0', 'VVN-AJ0', 'VVD-AJ0', 'NN1-AJ0', 'VVG-AJ0', 'PRP-AVP',
        'CJS-AVQ', 'PRP-CJS', 'DT0-CJT', 'PNI-CRD', 'NP0-NN1', 'VVB-NN1', 'VVG-NN1', 'VVZ-NN2', 'VVN-VVD'])

if __name__ == '__main__':
    TAGWORD = {}

    for type in TYPES:
        for filename in os.listdir("training/"+type):
            file = open("./training/"+type+"/" + filename , "r")

            for line in file:
                tokens = line.strip().split(' : ')
                
                if(len(tokens) != 2):
                    continue
                
                if tokens[1].strip().upper() not in TAGS:
                    continue

                word = tokens[0].strip().lower()
                tag = tokens[1].strip().upper()

                if tag not in TAGWORD:
                    TAGWORD[tag] = set()

                TAGWORD[tag].add(word)

    for tag in TAGWORD.keys():
        f = open("./tags/"+tag+".txt", "w")
        for word in TAGWORD[tag]:
            f.write("{} : {}\n".format(word, tag))


