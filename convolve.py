#Written by Teresa Van
#10149274
#CPSC 501 Assignment #4
#Resources: https://docs.python.org/3.7/library/wave.html
#           https://github.com/numpy/numpy/blob/v1.13.0/numpy/core/numeric.py#L978-L1073
#Note: This program requires the installation of numpy and scipy in order to run properly

import wave
import sys
import collections
import itertools
import operator
import struct
import numpy

class Convolve():
    #Read samples from a WAV file, return the samples and the parameters for the WAV file
    def LoadWaveFile(filename):
        wavFile = wave.openfp(filename, 'rb')

        #Read and store required data from the wav file
        numChannels = wavFile.getnchannels()
        numFrames = wavFile.getnframes()
        sampleWidth = wavFile.getsampwidth()

        #Unpack samples by reading all frames from the .wav file (this assumes a 16-bit monophonic recording)
        frames = wavFile.readframes(numFrames * numChannels)
        fmt = ("%i" % numFrames + "h") * numChannels
        samples = struct.unpack_from(fmt, frames)

        #Store parameters
        parameters = wavFile.getparams()
        wavFile.close()

        return samples, parameters

    #Write samples to WAV file into 16-bit monophonic format
    def SaveWaveFile(outputName, samples, parameters):
        wavFile = wave.openfp(outputName, 'wb')
        wavFile.setparams(parameters)
        data = bytearray()
        for info in samples:
            data.extend(struct.pack("h", int(info)))
        wavFile.writeframes(data)
        wavFile.close()

    #Convolve using the input side algorithm
    #Loop through samples in signal x, and multiply it with signal h. (Add the result to signal y starting at incrementing positions)
    def Convolve(x, h):
        y = numpy.zeros(x.size + h.size)
        acc = 0
        for sample in x:
            y[acc : acc + h.size] += sample * h
            acc += 1
        return y

    #Normalize the samples according to a 16-bit format
    #Required to pack shorts into struct, and extend to a bytearray
    def Normalize(samples, bitsize):
        if abs(numpy.amax(samples)) > abs(numpy.amin(samples)): maximum = abs(numpy.amax(samples))
        else: maximum = abs(numpy.amin(samples))

        temp = 0

        for i in range(((2**bitsize // 2) - 1)):
            temp += (samples / maximum)

        samples = temp
        return samples

    #The main function of the program
    #Stores dry recording and impulse response from command line arguments
    #Convolves dry recording with impulse response and normalizes it according to a 16-bit size format
    #Writes the result to a .wav file
    def Main(dryRecording, impulseResponse, outputFile):
        bitsize = 16

        #Read from dry recording and impulse response to get their samples and parameters
        (dryRecSamples, dryRecParams) = Convolve.LoadWaveFile(dryRecording)
        (IRSamples, IRParams) = Convolve.LoadWaveFile(impulseResponse)

        #Convert to a numpy array for easier manipulation
        dryRecArray = numpy.array(dryRecSamples)
        IRArray = numpy.array(IRSamples)

        #Convolve the dry recording with the impulse response and normalize the result
        result = Convolve.Convolve(dryRecArray, IRArray)
        result = Convolve.Normalize(result, bitsize)

        #Write the result to a new .wav file
        Convolve.SaveWaveFile(outputFile, result, dryRecParams)

if __name__ == '__main__':
    #Store command line arguments
    dryRecording = sys.argv[1]
    impulseResponse = sys.argv[2]
    outputFile = sys.argv[3]
    Convolve.Main(dryRecording, impulseResponse, outputFile)
