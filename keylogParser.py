import statistics as stat
import matplotlib.pyplot as plt

bigrams = ['th', 'he', 'gh', 'nd', 'ne', 'in', 'er', 'an', 'ng', 'me', 'we', 'is'
			'at', 'on', 'es', 'ay', 'or', 'hi']

def filter_pressed(line):
	letter, timestamp, strokeType = line.split(' ')
	if (strokeType.strip() == 'Pressed'):
		return True
	else:
		return False

def read_file(user):
		with open(f"keylogs/{user}.txt") as f:
			lines = f.readlines()
			return lines

def is_valid(diff):
	if (diff > 4):
		return False
	else:
		return True

class KeylogsParser:
	def __init__(self, bigrams):
		self.bigrams = bigrams

	## takes a file and returns array seperated by linebreak

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
					diff = float(nxtTimestamp) - float(crtTimestamp)
					if (crtLetter + nxtLetter == bg and is_valid(diff)):
						if (bg in output):
							output[bg].append(diff)
						else:
							output[bg] = [diff]
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

	def print_graph(self, stats):
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
