import pygame
import sys 
from grid import *
from setting import *


class Main:
	def __init__(self):
		self.grid = Grid()
		self.setting = Setting()
		self.player_pos = []
		self.check_box = [[0, 0, 0],
						  [0, 0, 0],
						  [0, 0, 0]]
		self.turn_swap = False
	
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

	def convert_to_2d(self, index):
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
		first_index, second_index = self.convert_to_2d(current_index)

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
						#Swap turn every time you hit restart
						self.turn_swap = self.change_turn(self.turn_swap)
						restart = False

					if self.hit_reset_button(mouse_pos):
						self.reset_game()
						restart = False

		self.reset()

	def reset_game(self):
		self.reset()
		self.setting.player_o_score = 0
		self.setting.player_x_score = 0

	def change_turn(self, turn):
		return not turn

	def draw_winning_line(self):
		index, win_how = self.index_winning_line()
		line_width = 5
		line_color = ORANGE

		if win_how == 1:
			if index == 0:
				pygame.draw.line(self.setting.screen, line_color, self.grid.square[0], self.grid.square[2], line_width)
			elif index == 1:
				pygame.draw.line(self.setting.screen, line_color, self.grid.square[3], self.grid.square[5], line_width)
			else:
				pygame.draw.line(self.setting.screen, line_color, self.grid.square[6], self.grid.square[8], line_width)

		elif win_how == 2:
			if index == 0:
				pygame.draw.line(self.setting.screen, line_color, self.grid.square[0], self.grid.square[6], line_width)
			elif index == 1:
				pygame.draw.line(self.setting.screen, line_color, self.grid.square[1], self.grid.square[7], line_width)
			else:
				pygame.draw.line(self.setting.screen, line_color, self.grid.square[2], self.grid.square[8], line_width)
				
		elif win_how == 3:
			pygame.draw.line(self.setting.screen, line_color, self.grid.square[0], self.grid.square[8], line_width)
		elif win_how == 4:
			pygame.draw.line(self.setting.screen, line_color, self.grid.square[2], self.grid.square[6], line_width)


	def index_winning_line(self):
		for i in range(3):
			if self.check_box[i][0] == self.check_box[i][1] == self.check_box[i][2]:#rows
				if self.check_box[i][0] != 0:
					return i, 1
			elif self.check_box[0][i] == self.check_box[1][i] == self.check_box[2][i]:#column
				if self.check_box[0][i] != 0:
					return i, 2

		if self.check_box[0][0] == self.check_box[1][1] == self.check_box[2][2]:#diagonal 1
			if self.check_box[0][0] != 0:
				return None, 3
		if self.check_box[0][2] == self.check_box[1][1] == self.check_box[2][0]:#diagonal 2
			if self.check_box[0][2] != 0:
				return None, 4

		return None, None

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
			self.setting.set_title()

			mouse_pos = pygame.mouse.get_pos()
			turn_flag = True #Take turns between x and o
			#If hit restart --> swap turn
			if self.turn_swap:
				turn_flag = self.change_turn(turn_flag)

			for events in pygame.event.get():
				if events.type == pygame.QUIT:
					sys.exit()
					pygame.quit()

				if events.type == pygame.MOUSEBUTTONDOWN:
					if self.hit_reset_button(mouse_pos):
						self.reset_game()

					if self.hit_square(mouse_pos)[0]:
						#Get the index of mouse_pos if you hit a square(made by grids)
						_, current_index = self.hit_square(mouse_pos)
						#Get the position of the square associated with mouse_pos
						mouse_pos_clone = self.grid.square[current_index]
						self.player_pos.append(mouse_pos_clone)
						#Undo available when you place a move
						undo_flag = True
					
					if self.hit_undo_button(mouse_pos):
						if len(self.player_pos) > 0:
							if undo_flag:
								undo_flag = False
								self.undo(current_index)
			#remove duplicate(preventing draw x on o or the other way around)
			self.player_pos = self.non_duplicate(self.player_pos)
			
			#Draw x and o
			for pos in self.player_pos:
				first_index, second_index = self.convert_to_2d(current_index)
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

			#Detect the next move
			self.setting.next_move(turn_flag)
					
			if self.check_win() > 0:
				self.setting.winning_label(self.check_win())
				self.draw_winning_line()
				self.restart()

			pygame.display.update()

if __name__ == "__main__":
	main = Main()
	main.game_loop()