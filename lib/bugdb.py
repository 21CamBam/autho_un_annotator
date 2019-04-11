#!/usr/bin/python3

import subprocess
import sys

def main(args):
    out = subprocess.Popen(['mysql', '-D','bugs42','-u','kawale','-peng-reports','-h','eng-sea-bugsDB02.west.isilon.com','-e',args[0]], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    stdout = stdout.replace("\\n", "\n")
    print(stdout)
    return 0;

if __name__ == "__main__":
   main(sys.argv[1:])
