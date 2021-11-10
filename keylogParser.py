import statistics as stat
import matplotlib.pyplot as plt

bigrams = ['th', 'he', 'gh', 'nd', 'ne', 'in', 'er', 'an', 'ng', 'me', 'we', 'is'
			'at', 'on', 'es', 'ay', 'or', 'hi']
currentUser = 'oskar'

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
		self.present_bigrams = []
		self.std_devs = []
		self.means = []
		self.variances = []
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
	def get_pressed_data_diffs(self, vector):
		pressed = list(filter(filter_pressed, vector))
		return self.generate_bigram_diffs_array(pressed)

	#calculates the stats and prints them
	def get_stats(self, results):
		std_devs = []
		means = []
		variances = []
		present_bigrams = []
		for bigram in self.bigrams:
			if (bigram in results and len(results[bigram]) > 1):

				std_devs.append(float(stat.stdev(results[bigram])))
				means.append(float(stat.mean(results[bigram])))
				variances.append(float(stat.variance(results[bigram])))
				present_bigrams.append(bigram)

		return {
			'std_devs': std_devs,
			'means': means,
			'variances': variances,
			'present_bigrams': present_bigrams
		}

	def print_graph(self, to_be_named):
		stats = to_be_named['oskar']
		x = stats['present_bigrams']
		y_std_dev = stats['std_devs']
		y_mean = stats['means']
		y_var = stats['variances']

		#graph showing all stats measures
		plt.plot(x, y_std_dev, label = "Standard Deviation")
		plt.plot(x, y_mean, label = "Mean")
		plt.plot(x, y_var, label = "Variance")
		plt.xlabel('bigrams')
		plt.title('Statisics of bigrams')
		plt.show()

		#individual graphs
		self.make_graph(x, y_std_dev, 'Standard deviation of bigrams')
		self.make_graph(x, y_mean, 'Means of bigrams')
		self.make_graph(x, y_var, 'Variance of bigrams')


	## Just printing the results
	def print_results(self):
		print(self.results)
		print(self.std_devs)
		print(self.means)
		print(self.variances)

	def make_graph(self,x,y,title):
		plt.plot(x,y)
		plt.title(title)
		plt.show()


if __name__ == "__main__":
	keylogsParser = KeylogsParser(bigrams, f"keylogs/{currentUser}.txt")
	keylogsParser.get_pressed_data_diffs()
	keylogsParser.print_results()
	keylogsParser.get_stats()
	keylogsParser.print_graph()
