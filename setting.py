import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
OPAQUE_GREEN = (0, 180, 0)

general_font = pygame.font.SysFont('Arial', 20)

class Setting:
	def __init__(self):
		self.size = self.WIDTH, self.HEIGHT = 550, 550
		self.screen = pygame.display.set_mode(self.size)
		self.winning_font = pygame.font.SysFont("monospace", 35)
		self.player_o_score = 0
		self.player_x_score = 0
		self.title = "Tic Tac Toe"

	def set_title(self):
		pygame.display.set_caption(self.title)

	def draw_screen(self):
		self.screen.fill(WHITE)

	def score_label(self):
		player_o = general_font.render(f'Player 1: {self.player_o_score}', True, BLACK)
		player_x = general_font.render(f'Player 2: {self.player_x_score}', True, BLACK)

		self.screen.blit(player_o, (10, 10))
		self.screen.blit(player_x, (10, 30))

	def reset_label(self):#reset game, score --> 0
		button = pygame.draw.rect(self.screen, BLUE, (450, 10, 90, 40))
		reset_label = general_font.render("RESET", True, WHITE)
		reset_label_rect = reset_label.get_rect(topleft=(round(self.WIDTH - 85), 20))
		self.screen.blit(reset_label, reset_label_rect)

	def undo_label(self):
		button = pygame.draw.rect(self.screen, RED, (10, 60, 80, 30), )
		undo_label = general_font.render("Undo", True, BLACK)
		self.screen.blit(undo_label, [25, 65])

	def winning_label(self, win_player):
		if win_player == 1:
			win_label = self.winning_font.render("Player 1 win", True, OPAQUE_GREEN)
			self.player_o_score += 1
		elif win_player == 2:
			win_label = self.winning_font.render("Player 2 win", True, OPAQUE_GREEN)
			self.player_x_score += 1
		elif win_player == 3:
			win_label = self.winning_font.render("DRAW", True, RED)
		else:
			win_label = self.winning_font.render("", True, RED)
		win_label_rect = win_label.get_rect(midtop=(round(self.WIDTH / 2), 10))
		self.screen.blit(win_label, win_label_rect)

	def next_move(self, turn_flag):
		next = self.winning_font.render("NEXT:", True, BLACK)

		if turn_flag:
			next_move_label = self.winning_font.render("O", True, OPAQUE_GREEN)
		else:
			next_move_label = self.winning_font.render("X", True, RED)
		move_label_rect = next_move_label.get_rect(topright=(self.WIDTH - 10, 61)) 

		self.screen.blit(next, (self.WIDTH - 140, 60))
		self.screen.blit(next_move_label, move_label_rect)