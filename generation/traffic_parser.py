import configparser

def readTrafficData(configFile):
	config = configparser.ConfigParser()
	config.read(configFile)
	trafficSpeed = int(config["default"]["trafficSpeed"])
	mtSpeed = int(config["default"]["massTransportSpeed"])
	distStationsX = int(config["default"]["distStationsX"])
	distStationsY = int(config["default"]["distStationsY"])
	frequency = int(config["default"]["frequency"])	
	return trafficSpeed, mtSpeed, distStationsX, distStationsY, frequency

