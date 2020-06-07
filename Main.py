import pygame
import sys 
import time

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

general_font = pygame.font.SysFont('Arial', 20)

class Setting:
	def __init__(self):
		self.size = self.WIDTH, self.HEIGHT = 550, 550
		self.screen = pygame.display.set_mode(self.size)
		self.winning_font = pygame.font.SysFont("monospace", 30)
		self.player_o_score = 0
		self.player_x_score = 0

	def draw_screen(self):
		self.screen.fill(WHITE)

	def score_label(self):
		player_o = general_font.render(f'Player 1: {self.player_o_score}', True, BLACK)
		player_x = general_font.render(f'Player 2: {self.player_x_score}', True, BLACK)

		self.screen.blit(player_o, (10, 10))
		self.screen.blit(player_x, (10, 30))

	def reset_label(self):#reset game, score --> 0
		button = pygame.draw.rect(self.screen, RED, (450, 10, 90, 40))
		reset_label = general_font.render("RESET", True, BLACK)
		reset_label_rect = reset_label.get_rect(topleft=(round(self.WIDTH - 85), 20))
		self.screen.blit(reset_label, reset_label_rect)

	def undo_label(self):
		button = pygame.draw.rect(self.screen, RED, (10, 60, 80, 30), )
		undo_label = general_font.render("Undo", True, BLACK)
		self.screen.blit(undo_label, [25, 65])


	def winning_label(self, win_player):
		if win_player == 1:
			win_label = self.winning_font.render("Player O win", True, GREEN, BLACK)
			self.player_o_score += 1
		elif win_player == 2:
			win_label = self.winning_font.render("Player X win", True, GREEN, BLACK)
			self.player_x_score += 1
		elif win_player == 3:
			win_label = self.winning_font.render("DRAW", True, RED, BLACK)
		else:
			win_label = self.winning_font.render("", True, RED)
		win_label_rect = win_label.get_rect(midtop=(round(self.WIDTH / 2), 10))
		self.screen.blit(win_label, win_label_rect)



class Grid:
	def __init__(self):
		self.grids = [[(50, 250), (500, 250)], #horizontal line
					  [(50, 400), (500, 400)], #horizontal line
					  [(200, 100), (200, 550)], #vertical line
					  [(350, 100), (350, 550)]] #vertical line

		self.square = [(125, 175), (275, 175), (425, 175),
					   (125, 325), (275, 325), (425, 325),
					   (125, 475), (275, 475), (425, 475)]		

	def draw_grids(self, screen):
		for line in self.grids:
			pygame.draw.line(screen, BLACK, line[0], line[1], 2)


class Main:
	def __init__(self):
		self.grid = Grid()
		self.setting = Setting()
		self.player_pos = []
		self.check_box = [[0, 0, 0],
						  [0, 0, 0],
						  [0, 0, 0]]
	
	def hit_square(self, mouse_pos):
		for index, pos in enumerate(self.grid.square):
			if mouse_pos[0] <= pos[0] + 75 and mouse_pos[0] >= pos[0] - 75:
				if mouse_pos[1] <= pos[1] + 75 and mouse_pos[1] >= pos[1] - 75:
					return True, index
		return False, -1

	def get_winner(self, x, y):
		if self.check_box[x][y] == 1:
			return 1
		elif self.check_box[x][y] == 2:
			return 2

	def check_win(self):
		for i in range(3):
			if self.check_box[i][0] == self.check_box[i][1] == self.check_box[i][2]:#rows
				if self.check_box[i][0] != 0:
					return self.get_winner(i, 0)
			elif self.check_box[0][i] == self.check_box[1][i] == self.check_box[2][i]:#column
				if self.check_box[0][i] != 0:
					return self.get_winner(0, i)

		if self.check_box[0][0] == self.check_box[1][1] == self.check_box[2][2]:#diagonal 1
			if self.check_box[0][0] != 0:
				return self.get_winner(0, 0)
		if self.check_box[0][2] == self.check_box[1][1] == self.check_box[2][0]:#diagonal 2
			if self.check_box[0][2] != 0:
				return self.get_winner(0, 2)
		
		for arr in self.check_box:
			for value in arr:
				if value == 0:
					return 0
		return 3


	def non_duplicate(self, lis):
		result = []
		for i in lis:
			if i not in result:
				result.append(i)
		return result

	def convert(self, index):
		for i in range(9):
			if index == i:
				if index < 3:
					return 0, index
				elif index < 6:
					return 1, index - 3
				elif index < 9:
					return 2, index - 6
		return None

	def reset(self):
		#reset everything back to the start
		self.check_box = [[0, 0, 0] for i in range(3)]
		self.player_pos = []

	def hit_restart_button(self, mouse_pos):
		mouse_pos_x, mouse_pos_y = mouse_pos

		if mouse_pos_x > 200 and mouse_pos_x < 200 + 150:
			if mouse_pos_y > 50 and mouse_pos_y < 50 + 50:
				return True
		return False

	def hit_reset_button(self, mouse_pos):
		mouse_pos_x, mouse_pos_y = mouse_pos

		if mouse_pos_x > 450 and mouse_pos_x < 450 + 90:
			if mouse_pos_y > 10 and mouse_pos_y < 10 + 40:
				return True
		return False

	def hit_undo_button(self, mouse_pos):
		mouse_pos_x, mouse_pos_y = mouse_pos

		if mouse_pos_x > 10 and mouse_pos_x < 10 + 80:
			if mouse_pos_y > 60 and mouse_pos_y < 60 + 30:
				return True
		return False

	def undo(self, current_index):
		first_index, second_index = self.convert(current_index)

		self.player_pos.pop()
		self.check_box[first_index][second_index] = 0

	def restart(self): #Click on restart and add score
		button = pygame.draw.rect(self.setting.screen, GREEN, (200, 50, 150, 50))
		restart_label = general_font.render("Restart", True, BLACK)
		restart_label_rect = restart_label.get_rect(midtop=(round(self.setting.WIDTH / 2), 65))
		self.setting.screen.blit(restart_label, restart_label_rect) 
		pygame.display.update()


		restart = True
		while restart:
			for events in pygame.event.get():
				mouse_pos = pygame.mouse.get_pos()
				if events.type == pygame.QUIT:
					sys.exit()
					pygame.quit()

				if events.type == pygame.MOUSEBUTTONDOWN:
					if self.hit_restart_button(mouse_pos):
						restart = False

					if self.hit_reset_button(mouse_pos):
						self.reset_game()
						restart = False

		self.reset()

	def reset_game(self):
		self.reset()
		self.setting.player_o_score = 0
		self.setting.player_x_score = 0


	def game_loop(self):
		gameRun = True 
		count = 1
		undo_flag = True

		while gameRun:
			self.setting.draw_screen()
			self.setting.score_label()
			self.grid.draw_grids(self.setting.screen)
			self.setting.undo_label()
			self.setting.reset_label()

			mouse_pos = pygame.mouse.get_pos()
			turn_flag = True #Take turns between x and o

			for events in pygame.event.get():
				if events.type == pygame.QUIT:
					sys.exit()
					pygame.quit()

				if events.type == pygame.MOUSEBUTTONDOWN:
					if self.hit_reset_button(mouse_pos):
						self.reset_game()

					if self.hit_square(mouse_pos)[0]:
						_, current_index = self.hit_square(mouse_pos)
						mouse_pos_clone = self.grid.square[current_index]
						self.player_pos.append(mouse_pos_clone)
						undo_flag = True
					
					if self.hit_undo_button(mouse_pos):
						if len(self.player_pos) > 0:
							if undo_flag:
								undo_flag = False
								print(current_index)
								self.undo(current_index)
					
			print(self.check_box)
			self.player_pos = self.non_duplicate(self.player_pos)
			

			for pos in self.player_pos:
				first_index, second_index = self.convert(current_index)
				if turn_flag:
					pygame.draw.circle(self.setting.screen, GREEN, pos, 50, 5)
					turn_flag = False
					if undo_flag:
						self.check_box[first_index][second_index] = 1
				else:
					x = pos[0]
					y = pos[1]

					pygame.draw.line(self.setting.screen, RED, (x- 50, y - 50), (x + 50, y + 50), 5)
					pygame.draw.line(self.setting.screen, RED, (x - 50, y + 50), (x + 50, y - 50), 5)
					turn_flag = True
					if undo_flag:
						self.check_box[first_index][second_index] = 2

					
			if self.check_win() > 0:
				self.setting.winning_label(self.check_win())
				self.restart()

			pygame.display.update()

if __name__ == "__main__":
	main = Main()
	main.game_loop()