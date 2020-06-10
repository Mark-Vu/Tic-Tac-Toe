import pygame

BLACK = (0, 0 , 0)

class Grid:
	def __init__(self):
		self.grids = [[(50, 250), (500, 250)], #horizontal line
					  [(50, 400), (500, 400)], #horizontal line
					  [(200, 100), (200, 550)], #vertical line
					  [(350, 100), (350, 550)]] #vertical line

		#Centers of the squares made by grids so we can draw easily
		self.square = [(125, 175), (275, 175), (425, 175),
					   (125, 325), (275, 325), (425, 325),
					   (125, 475), (275, 475), (425, 475)]		

	def draw_grids(self, screen):
		for line in self.grids:
			pygame.draw.line(screen, BLACK, line[0], line[1], 2)