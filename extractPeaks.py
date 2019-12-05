import numpy as np

def peaks(values, distanceAroundPeak, peakHeight):
	if len(values.shape) > 1:
		print("Can only find peaks in one dimensional array!")
		return
	n = values.shape[0]

	peakIndecies = firstDerivativeTest(values)
	start = np.searchsorted(peakIndecies, distanceAroundPeak, side="right") # find start of indecies which have easily found peak heights
	end = np.searchsorted(peakIndecies, n - distanceAroundPeak) # find end of indecies which have easily found peak heights
	middlePeakIndecies = peakIndecies[start:end] # narrow down to easy indicies
	middlePeakHeights = 2 * values[middlePeakIndecies] - values[middlePeakIndecies - distanceAroundPeak] - values[middlePeakIndecies + distanceAroundPeak] # get peak height (sum of heights on both sides)
	middlePeakIndecies = middlePeakIndecies[np.where(middlePeakHeights > peakHeight)[0]] # narrow down to tall enough peaks

	leftPeakIndecies = peakIndecies[:start] # handle peaks on the left
	leftPeakHeights = 2 * values[leftPeakIndecies] - values[0] - values[leftPeakIndecies + distanceAroundPeak] # calculate peak height relative to start of data
	leftPeakIndecies = leftPeakIndecies[np.where(leftPeakHeights > peakHeight)[0]]

	rightPeakIndecies = peakIndecies[:start] # handle peaks on the right
	rightPeakHeights = 2 * values[rightPeakIndecies] - values[rightPeakIndecies - distanceAroundPeak] - values[-1] # calculate peak height relative to end of data
	rightPeakIndecies = rightPeakIndecies[np.where(rightPeakHeights > peakHeight)[0]]

	peakIndecies = np.concatenate((leftPeakIndecies, middlePeakIndecies, rightPeakIndecies)) # combine all good peaks
	return peakIndecies

def firstDerivativeTest(values, peaksOnly=True):
	deltaValues = values[1:] - values[:-1]
	signs = np.sign(deltaValues)
	signChanges = signs[1:] - signs[:-1]
	if (peaksOnly):
		return np.where(signChanges < 0)[0] + 1
	else:
		return np.where(signChanges != 0)[0] + 1