import statistics as stat
import matplotlib.pyplot as plt

bigrams = ['th', 'he', 'gh', 'nd', 'ne', 'in', 'er', 'an', 'ng', 'me', 'we', 'is'
			'at', 'on', 'es', 'ay', 'or', 'hi']
currentUser = 'johan'

class KeylogsParser:
	def __init__(self, bigrams, file_name):
		self.bigrams = bigrams
		self.file_name = file_name
		self.present_bigrams = []
		self.std_devs = []
		self.means = []
		self.variances = []
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

	def get_stddev(self, bigram):
		stddev = stat.stdev(self.results[bigram])
		print('"' + bigram + '" standard deviation: ' + str(stddev))
		return stddev

	def get_mean(self, bigram):
		mean = stat.mean(self.results[bigram])
		print('"' + bigram + '" mean: ' + str(mean))
		return mean

	def get_variance(self, bigram):
		var = stat.variance(self.results[bigram])
		print('"' + bigram + '" variance: ' + str(var))
		return var

	#calculates the stats and prints them
	def get_stats(self):
		for bigram in self.bigrams:
			if (bigram in self.results and len(self.results[bigram]) > 1):
				self.std_devs.append(float(keylogsParser.get_stddev(bigram)))
				self.means.append(float(keylogsParser.get_mean(bigram)))
				self.variances.append(float(keylogsParser.get_variance(bigram)))
				self.present_bigrams.append(bigram)
		print(self.std_devs)
		print(self.means)
		print(self.variances)

	def print_graph(self):
		x = self.present_bigrams
		y_std_dev = self.std_devs
		y_mean = self.means
		y_var = self.variances

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




	def make_graph(self,x,y,title):
		plt.plot(x,y)
		plt.title(title)
		plt.show()


if __name__ == "__main__":
	keylogsParser = KeylogsParser(bigrams, f"keylogs/{currentUser}.txt")
	keylogsParser.read_file()
	keylogsParser.get_stats()
	keylogsParser.print_graph()
