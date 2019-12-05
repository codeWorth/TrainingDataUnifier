import json, bz2, argparse, pickle

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Converts a .txt training data file to a .pbz2 file.")
	parser.add_argument("--input", required=True, type=str, help="The .txt file containing the training data.")
	parser.add_argument("--output", type=str, help="Path to the output .pbz2 file.")

	args = parser.parse_args()

	path = args.input
	if args.output == None:
		outputPath = path.split(".")[0] + ".pbz2"
	else:
		outputPath = args.output

	print("Loading RLBot data from " +  path + "...")
	rlbotData = []
	with open("training-data.txt") as file:
		line = file.readline()
		while line:
			rlbotData.append(json.loads(line))
			line = file.readline()

	print("Loaded RLBot data")
	print("Saving to " + outputPath + "...")

	with bz2.BZ2File(outputPath, 'w') as f:
	    pickle.dump(rlbotData , f)

	print("Done")