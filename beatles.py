import numpy as np
import sys
import TIVlib as tiv

from essentia.standard import MonoLoader, Windowing, Spectrum, SpectralPeaks, FrameGenerator, HPCP, ConstantQ, \
	Chromagram, SingleGaussian


def file_to_hpcp(filename):
	audio = MonoLoader(filename=filename)()
	windowing = Windowing(type='blackmanharris62')
	spectrum = Spectrum()
	spectral_peaks = SpectralPeaks(orderBy='magnitude',
	                               magnitudeThreshold=0.001,
	                               maxPeaks=20,
	                               minFrequency=20,
	                               maxFrequency=8000)
	hpcp = HPCP(maxFrequency=8000)  # ,
	# normalized='unitSum') #VERIFICAR QUE ISTO E O Q FAZ SENTIDO FAZER

	spec_group = []
	hpcp_group = []

	for frame in FrameGenerator(audio, frameSize=1024, hopSize=512):
		windowed = windowing(frame)
		fft = spectrum(windowed)
		frequencies, magnitudes = spectral_peaks(fft)
		final_hpcp = hpcp(frequencies, magnitudes)

		spec_group.append(fft)
		hpcp_group.append(final_hpcp)

	mean_hpcp = np.mean(np.array(hpcp_group).T, axis=1)
	return mean_hpcp


import librosa


def file_to_chroma(filename):
	audio = librosa.core.load(filename)
	chromagram = librosa.feature.chroma_stft(audio)
	print(chromagram)
	mean_chromagram = np.mean(chromagram, axis=0)
	return mean_chromagram


def hcdf(filename):
	audio = MonoLoader(filename=filename)()
	windowing = Windowing(type='hann')

	for frame in FrameGenerator(audio, frameSize=32768, hopSize=4096):
		windowed = windowing(frame)
		print('window', windowed)
		# ConstantQ transform
		# constant_q = ConstantQ(binsPerOctave=36, minFrequency=110, maxFrequency=3520, sampleRate=11025)
		# kk = constant_q(windowed)
		# 12 bin tunned Chromagram
		# pedirle al ruso que lo ponga
		chroma = Chromagram(numberBins=12, binsPerOctave=36, minFrequency=110, windowType='hann') # maxFrequency=3520

		pitch_class_vectors = chroma(frame)
		print('pitch_class_vectors', pitch_class_vectors)


# Tonal centroid transform

# Smoothing and Dostance calculation


def main():
	# Reference: CMaj chord
	please = "./audio_files/please.flac"
	# Consonant chords: GMaj, Amin
	secret = "./audio_files/secret.flac"

	# Calculate the HPCP for each of the chords
	hcdf(please)



if __name__ == '__main__':
	main()
