# Requirements
- [Python](https://www.python.org/)

# Execution

The program can be executed via the command line as:  
`python tagger.py`  
  
With the following required options in order:
1. `--diff`: **OPTIONAL** True if you want the program to output an additional file containing the words that were tagged incorrectly alongside their correct tagging. Also includes accuracy and other statistics

2. `--truth`: **OPTIONAL** Required if --diff is True. The name of the file to be used as the source of correct tagging for the comparision. The file must be located in ./training or whichever folder specified via the TRAINDIR constant

3. `--trainingfiles`: A list of the names of the files to be used for training. All files must be located in ./training or whichever folder specified via the TRAINDIR constant

4. `--testfile`: The name of the file to be used for testing (that is, the file to be tagged). The file must be located in ./testing or whichever folder specified via the TESTDIR constant

5. `--outputfile`: The name of the file to be used for the output of the algorithm. The file will be located in ./output or whichever folder specified via the OUTDIR constant

Examples:
- `python tagger.py --diff true --truth FPB.txt --trainingfiles FPB.txt --testfile FPB.txt --outputfile output.txt`

- `python tagger.py --trainingfiles FPB.txt --testfile FPB.txt --outputfile output.txt`

- `python tagger.py --diff true --truth G0L.txt --trainingfiles FPB.txt G0S.txt --testfile G0L.txt --outputfile output.txt`

# Format
A training file is a file the program will use to train its model via extracting information such as the tags associated with the word, its position, etc.  

It will contain words and tags in the format:  

**WORD : TAG**  
**WORD : TAG**  
**WORD : TAG**  
**...**

A testing file is a file the program will use to test its model via giving the word the tag it deduces is most appropriate.  

It will contain only words separated by lines:  

**WORD**  
**WORD**  
**WORD**  
**...**

If a training file is called ABX, then a test file called ABX must be ABX minus the tags. That is, they are the same file, just with one having the tags removed.  

This is so ABX can be used as the truth file when testing.  

Three examples to demonstrate this format have been included.