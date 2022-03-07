import librosa
import os
import numpy as np

# Get MP3s from file
files = os.listdir("Audio_Files/Audio")

# Load an audio file
y, sr = librosa.load(f"Audio_Files/Audio/{files[0]}")

# Mel-Frequency Cepstral Coefficient
mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
print(mfcc)

# Short-Time Fourier Transform
stft = np.abs(librosa.stft(y))
print(stft)

# Chromagram
chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)
print(chroma)

# Spectral Contrast
cont = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sr).T, axis=0)
print(cont)

# Tonal Centroid Features
tone = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
print(tone)
