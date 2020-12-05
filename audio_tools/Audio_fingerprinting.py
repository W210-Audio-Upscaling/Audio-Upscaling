#!/usr/bin/env python
# coding: utf-8

from ffmpy import FFmpeg
import matplotlib.pyplot as plt
import librosa
from librosa import display as ld
import numpy as np


def framing(sig, fs=48000, win_len=0.37, win_hop=0.02):
    """
    transform a signal into a series of overlapping frames.

    Args:
         sig            (array) : a mono audio signal (Nx1) from which to compute features.
         fs               (int) : the sampling frequency of the signal we are working with.
         win_len        (float) : window length in sec.
                                  Default is 0.37.
         win_hop        (float) : step between successive windows in sec.
                                  Default is 0.02.
    Returns:
         array of frames.
         frame length.
    """
    # compute frame length and frame step (convert from seconds to samples)
    frame_length = win_len * fs
    frame_step = win_hop * fs
    signal_length = len(sig)
    frames_overlap = frame_length - frame_step

    # Make sure that we have at least 1 frame+
    num_frames = np.abs(signal_length - frames_overlap) // np.abs(frame_length - frames_overlap)
    rest_samples = np.abs(signal_length - frames_overlap) % np.abs(frame_length - frames_overlap)

    # Pad Signal to make sure that all frames have equal number of samples
    # without truncating any samples from the original signal
    if rest_samples != 0:
        pad_signal_length = int(frame_step - rest_samples)
        z = np.zeros((pad_signal_length))
        pad_signal = np.append(sig, z)
        num_frames += 1
    else:
        pad_signal = sig

    # make sure to use integers as indices
    frame_length = int(frame_length)
    frame_step = int(frame_step)
    num_frames = int(num_frames)

     # compute indices
    idx1 = np.tile(np.arange(0, frame_length), (num_frames, 1))
    idx2 = np.tile(np.arange(0, num_frames * frame_step, frame_step),
                    (frame_length, 1)).T
    indices = idx1 + idx2
    frames = pad_signal[indices.astype(np.int32, copy=False)]
    return frames
    
def fingerprint(x,sr):
    frames=framing(x,sr)
    E=np.zeros((len(frames),1025))
    for i in range(len(frames)):
        X = librosa.stft(frames[i])
        Xdb = librosa.amplitude_to_db(abs(X))
        for j in range(len(Xdb)):
            E[i][j]=sum([x*2 for x in Xdb[j]])
    diff=np.zeros(E.shape)
    bit_matrix=np.zeros(E.shape)
    for i in range(len(E)):
        for j in range(len(E[i])):
            if i>0 and j <len(E[i])-1:
                diff[i][j] = E[i][j]-E[i][j+1] - (E[i-1][j]-E[i-1][j+1])
                if diff[i][j]>0:
                    bit_matrix[i][j]=1
                else:
                    bit_matrix[i][j]=0
    return bit_matrix

def plot_fingerprint(fingerprint):
    plt.imshow(fingerprint, cmap='Greys',  interpolation='nearest')
    plt.show()

def bit_error_rate(audio_1,audio_2,sampling_rate):
    x1, sr1 = librosa.load(audio_1, sr=sampling_rate)
    x2, sr2 = librosa.load(audio_2, sr=sampling_rate)
    
    fingerprint_1=fingerprint(x1,sr1)
    print("-"*100)
    print("Fingerprint plot for %s" %(audio_1))
    plot_fingerprint(fingerprint_1)
    print("-"*100)
    
    fingerprint_2=fingerprint(x2,sr2)
    print("Fingerprint plot for %s" %(audio_2))
    plot_fingerprint(fingerprint_2)
    print("-"*100)
    
    BER=np.sum(fingerprint_1!=fingerprint_2)/fingerprint_1.size
    print("Bit Error rate:",BER)




