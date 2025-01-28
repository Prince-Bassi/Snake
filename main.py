import pygame
import config
import random
from snake import Snake

pygame.init()

screen = pygame.display.set_mode(config.SCREEN_SIZE)
pygame.display.set_caption("Snake")
font = pygame.font.SysFont('Arial', 36)
smallFont = pygame.font.SysFont("Arial", 25)

class Game:
	def __init__(self):
		self.snake = Snake()
		self.applePos = []
		self.score = 0
		self.drawApple()
		self.over = False

		self.buttonRect = None

	def drawGameOver(self):
		boxWidth = 300
		boxHeight = 350
		boxPosX = config.SCREEN_SIZE[0]/2 - (boxWidth/2)
		boxPosY = config.SCREEN_SIZE[1]/2 - (boxHeight/2)

		pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(boxPosX, boxPosY, boxWidth, boxHeight))

		gameOverText = font.render("Game Over", True, config.TEXT_COLOR)
		screen.blit(gameOverText, (220, boxPosY+60))

		scoreText = smallFont.render(f"Score: {self.score}", True, config.TEXT_COLOR)
		screen.blit(scoreText, (260, boxHeight-100))		

		buttonWidth = 80
		buttonHeight = 50
		buttonPosX = config.SCREEN_SIZE[0]/2 - (buttonWidth/2)

		self.buttonRect = pygame.Rect(buttonPosX, boxPosY+boxHeight-buttonHeight-30, buttonWidth, buttonHeight)
		pygame.draw.rect(screen, (150, 150, 150), self.buttonRect)

		retryText = smallFont.render("Retry", True, config.TEXT_COLOR)
		screen.blit(retryText, (275, boxPosY+boxHeight-70))

	def retryClick(self, mousePos):
		return True if self.buttonRect and self.buttonRect.collidepoint(mousePos) else False

	def retry(self):
		self.__init__()

	def drawGameScreen(self):
		#Score background
		pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(0, 0, config.SCREEN_SIZE[0], 60))

		scoreText = font.render(f"Score: {self.score}", True, config.TEXT_COLOR)
		screen.blit(scoreText, (250, 8))

		dummyHead = self.snake.head

		while dummyHead:
			nodeRect = pygame.Rect(dummyHead.pos[0], dummyHead.pos[1], config.GRID_SIZE, config.GRID_SIZE)
			pygame.draw.rect(screen, config.SNAKE_COLOR, nodeRect)
			dummyHead = dummyHead.next

	def tick(self):
		if self.over:
			self.drawGameOver()
			return

		self.snake.move()
		collisions = self.checkCollisions()

		if collisions:
			if collisions == 1:
				self.over = True
				self.drawGameOver()
				return
			elif collisions == 2:
				self.score += 1
				self.snake.grow = True

		self.drawGameScreen()


	def checkCollisions(self):
		"""
			Return:
				0: No important collisions
				1: Game Over
				2: Grow
		"""
		headPos = self.snake.head.pos
		outOfBounds = (
			headPos[0] < 0 or
			headPos[0] >= config.SCREEN_SIZE[0] or
			headPos[1] < 60 or
			headPos[1] >= config.SCREEN_SIZE[1]
		)

		if headPos in self.snake.posSet or outOfBounds:
			return 1

		if headPos == self.applePos:
			self.drawApple(True)
			return 2
		else:
			self.drawApple()

		return 0

	def drawApple(self, randomize=False):
		
		if randomize or not self.applePos:
			self.applePos = (
				random.randint(0, config.SCREEN_SIZE[0]/config.GRID_SIZE - 1) * config.GRID_SIZE,
				random.randint(2, config.SCREEN_SIZE[0]/config.GRID_SIZE - 1) * config.GRID_SIZE
			)

		appleRect = pygame.Rect(self.applePos[0], self.applePos[1], config.GRID_SIZE, config.GRID_SIZE)
		pygame.draw.rect(screen, config.APPLE_COLOR, appleRect)


game = Game()
clock = pygame.time.Clock()

while True:
	for event in pygame.event.get():
		mousePos = pygame.mouse.get_pos()

		if event.type == pygame.QUIT:
			pygame.quit()
		elif event.type == pygame.KEYDOWN:
			oppositeDir = tuple(i * -1 for i in game.snake.dir)

			if event.key == pygame.K_RIGHT and oppositeDir != (1, 0):
				game.snake.dir = (1, 0)
			elif event.key == pygame.K_LEFT and oppositeDir != (-1, 0):
				game.snake.dir = (-1, 0)
			elif event.key == pygame.K_UP and oppositeDir != (0, -1):
				game.snake.dir = (0, -1)
			elif event.key == pygame.K_DOWN and oppositeDir != (0, 1):
				game.snake.dir = (0, 1)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if game.retryClick(mousePos):
				game.retry()

	screen.fill(config.BACKGROUND_COLOR)
	game.tick()
	pygame.display.flip()
	clock.tick(config.TICK_SPEED)

pygame.quit()