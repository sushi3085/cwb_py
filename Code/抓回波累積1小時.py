import threading
import time
import dataCrawler as dc

def storeData():
	data, stamp = dc.getRadarData()
	dc.dumpRadarData(data, stamp)

	data, stamp = dc.getRainData()
	dc.dumpRadarData(data, stamp)

def main():
	while True:
		storeData()
		print("stored", time.strftime("%D %H:%M:%S", time.localtime()))
		time.sleep(8*60)
if __name__ == "__main__":
	main()