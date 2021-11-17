import matplotlib.pyplot as plt
import statistics as stat
from collections import Counter
import numpy as np

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

def mse(Y_true, T_pred):
	return np.square(np.subtract(Y_true, T_pred)).mean()


def is_valid(diff):
	if (diff > 4):
		return False
	else:
		return True

def store_user_results(user, stats):
	results = {}
	lines = read_file(user)
	results[user] = parser.get_pressed_data_diffs(lines)
	stats[user] = parser.get_stats(results[user])


	bigram_diff = list(set(stats[user]['present_bigrams']) - set(stats['test']['present_bigrams']))
	result_copy = results[user]
	for bg in bigram_diff:
		if (bg in result_copy):
			del result_copy[bg]
	stats[user] = parser.get_stats(results[user])

	return stats

def find_closest_user(MSE, stat):
	min_stdev  = min((mse[stat]) for mse in MSE.values())
	for user in MSE:
		if(MSE[user][stat]==min_stdev):
			closest_user = user
	return closest_user


def print_graph(stats, stat):
	x = stats['oskar']['present_bigrams']
	test = stats['test'][stat]
	oskar = stats['oskar'][stat]
	johan = stats['johan'][stat]
	aoife = stats['aoife'][stat]
	luke= stats['luke'][stat]

	#graph showing all stats measures
	plt.plot(x, test, label = "Test")
	plt.plot(x, oskar, label = "Oskar")
	plt.plot(x, johan, label = "Johan")
	plt.plot(x, aoife, label = "Aoife")
	plt.plot(x, luke, label = "Luke")

	plt.xlabel('bigrams')
	plt.legend()
	plt.title('Statisics of ' + stat)
	plt.show()

def print_closest_user_graph(stats, user, stat):
	x = stats['test']['present_bigrams']
	test_line = stats['test'][stat]
	user_line = stats[user][stat]

	plt.plot(x, test_line, label = "Test")
	plt.plot(x, user_line, label = "Closest User")

	plt.xlabel('bigrams')
	plt.legend()
	plt.title('Comparison of ' + stat + ' with the closest user: ' + user)
	plt.show()

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



	## Just printing the results
	def print_results(self):
		print(self.results)
		print(self.std_devs)
		print(self.means)
		print(self.variances)
