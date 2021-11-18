import statistics as stat

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

## generates object with timestamp diffs for given input array
def generate_bigram_diffs_array(bigrams, inputs):
	output = {}
	for idx in range(len(inputs)):
		if (idx < len(inputs) - 1):
			line = inputs[idx]
			nxtLine = inputs[idx + 1]
			# crt = current, nxt = next
			crtLetter, crtTimestamp, _ = line.split(' ')
			nxtLetter, nxtTimestamp, _ = nxtLine.split(' ')
			for bg in bigrams:
				diff = float(nxtTimestamp) - float(crtTimestamp)
				if (crtLetter + nxtLetter == bg and is_valid(diff)):
					if (bg in output):
						output[bg].append(diff)
					else:
						output[bg] = [diff]
	return output


## compute timestamp diffs between pressed and set results
def get_pressed_data_diffs(bigrams, vector):
	pressed = list(filter(filter_pressed, vector))
	return generate_bigram_diffs_array(bigrams, pressed)

#calculates the stats and prints them
def get_stats(bigrams, results):
	std_devs = []
	means = []
	variances = []
	present_bigrams = []
	for bigram in bigrams:
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
