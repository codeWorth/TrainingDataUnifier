import createTrainingData, argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Converts a .replay file to a .pbz2 file using carball.")
	parser.add_argument("--input", required=True, type=str, help="The .replay file containing the rocket league replay.")
	inputFile = parser.parse_args().input
	filename = inputFile.split(".")[0]

	print("Extracting " + inputFile + " to " + filename+".json ...")
	extractedGameStatesAndControls = createTrainingData.convert_replay_to_game_frames(inputFile, filename+".json", save_json = True)
	print(".json file extracted.")

	print("Converting " + filename+".json to " + filename+".pbz2 ...")
	createTrainingData.createAndSaveReplayTrainingDataFromJSON(filename+".json", outputFileName = filename+".pbz2")
	print("Done")