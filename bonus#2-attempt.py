#Written by Teresa Van
#10149274
#CPSC 501 Assignment #4
#Resources: https://docs.python.org/3.7/library/wave.html
#           https://github.com/scipy/scipy/blob/v1.0.0/scipy/signal/signaltools.py#L282-L416
#           https://docs.python.org/2/library/aifc.html
#           https://docs.python.org/2/library/sndhdr.html?highlight=snd#module-sndhdr
#Note: This program requires the installation of numpy and scipy in order to run properly

import aifc
import sndhdr
import wave
import sys
import collections
import itertools
import operator
import struct
import numpy
from scipy import signal
from scipy import fftpack

bitsize = 16
class FFTConvolve():
    #Read samples from a WAV file, return the samples and the parameters for the WAV file
    def LoadAiffSndFile(filename):
        aiffFile = aifc.openfp(filename, 'rb')

        #Read and store required data from the wav file
        numChannels = aiffFile.getnchannels()
        numFrames = aiffFile.getnframes()
        sampleWidth = aiffFile.getsampwidth()

        #Unpack samples by reading all frames from the .wav file (this assumes a 16-bit monophonic recording)
        frames = aiffFile.readframes(numFrames * numChannels)
        fmt = ("%i" % numFrames + "B") * numChannels
        samples = struct.unpack_from(fmt, frames)

        #Store parameters
        parameters = aiffFile.getparams()
        aiffFile.close()

        return samples, parameters

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
        print(parameters[4])
        wavFile.close()

        return samples, parameters

    #Write samples to WAV file into 16-bit monophonic format
    def SaveWaveFile(outputName, samples, parameters):
        wavFile = wave.openfp(outputName, 'wb')
        wavFile.setnchannels(parameters[0])
        wavFile.setsampwidth(parameters[1])
        wavFile.setframerate(parameters[2])
        wavFile.setnframes(parameters[3])
        wavFile.setcomptype('NONE', 'not compressed')

        #wavFile.setparams(parameters)
        data = bytearray()
        for info in samples:
            data.extend(struct.pack("h", int(info)))
        wavFile.writeframes(data)
        wavFile.close()

    #Convolve drying recording and impulse response using the FFT algorithm (sort of, I just used numpy's implementation of FFT)
    def FFTConvolve(x, h):
        #Convolve using the FFT algorithm
        x = numpy.array(x)
        h = numpy.array(h)
        if (x.ndim == 0 and h.ndim == 0): return x * h

        #Assuming we were given a complex result
        shapeX = numpy.array(x.shape)
        shapeH = numpy.array(h.shape)
        complexResult = (numpy.issubdtype(x.dtype, numpy.complexfloating))
        shape = shapeX + shapeH - 1

        #Pad to optimal size for faster FFT
        fourierShape = [fftpack.helper.next_fast_len(int(s)) for s in shape]
        fourierSlice = tuple(slice(0, int(s2)) for s2 in shape)

        #FFT routine with the help of numpy
        structPackX = numpy.fft.rfftn(x, fourierShape)
        structPackH = numpy.fft.rfftn(h, fourierShape)
        result = (numpy.fft.irfftn(structPackX * structPackH, fourierShape)[fourierSlice].copy())

        return result

    #Normalize the samples according to a 16-bit format
    #Required to pack shorts into struct, and extend to a bytearray
    def Normalize(samples, bitsize):
        maximum = max(abs(numpy.amax(samples)), abs(numpy.amin(samples)))
        samples = (samples / maximum * ((2**bitsize // 2) - 1))
        return samples

    #The main function of the program
    #Stores dry recording and impulse response from command line arguments
    #Convolves dry recording with impulse response and normalizes it according to a 16-bit size format
    #Writes the result to a .wav file
    def Main(dryRecording, impulseResponse, outputFile):
        #Read from dry recording and impulse response to get their samples and parameters
        (typ, sampling_rate, channels, frames, bits_per_sample) = sndhdr.what(dryRecording)
        print(typ)
        if typ == "aiff": (dryRecSamples, dryRecParams) = FFTConvolve.LoadAiffSndFile(dryRecording)
        else: (dryRecSamples, dryRecParams) = FFTConvolve.LoadWaveFile(dryRecording)

        (IRSamples, IRParams) = FFTConvolve.LoadWaveFile(impulseResponse)

        #Convert to a numpy array for easier manipulation
        dryRecArray = numpy.array(dryRecSamples)
        IRArray = numpy.array(IRSamples)

        #Convolve the dry recording with the impulse response and normalize the result
        result = FFTConvolve.FFTConvolve(dryRecArray, IRArray)
        result = FFTConvolve.Normalize(result, bitsize)

        #Write the result to a new .wav file
        FFTConvolve.SaveWaveFile(outputFile, result, dryRecParams)

if __name__ == '__main__':
    #Store command line arguments
    dryRecording = sys.argv[1]
    impulseResponse = sys.argv[2]
    outputFile = sys.argv[3]
    FFTConvolve.Main(dryRecording, impulseResponse, outputFile)
