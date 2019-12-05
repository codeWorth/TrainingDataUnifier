import createTrainingData, json, extractPeaks, correlatePeaks, argparse
from matplotlib import pyplot as plt
import numpy as np

def extractProperty(item, *path):
	i = item
	for p in path:
		i = i[p]
	return i

def extractProperties(array, *path):
	return list(map(lambda item: extractProperty(item, *path), array))

def plotInput(inputString, playerIndex = 0):
		generatedInput = np.asarray(extractProperties(generatedData, "PlayerData", playerIndex, inputString))
		rlbotInput = np.asarray(extractProperties(rlbotData, "PlayerData", playerIndex, inputString))

		plt.plot(generatedTimes, generatedInput, alpha=0.7)
		plt.plot(rlbotTimes, rlbotInput, color="orange", alpha=0.7)
		plt.title("carball {} in blue, rlbot {} in orange".format(inputString, inputString))
		plt.show()

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Synchronizes carball extracted training data in .pbz2 format with rlbot extracted training data in .pbz2 format.")
	parser.add_argument("--generated", required=True, type=str, help="The .pbz2 file extracted from the .replay.")
	parser.add_argument("--rlbot", required=True, type=str, help="The .pbz2 file from direct rlbot training data.")

	args = parser.parse_args()

	# get raw data
	print("Loading generated data...")
	generatedData = createTrainingData.loadSavedTrainingData("replay.pbz2")
	print("Loaded generated data")

	print("Loading RLBot data...")
	rlbotData = createTrainingData.loadSavedTrainingData("training-data.pbz2")
	print("Loaded RLBot data")

	# extract times
	generatedTimes = extractProperties(generatedData, "GameState", "time")
	rlbotTimes = extractProperties(rlbotData, "GameState", "time")

	# extract heights
	generatedBallHeight = np.asarray(extractProperties(generatedData, "GameState", "ball", "position", 2))
	rlbotBallHeight = np.asarray(extractProperties(rlbotData, "GameState", "ball", "position", 2))

	# extract peaks from rlbot
	realSwitchIndecies = extractPeaks.peaks(rlbotBallHeight, 60, 400)
	realSwitchHeights = rlbotBallHeight[realSwitchIndecies]
	realSwitchTimes = list(map(lambda n: rlbotData[n]["GameState"]["time"], realSwitchIndecies))
	for t in realSwitchTimes:
		plt.axvline(x=t, color="orange")


	# extract peaks from replay
	genSwitchIndecies = extractPeaks.peaks(generatedBallHeight, 25, 400)
	genSwitchHeights = generatedBallHeight[genSwitchIndecies]
	genSwitchTimes = list(map(lambda n: generatedData[n]["GameState"]["time"], genSwitchIndecies))
	for t in genSwitchTimes:
		plt.axvline(x=t)

	# plot heights w/ peaks
	plt.plot(generatedTimes, generatedBallHeight)
	plt.plot(rlbotTimes, rlbotBallHeight, color="orange")
	plt.show()

	# extract dTs for correlated peaks
	rlbotT, dTs = correlatePeaks.peakDXs(realSwitchTimes, realSwitchHeights, genSwitchTimes, genSwitchHeights, 7, 4)
	# plot it
	plt.plot(rlbotT, dTs, '--bo')
	plt.title("delta time is carball minus rlbot")
	plt.show()

	# get adjusted rlbotTimes to match generatedTimes
	rlbotTimes = correlatePeaks.adjustXs(np.asarray(rlbotTimes), rlbotT, dTs)
	for i in range(len(rlbotData)):
		rlbotData[i]["GameState"]["time"] = rlbotTimes[i]

	# plot heights (should look nearly identical)
	plt.plot(generatedTimes, generatedBallHeight)
	plt.plot(rlbotTimes, rlbotBallHeight, color="orange")
	plt.show()

	# plotInput("pitch")
	# plotInput("yaw")
	# plotInput("roll")
	plotInput("handbrake")