import configparser

def readTrafficData(configFile):
	config = configparser.ConfigParser()
	config.read(configFile)
	privateSpeed = int(config["default"]["privateSpeed"])
	publicSpeed = int(config["default"]["publicSpeed"])
	distStations = int(config["default"]["distStations"])
	numLines = int(config["default"]["numLines"])
	frequency = int(config["default"]["frequency"])	
	return privateSpeed, publicSpeed, distStations, numLines, frequency

