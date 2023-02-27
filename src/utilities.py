# functions that didnt fit an other file

import pygame, time, os.path, pages

def roundSurface(inSurf, roundness):
	size = inSurf.get_size()
	mask = pygame.Surface(size, pygame.SRCALPHA)
	pygame.draw.rect(mask, (255, 255, 255), (0, 0, *size), border_radius=roundness)
	image = inSurf.copy().convert_alpha()
	image.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MIN)
	return image

def checkForExpiredProducts(pVs):
	inventory = pVs.manager.getInventoryAndExpireDates()
	csvPath = pVs.manager.csvPath
	data = loadCSV(csvPath)

	expiredProducts = {}
	for product in list(inventory.keys()):
		expiryDate = int(inventory[product]["timeStamp"]) + daysToSeconds(inventory[product]["days"])
		if  expiryDate < time.time():
			timeSinceExpiry = time.time() - (inventory[product]["timeStamp"] + daysToSeconds(inventory[product]["days"]))
			if not str(expiryDate) in data:
				#//TODO:WARN
				print("warning:  product:", product, " has expired ", timeSinceExpiry, " days ago")
				expiredProducts[product] = timeSinceExpiry

				# mark as warned
				data.append(str(expiryDate))
				writeCSV(csvPath, data)
	if len(expiredProducts):
		pVs.currentPage = pages.expiryWarningPage(pVs, expiredProducts)


def daysToSeconds(days):
	return (days * 24 * 60 * 60)

def SecondsToDays(seconds):
	return (seconds / 60 /60 / 24)

def loadCSV(filePath):
	with open(filePath, "r") as fp:
		data = fp.read().replace("\n", "").split(",")
	return list(data)

def writeCSV(filePath, listData):
	with open(filePath, "w") as fp:
		fp.write(",".join(listData))
