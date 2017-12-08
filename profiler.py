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
