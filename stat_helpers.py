import matplotlib.pyplot as plt
import numpy as np

def mse(Y_true, T_pred):
	return np.square(np.subtract(Y_true, T_pred)).mean()

def print_graph(stats, stat, present_bigrams, users):
	x = present_bigrams

	for user in users:
		plt.plot(x, stats[user][stat], label = user)

	plt.xlabel('bigrams')
	plt.legend()
	plt.title('Statisics of ' + stat)
	plt.show()

def print_closest_user_graph(stats, test_stats, user, stat_key, bigrams):
	test_line = test_stats[stat_key]
	user_line = stats[user][stat_key]

	plt.plot(bigrams, test_line, label = "Test")
	plt.plot(bigrams, user_line, label = "Closest User")

	plt.xlabel('bigrams')
	plt.legend()
	plt.title('Comparison of ' + stat_key + ' with the closest user: ' + user)
	plt.show()

def find_closest_user(MSE, stat_key):
	min_stdev  = min((mse[stat_key]) for mse in MSE.values())
	for user in MSE:
		if(MSE[user][stat_key]==min_stdev):
			closest_user = user
	return closest_user
