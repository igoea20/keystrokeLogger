import statistics as stat

bigrams = ['th', 'he', 'gh']

class KeylogsParser:
	def __init__(self, bigrams, file_name):
		self.bigrams = bigrams
		self.file_name = file_name
		self.results = {}

	def read_file(self):
		with open(self.file_name) as f:
			lines = f.readlines()
			for idx in range(len(lines)):
				if (idx < len(lines) - 1):
					line = lines[idx]
					nxtLine = lines[idx + 1]
					# crt = current, nxt = next
					crtLetter, crtTimestamp, _ = line.split(' ')
					nxtLetter, nxtTimestamp, _ = nxtLine.split(' ')
					for bg in self.bigrams:
						if (crtLetter + nxtLetter == bg):
							if (bg in self.results):
								self.results[bg].append(float(nxtTimestamp) - float(crtTimestamp))
							else:
								self.results[bg] = [float(nxtTimestamp) - float(crtTimestamp)]

			print(self.results)

	def get_sigma(self):
		for bigram in self.bigrams:
			result = self.results[bigram]
			if (len(result) > 1):
				print(bigram + ' ' + str(stat.stdev(self.results[bigram])))





if __name__ == "__main__":
	keylogsParser = KeylogsParser(bigrams, "keylog.txt")
	keylogsParser.read_file()
	keylogsParser.get_sigma()