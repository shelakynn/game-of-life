import pygame, sys
from pygame.locals import *
import random
from pprint import pprint

WIDTH=640
HEIGHT=480
CELLSIZE=10
FPS = 10

assert WIDTH % CELLSIZE == 0, "Width must be a multiple of cell size"
assert HEIGHT % CELLSIZE == 0, "Height must be a multiple of cell size"

CELLWIDTH = WIDTH // CELLSIZE # Number of cells wide
CELLHEIGHT = HEIGHT // CELLSIZE # Number of cells high

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (40, 40, 40)
GREEN = (0, 255, 0)

# Grid drwawing function
def drawGrid():
	for x in range(0, WIDTH, CELLSIZE): # Verical lines
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, HEIGHT))
	for y in range(0, HEIGHT, CELLSIZE): # Horizontal lines
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WIDTH, y))

# Create and initialise cells dictionary
def blankGrid():
	gridDict = {}
	for y in range(CELLHEIGHT):
		for x in range(CELLWIDTH):
			gridDict[x,y] = 0 # Start with all dead cells

	return gridDict

# Spawn live cells
def startingGridRandom(lifeDict):
	for item in lifeDict:
		lifeDict[item] = random.randint(0,1)
	return lifeDict

# Give colours to cells
def colourGrid(item, lifeDict):
	x = item[0]
	y = item[1]

	# Actual cell size
	x = x * CELLSIZE
	y = y * CELLSIZE

	if lifeDict[item] == 0:
		pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE))

	if lifeDict[item] == 1:
		pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELLSIZE, CELLSIZE))

	return None

# Check cell's neighbours
def getNeighbours(item, lifeDict):
	neighbours = 0
	for x in range (-1, 2):
		for y in range (-1, 2):
			checkCell = (item[0]+x, item[1]+y)
			if checkCell[0] < CELLWIDTH and checkCell[0] >= 0:
				if checkCell[1] < CELLHEIGHT and checkCell[1] >= 0:
					if lifeDict[checkCell] == 1:
						if x == 0 and y == 0:
							neighbours += 0
						else:
							neighbours += 1
	return neighbours

# Game tick
def tick(lifeDict):
	newTick = {}
	for item in lifeDict:
		numberNeighbours = getNeighbours(item, lifeDict)
		if lifeDict[item] == 1: # For live cells
			if numberNeighbours < 2: # kill for under-population
				newTick[item] = 0
			elif numberNeighbours > 3: # kill for over-population
				newTick[item] = 0
			else:
				newTick[item] = 1 # Cell survives
		elif lifeDict[item] == 0:
			if numberNeighbours == 3: # cells around reproduce
				newTick[item] = 1
			else:
				newTick[item] = 0
	
	return newTick

# Calculate how similar two ticks are
def checkStability(old, new):
	same = {k: old[k] for k in old if k in new and old[k] == new[k]}
	stability = ((len(same))/(CELLWIDTH * CELLHEIGHT)) * 100
	return stability	

# The actual game starts here!
def main():
	pygame.init()
	global DISPLAYSURF
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption('Game of Life')
	highestStability = 0

	DISPLAYSURF.fill(WHITE) # Background

	lifeDict = blankGrid()
	lifeDict = startingGridRandom(lifeDict)

	for item in lifeDict:
		colourGrid(item, lifeDict)

	drawGrid()
	pygame.display.update()

	while True: # Main game loop
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYUP:
				pprint('Highest stability achieved:')
				pprint(highestStability)
				pygame.quit()
				sys.exit()
		
		# Run a tick, but save old tick first
		oldDict = lifeDict
		lifeDict = tick(lifeDict)

		# Do something if the 2 ticks are too similar
		stability = checkStability(oldDict, lifeDict)
		if stability > highestStability:
			highestStability = stability
		
		# Colour the new grid setup
		for item in lifeDict:
			colourGrid(item, lifeDict)
		drawGrid()
		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == '__main__':
	main()
