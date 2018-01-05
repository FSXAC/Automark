import subprocess
import os
import shutil

testdir = './Tests/'
tempdir = './temp/'

def readOutput(f):
    # Make temporary directory
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    subprocess.run('gcc ' + f + ' -o ./temp/out.exe')

    # Method 1: (will have to remove all the 'system pause')
    # result = subprocess.run('a.exe', stdout=subprocess.PIPE, input='\n'.encode('utf-8'))
    # result = subprocess.run('a.exe', input='\n'.encode('utf-8'))
    result = subprocess.run('temp\\out.exe', input='\n'.encode('utf-8'), shell=True)

    # Method 2:
    # process = subprocess.Popen(['a.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    # process.communicate(input='\n')

    print(result)

    # Delete the temorary folder
    shutil.rmtree(tempdir)

for file in os.listdir(testdir):
    fname, fext = os.path.splitext(file)
    if fext == '.c':
        readOutput(testdir + fname + fext)
        break
