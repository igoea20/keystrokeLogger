import statistics as stat

bigrams = ['th', 'he', 'gh', 'nd', 'ne', 'in', 'er', 'an', 'ng', 'me', 'we', 'is'
			'at', 'on', 'es', 'ay', 'or', 'hi']
currentUser = 'aoife'

def filter_pressed(line):
	letter, timestamp, strokeType = line.split(' ')
	if (strokeType.strip() == 'Pressed'):
		return True
	else:
		return False
class KeylogsParser:
	def __init__(self, bigrams, file_name):
		self.bigrams = bigrams
		self.file_name = file_name
		self.results = {}

	## takes a file and returns array seperated by linebreak
	def read_file(self):
		with open(self.file_name) as f:
			lines = f.readlines()

			return lines

	## generates object with timestamp diffs for given input array
	def generate_bigram_diffs_array(self, inputs):
		output = {}
		for idx in range(len(inputs)):
			if (idx < len(inputs) - 1):
				line = inputs[idx]
				nxtLine = inputs[idx + 1]
				# crt = current, nxt = next
				crtLetter, crtTimestamp, _ = line.split(' ')
				nxtLetter, nxtTimestamp, _ = nxtLine.split(' ')
				for bg in self.bigrams:
					if (crtLetter + nxtLetter == bg):
						if (bg in output):
							output[bg].append(float(nxtTimestamp) - float(crtTimestamp))
						else:
							output[bg] = [float(nxtTimestamp) - float(crtTimestamp)]
		return output


	## compute timestamp diffs between pressed and set self.results
	def get_pressed_data_diffs(self):
		lines = self.read_file()
		pressed = list(filter(filter_pressed, lines))
		self.results = self.generate_bigram_diffs_array(pressed)

	## print standard deviation for everything in self.results
	## remember that at least two occurances of a bigram is required to compute standard deviation
	def get_sigma(self):
		for bigram in self.bigrams:
			if (bigram in self.results and len(self.results[bigram]) > 1):
				print(bigram + ' ' + str(stat.stdev(self.results[bigram])))

	## print mean for each bigram that exists
	def get_mean(self):
		for bigram in self.bigrams:
			if (bigram in self.results):
				print(bigram + ' ' + str(stat.mean(self.results[bigram])))

	## Just printing the results
	def print_results(self):
		print(self.results)



if __name__ == "__main__":
	keylogsParser = KeylogsParser(bigrams, f"keylogs/{currentUser}.txt")
	keylogsParser.get_pressed_data_diffs()
	keylogsParser.print_results()
	keylogsParser.get_mean()
