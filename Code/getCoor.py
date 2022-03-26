def printCoor(string:str):
	O = (115.0, 18.0)
	resolution = 0.0125
	lo = string.split(',')[0].strip()
	la = string.split(',')[1].strip()
	
	loLeft = float(lo.split(" ")[0])
	loRight = float(lo.split(" ")[1])

	laLeft = float(la.split(" ")[0])
	laRight = float(la.split(" ")[1])

	loLeft += loRight/60
	laLeft += laRight/60

	print((float(loLeft)-O[0])/resolution)
	print((float(laLeft)-O[1])/resolution)


if __name__ == "__main__":
	import math
	while True:
		string = input()
		printCoor(string)
		print(1/math.log(2))