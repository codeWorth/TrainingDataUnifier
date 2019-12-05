import numpy as np

# assumes x1s are sorted
# assumes x2 leads x1
# returns (x1s, dXs), where dXs = x2s - x1s and the peaks are correlated
def peakDXs(x1s, y1s, x2s, y2s, maxDx, maxDy):
	x1sCorrelated = []
	dXs = []
	maxDx = abs(maxDx) # ensure that maxDx and maxDy are positive
	maxDy = abs(maxDy)

	n1 = len(x1s) # cache length of arrays
	n2 = len(x2s)
	i = 0
	j = 0
	while i < n1:
		x1 = x1s[i] # iterate over each 
		y1 = y1s[i]

		dx = 0
		dy = 0
		while j < n2 and dx < maxDx: # iterate over x2 until it ends or dx beomes too large
			x2 = x2s[j]
			y2 = y2s[j]
			dx = x2 - x1
			dy = y2 - y1
			j += 1
			if dy < maxDy and dy > -maxDy and dx > 0:
				x1sCorrelated.append(x1)
				dXs.append(dx)
				break

		j -= 1 # allow match x1s to single x2s
		i += 1

	return (np.asarray(x1sCorrelated), np.asarray(dXs))

# xs is an array of times within the same context as x1s from peakDXs()
# returns xs adjusted to match x2s using dX at each matched peak
def adjustXs(xs, peakXs, peakDxs):
	dXsInterped = interpSorted(peakXs, peakDxs, xs)
	return xs + dXsInterped

def interpSorted(xPoints, yPoints, xs):
	minX = np.min(xs)
	maxX = np.max(xs)

	# put extra points so that every x in xs has a lower and upper bounding value in xPoints
	xPointsPadded = np.empty(len(xPoints)+2, xPoints.dtype)
	xPointsPadded[0] = minX-1
	xPointsPadded[1:-1] = xPoints
	xPointsPadded[-1] = maxX+1

	yPointsPadded = np.empty(len(yPoints)+2, yPoints.dtype)
	yPointsPadded[0] = yPoints[0]
	yPointsPadded[1:-1] = yPoints
	yPointsPadded[-1] = yPoints[-1]

	indecies = np.searchsorted(xPointsPadded, xs) # index of closest xPoint above each x in xs
	# interpolation
	x1s = xPointsPadded[indecies-1]
	y1s = yPointsPadded[indecies-1]
	x2s = xPointsPadded[indecies]
	y2s = yPointsPadded[indecies]
	dXs = x2s - x1s
	dYs = y2s - y1s
	ts = (xs - x1s) / dXs
	return ts*dYs + y1s