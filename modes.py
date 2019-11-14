class HarmonicFunction:
	key_labels = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'E#': 5, 'Fb': 4, 'F': 5, 'F#': 6, 'Gb': 6,
	              'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, 'B#': 12, 'Cb': 11}

	def __init__(self, tonica):
		self.tonica = HarmonicFunction.key_labels[tonica]

	def getKey(self):
		for notation, num in HarmonicFunction.key_labels.items():
			if num == self.tonica:
				print(notation)

	def get(self, chord):
		return (HarmonicFunction.key_labels[chord] - self.tonica) % 12
