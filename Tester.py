"""This is used to generate random submissions and test Automark"""

import os
import shutil
import random
import string

TESTDIR = './Tests'
DELETE_FILES = False
N = 3

def generateID():
    return(random.randint(10000000, 99999999))

def generateCSID():
    csid = ''
    for j in range(5):
        if i % 2 == 0:
            csid += random.choice(string.ascii_lowercase)
        else:
            csid += str(random.randint(0, 9))
    return csid

def generateName():
    return 'Muchen He'

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
    cdID = generateCSID()
    name = generateName()
    print(cdID)
