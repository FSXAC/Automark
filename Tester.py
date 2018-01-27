"""This is used to generate random submissions and test Automark"""

import os
import shutil
import random
import string

WRITE_INFO = False
TESTDIR = './Tests/'
DELETE_FILES = True
SUMMARY = True
# LETTERS = 'abcdefghijklmnnopqrstuvwxyz'
LETTERS = 'x'
N = 20

def generateID():
    # return str(random.randint(10000000, 99999999))
    return '12345678'

def generateCSID():
    csid = ''
    for j in range(5):
        if j % 2 == 0:
            csid += random.choice(LETTERS)
        else:
            csid += str(random.randint(0, 9))
    return 'student_' + csid

def generateName():
    firstName = random.choice([
        # 'Abi', 'Braden', 'Cindy', 'David', 'Eleven', 'Finn',
        # 'Greg', 'Hillary', 'Ivy', 'Jacob', 'Kyle', 'Liam', 'Michael',
        # 'Noah', 'Opera', 'Pearl', 'Qing', 'Reese', 'Stanley', 'Thomas',
        # 'Victor', 'Wang', 'Xing', 'Yorkie', 'Zhang'
        'Derek'
    ])
    lastName = random.choice([
        # 'Alexander', 'Bitcon', 'Conbace', 'Deng', 'Feng', 'Genning', 'Henning',
        # 'Irving', 'Jackson', 'Koerner', 'Lincoln', 'Moira', 'Nassal', 'Olafmeister',
        # 'Pawleski', 'Quan', 'Romeo', 'Sombra', 'Tokyo', 'Unibaba', 'Volkov', 'Wang',
        # 'Xuan', 'Yaun', 'Zhang'
        'Bitcoin'
    ])
    return firstName + ' ' + lastName

def generateDateForm():
    df = random.choice([
        '2017 01 15', '2017-01-15', '01-15-2017', 'Jan 15 2017',
        'Jan 15, 2017', 'Jan-15, 2017', '2017 Jan 15', '2017-Jan-15'
    ])
    return df

def generateCFile():
    code = """/*
 * Author: """ + generateName() + """
 * Student Number: """ + generateID() + """
 * Lab Section: L2L
 * Date: 2017 01 15
 * Purpose: Prompts the user for his/her name and prints
 * a welcome message on the screen.
 */

#include <stdio.h>
#include <stdlib.h>

#define _CRT_SECURE_NO_WARNINGS

/* Constants */
#define MAX_NAME_LENGTH 100

int main(void) {
    char name[MAX_NAME_LENGTH];

    printf("Please enter your first name: ");
    scanf("%s", name);
    printf("\\nHello, %s, welcome to APSC 160!\\n\\n", name);

    system("PAUSE");
    return 0;
}"""
    return code

def generateReadme():
    return 'Empty'


def writeSummary():
    if WRITE_INFO:
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
