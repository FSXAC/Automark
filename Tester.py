"""This is used to generate random submissions and test Automark"""

import os
import shutil
import random
import string

TESTDIR = './Tests/'
DELETE_FILES = True
SUMMARY = True
LETTERS = 'abcdefghijklmnnopqrstuvwxyz'
N = 10

def generateID():
    return(random.randint(10000000, 99999999))

def generateCSID():
    csid = ''
    for j in range(5):
        if j % 2 == 0:
            csid += random.choice(LETTERS)
        else:
            csid += str(random.randint(0, 9))
    return csid

def generateName():
    return 'Muchen He'

def generateCFile():
    code = """
#include <stdio.h>
#include <stdlib.h>

#define _CRT_SECURE_NO_WARNINGS

#define N 4

int main(void) {
    printf("%d %d %d\\n", N, 3, 2);
    system("PAUSE");
    return 0;
}
    """
    return code

def generateReadme():
    return 'Empty'


def writeSummary():
    f = open(TESTDIR + csID + '.txt', 'w')
    f.write(generateReadme())
    f.close()

    f = open(TESTDIR + csID + '.c', 'w')
    f.write(generateCFile())
    f.close()

# First remove everything
if DELETE_FILES:
    for file in os.listdir(TESTDIR):
        filePath = os.path.join(TESTDIR, file)
        try:
            if os.path.isfile(filePath):
                os.unlink(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        except Exception as e:
            print(e)

# Now generate random samples
for i in range(N):
    studentID = generateID()
    csID = generateCSID()
    name = generateName()

    if SUMMARY:
        writeSummary()
