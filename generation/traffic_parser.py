import configparser

def readTrafficData(configFile):
	config = configparser.ConfigParser()
	config.read(configFile)
	privateSpeed = int(config["default"]["privateSpeed"])
	publicSpeed = int(config["default"]["publicSpeed"])
	distStationsX = int(config["default"]["distStationsX"])
	distStationsY = int(config["default"]["distStationsY"])
	frequency = int(config["default"]["frequency"])	
	return privateSpeed, publicSpeed, distStationsX, distStationsY, frequency

