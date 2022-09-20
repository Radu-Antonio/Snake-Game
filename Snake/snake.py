import pygame, random, sys, os

os.chdir(os.path.dirname(__file__) + '\\muzica')
pygame.init()
pygame.display.set_caption('Snake')
fps = 18
fpsclock = pygame.time.Clock()
SCREEN_SIZE = 900
RED, GREEN = (176, 18, 18), (71, 182, 15)
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pieceSize = SCREEN_SIZE // 30
snake = [(SCREEN_SIZE // 80 * pieceSize, SCREEN_SIZE // 80 * pieceSize)]
direction = 'r'
apple = (random.randint(0, SCREEN_SIZE - 1) // pieceSize * pieceSize, random.randint(0, SCREEN_SIZE - 1) // pieceSize * pieceSize)
ALIVE = True
highscore = 0
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
food = pygame.mixer.Sound('food.mp3')
dead = pygame.mixer.Sound('dead.mp3')

def reset():
	global snake, direction, apple, ALIVE
	snake = [(SCREEN_SIZE // 80 * pieceSize, SCREEN_SIZE // 80 * pieceSize)]
	direction = 'r'
	apple = (random.randint(0, SCREEN_SIZE - 1) // pieceSize * pieceSize, random.randint(0, SCREEN_SIZE - 1) // pieceSize * pieceSize)
	ALIVE = True
	
def showScore():
	text = pygame.font.Font(pygame.font.get_default_font(), 30).render(f'Score: {len(snake) - 1}', True, (255, 255, 255))
	textRect = text.get_rect()
	textRect.center = (70, 30)
	screen.blit(text, textRect)

def endScreen():
	text1 = pygame.font.Font(pygame.font.get_default_font(), 80).render(f'HighScore: {highscore}', True, (255, 255, 255))
	text2 = pygame.font.Font(pygame.font.get_default_font(), 50).render(f'Press SPACE to play again', True, (255, 255, 255))
	textRect = text1.get_rect()
	textRect.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 2 -  40)
	screen.blit(text1, textRect)
	textRect = text2.get_rect()
	textRect.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 40)
	screen.blit(text2, textRect)

def draw():
	screen.fill((42, 42, 32))
	pygame.draw.rect(screen, RED, (apple[0], apple[1], pieceSize - 2, pieceSize - 2))
	for piece in snake:
		pygame.draw.rect(screen, GREEN, (piece[0], piece[1], pieceSize - 2, pieceSize - 2))
	showScore()

def update(dir):
	global apple, snake, ALIVE, highscore
	head = snake[0]
	if ALIVE:
		for piece in snake[1:]:
			if head == piece:
				ALIVE = False
				highscore = max(len(snake) - 1, highscore)
				dead.play()
				return
	else:
		return
			
	if apple[0] <= head[0] < apple[0] + pieceSize and apple[1] <= head[1] < apple[1] + pieceSize:
		food.play()
		f = lambda : random.randint(0, SCREEN_SIZE - 1) // pieceSize * pieceSize
		ok = False
		while not ok:
			apple = (f(), f())
			for piece in snake:
				if apple == piece:
					break
			else:
				ok = True
		snake.append(head)
	snake.pop()

	if dir == 'r':
		head = head[0] + pieceSize, head[1]
	elif dir == 'u':
		head = head[0], head[1] - pieceSize
	elif dir == 'd':
		head = head[0], head[1] + pieceSize
	else:
		head = head[0] - pieceSize, head[1]
	x = 900 if head[0] < 0 else 0 if head[0] >= 900 else head[0]
	y = 900 if head[1] < 0 else 0 if head[1] >= 900 else head[1]
	snake.insert(0, (x, y))

def main():
	global direction, ALIVE
	reset()
	while True:
		draw()
		update(direction)
		if not ALIVE:
			endScreen()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not ALIVE:
					reset()
				if event.key == pygame.K_UP or event.unicode == 'w':
					direction = 'u'
				elif event.key == pygame.K_DOWN or event.unicode == 's':
					direction = 'd'
				elif event.key == pygame.K_RIGHT or event.unicode == 'd':
					direction = 'r'
				elif event.key == pygame.K_LEFT or event.unicode == 'a':
					direction = 'l'
		pygame.display.update()
		fpsclock.tick(fps)

if __name__ == "__main__":
	main()