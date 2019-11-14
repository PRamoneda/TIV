import librosa
import numpy
import numpy as np
import sys
import math

from musthe import Note

import TIVlib as tiv
import musthe

from essentia.standard import MonoLoader, Windowing, Spectrum, SpectralPeaks, FrameGenerator, HPCP, ConstantQ, \
	Chromagram


def save_tonnetz(centroids):
	with open('centroids.txt', 'w') as f:
		for j in range(0, centroids.shape[1]):
			for i in range(0, centroids.shape[0]):
				f.write("%s\t" % centroids[i][j])
			f.write("\n")


def hcdf(centroids, rate_centroids_second):
	ans = [0]
	for j in range(1, centroids.shape[1] - 1):
		sum = 0
		for i in range(0, centroids.shape[0]):
			sum += (centroids[i][j + 1] - centroids[i][j - 1]) ** 2
		sum = math.sqrt(sum)
		if sum > 0.2:
			print("harmonic change at second", j/rate_centroids_second)
		ans.append(sum)
	ans.append(0)
	return numpy.array(ans)


def save_hcdf(vector):
	with open('hcdf.txt', 'w') as f:
		for s in vector:
			f.write("%s\n" % s)


def centroids_second(src, y, centroids):
	return src * centroids.shape[1] / y.shape[0]


def harmonic_change(filename):
	y, sr = librosa.load(filename, sr=44100)
	y = librosa.effects.harmonic(y)
	tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
	save_tonnetz(tonnetz)
	rate_centroids_second = centroids_second(sr, y, tonnetz)
	vector = hcdf(tonnetz, rate_centroids_second)
	save_hcdf(vector)


def main():
	# Reference: CMaj chord
	please = "./audio_files/please.flac"
	# Consonant chords: GMaj, Amin
	secret = "./audio_files/secret.flac"

	# Calculate the HPCP for each of the chords
	harmonic_change(please)


if __name__ == '__main__':
	main()
