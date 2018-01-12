import subprocess
import os
import shutil

testdir = './Tests/'
tempdir = './temp/'

def readOutput(f):
    # Make temporary directory
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    # remove system pause
    # tf = open(f, 'r')
    # lines = tf.readlines()
    # tf.close()
    # tf = open(f, 'w')
    # for line in lines:
    #     if 'system("PAUSE");' not in line:
    #         tf.write(line)
    # tf.close()

    subprocess.run('gcc ' + f + ' -o ./temp/out.exe')

    # Method 1: (will have to remove all the 'system pause')
    # result = subprocess.run('a.exe', stdout=subprocess.PIPE, input='\n'.encode('utf-8'))
    # result = subprocess.run('a.exe', input='\n'.encode('utf-8'))
    # result = subprocess.run('temp\\out.exe', input='\n'.encode('utf-8'), shell=True)
    # print(result)

    # Method 2:
    # process = subprocess.Popen(['a.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    # process.communicate(input='\n')

    # Method 2 Attemp 2:
    # process = subprocess.Popen(
    #     ['temp\\out.exe'],
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE
    # )
    # inputdata = "Muchen\n".encode('utf-8')
    # stdoutdata, stderrdata = process.communicate(input=inputdata)
    # stdoutdata = str(stdoutdata)
    # stdoutdata = stdoutdata.replace('b\'', '')
    # stdoutdata = stdoutdata.replace('\\r\\n', '\r\n')
    # print(stdoutdata)

    # Method 3
    # os.system('temp\\out.exe')

    # Method 4
    rc = subprocess.call('start temp\\out.exe', shell=True)

    # Delete the temorary folder
    shutil.rmtree(tempdir)

for file in os.listdir(testdir):
    fname, fext = os.path.splitext(file)
    if fext == '.c':
        readOutput(testdir + fname + fext)
        break
