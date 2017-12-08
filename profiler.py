#Written by Teresa Van
#10149274
#CPSC 501 Assignment #4
#Resources: https://pymotw.com/2/profile/
#USAGE: python3 profiler.py [ProfileFFT or ProfileConvolve] dryrecording.wav impulseresponse.wav output.wav 

import cProfile
import sys
from convolve import Convolve
from version6 import FFTConvolve

def ProfileConvolve():
    cProfile.run("Convolve.Main(dryRecording, impulseResponse, outputFile)")

def ProfileFFT():
    cProfile.run("FFTConvolve.Main(dryRecording, impulseResponse, outputFile)")

if __name__ == '__main__':
    version = sys.argv[1]
    dryRecording = sys.argv[2]
    impulseResponse = sys.argv[3]
    outputFile = sys.argv[4]
    if version == "ProfileFFT": ProfileFFT()
    else: ProfileConvolve()
