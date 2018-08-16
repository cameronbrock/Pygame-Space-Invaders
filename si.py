#Sprites from https://www.deviantart.com/gooperblooper22/art/Space-Invaders-Sprite-Sheet-135338373

import pygame
import math
import random










#Player class
class Player:
	def __init__(self):

		#Determines the player's current score
		self.score = 0
		#The number of times the player can die before game over
		self.lives = 3

		#width and height of the player character in terms of pixels
		self.width = 52
		self.height = 31

		#The initial starting position of the player on the screen
		self.x = (width // 2) - self.width
		self.y = height - self.height

		#The player's velocity as they move
		self.velocity = 10

		#This determines how long before the player can fire another projectile
		self.cooldown = 5
		#The iteration that determines if the cooldown has been reached yet.
		self.projIter = self.cooldown

		#Determine how long the player will go through the death "animation"
		self.deathDuration = 70
		self.deathIteration = 0
		#Dead means that the player has been killed. finishedDying means that the player's
		#death animation has been completed.
		self.dead = False
		self.finishedDying = False

		#At the beginning of the game, there is a brief period where neither the player nor
		#the enemies can fire. They are considered 'locked' at this point. Afterward, they are
		#'unlocked.'
		self.unlocked = False


	def advance(self):
		#The term 'advancing' is used to refer to a character's ability to change position
		#or fire their laser. At every instant in the game, each character advances slightly.

		#Gets input from the user
		self.get_user_input()

		if self.dead:
			#If player is dead:
			if self.deathIteration < self.deathDuration:
				#If the character is still dying, iterate deathIteration.
				self.deathIteration += 1
			else:
				#Otherwise:
				if self.lives <= 0:
					#If the player is out of lives, they are finished dying.
					self.finishedDying = True
				else:
					#Otherwise, resurrect the player to continue playing
					self.dead = False
					self.deathIteration = 0


	def die(self):
		#Kill the player and decrement lives
		self.dead = True
		self.lives -= 1


	def draw(self):
		#Draw the player character on the screen
		if not self.dead:
			#Draw the player sprite
			self.img = pygame.image.load('sprites/player.png')
		else:
			#Draw the destroyed player sprite
			self.img = pygame.image.load('sprites/player_exp.png')
		#Modify the sprite so that it is the appropriate size
		self.img = pygame.transform.scale(self.img, (self.width, self.height))
		
		#blit the image on the screen
		window.blit(self.img, (self.x, self.y))


	def fire(self):
		#Fire the player's laser cannon
		if self.projIter >= self.cooldown:
			#If the cooldown period has been reached, add a new laser to the screen with the
			#same coordinates as the player, and reset projIter to zero.
			player_proj.append(Projectile(self.x + (self.width // 2), self.y, (0, 255, 0), math.pi / 2))
			self.projIter = 0
		else:
			#Otherwise, reset the projIter.
			self.projIter += 1



	def get_user_input(self):
		#Get input from the user

		#Get keyboard input
		keys = pygame.key.get_pressed()

		if not self.dead:
			#If the player is not dead, decrement x position if user is pressing left key
			#Increment x position if user is pressing right key.
			#If x-position - velocity goes off the screen, set x-position to zero.
			#If x-position + velocity goes off the screen, set x-position equal to window width - player width
			if keys[pygame.K_LEFT]:
				if self.x > self.velocity:
					self.x -= self.velocity
				else:
					self.x = 0
			elif keys[pygame.K_RIGHT]:
				if self.x + self.width + self.velocity > width:
					self.x = width - self.width
				else:
					self.x += self.velocity
			#If the player is pressing the up key and the player's laser cannon is unlocked,
			#fire.
			if keys[pygame.K_UP] and self.unlocked:
				self.fire()


	def unlock(self):
		#'Unlock' the player's ability to fire
		self.unlocked = True



#The enemy class
class Enemy:
	def __init__(self, designation, row, column):
		#Width and height of the enemy
		self.width = 43
		self.height = 30

		#The row and column of the enemy within the arrangement of enemies at the top of
		#the screen
		self.row = row
		self.column = column

		#The sprite number (for example, there is an enemy0, enemy1, and enemy2)
		self.spriteNum = 0

		#The speed at which the sprite changes, and the iteration that determines if the
		#time for it to switch has passed
		self.spriteSpd = 15
		self.spriteIter = 0

		#Set the initial (x, y) position of the enemy
		self.x = (self.width + 10) * self.column + 10
		self.y = 20 + (self.height + 10) * self.row + 10 + 30

		#Like the player, the enemy also has a cooldown that determines if it can fire
		#at the moment as well as an iteration.
		self.cooldown = 5
		self.projIter = self.cooldown
		#a value of x in this variable means it has a 1 in x chance of
		#firing at any given opportunity:
		self.fireProb = 200

		#points determines how much the score increments when the player destroys the enemy.
		#The points received depend on the type of enemy.
		self.points = 0
		self.designation = designation
		if self.designation == 0:
			self.points = 30
		elif self.designation == 1:
			self.points = 20
		elif self.designation == 2:
			self.points = 10

		#Velocity determines at what rate the enemy moves accross the screen
		self.velocity = 2
		#direction is measured in radians and determines in what direction the enemy
		#is moving
		self.direction = 0

		#numSteps determines how far accross the screen an enemy will travel. In order to keep
		#all the enemies in the same order, this is determined by column.
		#step is the iteration through numSteps and stepsDown determines how far down they will
		#travel.
		self.step = 0
		self.numSteps = width - 10 - numCols * (self.width + 10) - 1 / ((self.width + 10) * column + 10)
		self.stepsDown = 10

		#Death
		self.deathDuration = 5
		self.deathIteration = 0
		self.dead = False
		self.finishedDying = False

		self.unlocked = False


	def advance(self):
		#Advance the enemy

		#Simplify direction to between 0 and 2pi radians
		while self.direction < 0:
			self.direction += 2 * math.pi
		while self.direction > 2 * math.pi:
			self.direction -= 2 * math.pi

		#Change sprite if the spriteIter has reached spriteSpd
		if (self.spriteIter >= self.spriteSpd):
			self.spriteIter = 0
			if (self.spriteNum == 0):
				self.spriteNum = 1
			else:
				self.spriteNum = 0

		#Iterate spriteIter
		self.spriteIter += 1

		#Travel forward:
		if self.unlocked:
			#Unlike the player, enemies cannot move unless they are unlocked.
			if not self.dead:
				#They also cannot move if they are dead
				if not player.dead:
					#The enemies will freeze in position once the player dies.
					if math.cos(self.direction) == 1 or math.cos(self.direction) == -1:
						#If the enemy is travelling left or right:
						if self.step < self.numSteps:
							#Advance enemy position based on velocity and direction
							self.x += self.velocity * math.cos(self.direction)
							self.y -= self.velocity * math.sin(self.direction)
							self.step += self.velocity
						else:
							#Otherwise, reset direction to 3pi/2, or downward
							self.step = 0
							#Change direction
							self.direction += (3 * math.pi) / 2

					else:
						#If the enemy is not travelling left or right:
						if self.step < self.stepsDown:
							#If the enemy has not reached stepsDown, advance downward and
							#increment step by enemy velocity
							self.y += self.velocity
							self.step += self.velocity
						else:
							#If the enemy has reached stepsDown, reset step to zero and
							#change direction by 3pi/2
							self.step = 0
							#Change direction
							self.direction += (3 * math.pi) / 2

					#Fire
					self.fire()

			#Check for death
			else:
				#If the enemy is dead:
				if self.deathIteration < self.deathDuration:
					#If the enemy is not finished dying, increment deathIteration
					self.deathIteration += 1
				else:
					#Otherwise, set finishedDying to true
					self.finishedDying = True



	def die(self):
		#Allow the enemy to die
		self.dead = True

	def draw(self):
		#Draws the enemy sprite on the screen.
		if not self.dead:
			#If the enemy is not dead, load their sprite given designation and spriteNum
			self.img = pygame.image.load('sprites/enemy' + str(self.designation) + '_' + str(self.spriteNum) + '.png')
		else:
			#Otherwise, display an explosion where the enemy was.
			self.img = pygame.image.load('sprites/exp.png')
		#Set the sprite to the appropriate size
		self.img = pygame.transform.scale(self.img, (self.width, self.height))

		#Blit the image to the screen
		window.blit(self.img, (self.x, self.y))


	def fire(self):
		#Fire the enemy's laser
		if self.projIter >= self.cooldown:
			#If cooldown has been reached:
			if random.randint(0, self.fireProb - 1) < 1:
				#If the enemy has randomly decided to fire:
				enemy_proj.append(Projectile(self.x + (self.width / 2), self.y, (255, 0, 255), (3 * math.pi) / 2))
				#Reset projIter to zero and await it to reach cooldown
				self.projIter = 0
		else:
			#If cooldown has not been reached, increment projIter
			self.projIter += 1


	def unlock(self):
		#Unlocks the enemy's laser
		self.unlocked = True





#The projectile class. This is class describing the projectiles fired by the player and
#the enemies
class Projectile:
	def __init__(self, x, y, color, angle):
		#The (x, y) coordinates of the projectile
		self.x = x
		self.y = y

		#The color of the projectile, described by a tuple (red, green, blue)
		self.color = color

		#The width and height of the projectile
		self.width = 3
		self.height = 15

		#The angle at which the projectile is fired.
		self.angle = angle
		#The velocity at which the projectile travels
		self.velocity = 15


	def advance(self):
		#Avance the (x, y)-position of the projectile by the velocity in the direction of angle
		self.x += self.velocity * math.cos(self.angle)
		self.y -= self.velocity * math.sin(self.angle)

	def draw(self):
		#Draw the projectile on the screen (in this case, it is merely a simple rectangle)
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))










def advance():
	#Advance the projectiles:
	for projectile in player_proj:
		#Check if projectiles have gone off the screen
		if projectile.y + projectile.height < 0 or projectile.y > height:
			player_proj.pop(player_proj.index(projectile))

		projectile.advance()

	for projectile in enemy_proj:
		#Check if projectiles have gone off the screen
		if projectile.y < 0 or projectile.y > height:
			enemy_proj.pop(enemy_proj.index(projectile))

		projectile.advance()

	#Advance the player:
	player.advance()

	#Advance the enemies:
	for enemy in enemies:
		enemy.advance()


def checkDeath():
	#Check if an enemy is finished dying
	for enemy in enemies:
		if enemy.finishedDying:
			#If so, increment player score and remove enemy from list enemies
			player.score += enemy.points
			enemies.pop(enemies.index(enemy))


def checkImpact():
	for enemy in enemies:
		#Checks if player projectile collides with enemy
		for proj in player_proj:
			if (proj.x < enemy.x + enemy.width and proj.x > enemy.x) or (proj.x + proj.width < enemy.x + enemy.width and proj.x + proj.width > enemy.x):
				if (proj.y > enemy.y) and (proj.y < enemy.y + enemy.height):
					enemy.die()
					player_proj.pop(player_proj.index(proj))

		#Check if enemy collides with player
		if (enemy.x < player.x + player.width and enemy.x > player.x) or (enemy.x + enemy.width < player.x + player.width and enemy.x + enemy.width > player.x):
			if enemy.y + enemy.height > player.y:
				player.lives = 0
				player.die()

					
	#Check if enemy projectile collides with player
	for proj in enemy_proj:
		if (proj.x < player.x + player.width and proj.x > player.x) or (proj.x + proj.width < player.x + player.width and proj.x + proj.width > player.x):
			if (proj.y > player.y) and (proj.y < player.y + player.height):
				if not player.dead:
					player.die()
					enemy_proj.pop(enemy_proj.index(proj))


def define_window(width, height):
	#Initialize and return the window
	pygame.init()
	window = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Space Invaders')

	return window



def game_over():
	#Present the game over screen

	#If the player's current score is greater than the current high score, post the player's
	#score as the high score.
	if player.score > int(get_high_score()):
		post_high_score()

	#Fill the window with black
	window.fill((0, 0, 0))

	#Create text for game over and score
	game_over_txt = font.render('Game over', 1, (255, 255, 255))
	score_txt = font.render('Your score: ' + str(player.score), 1, (255, 255, 255))
	#Position and blit them to the screen
	window.blit(game_over_txt, (width / 2 - 30, height / 2 - 20))
	window.blit(score_txt, (width / 2 - 30 - 10 * len(str(player.score)), height / 2))

	#Update the pygame display
	pygame.display.update()

	#The time at which game_over() was called
	end_time = pygame.time.get_ticks()
	#Set game_over_running to true
	game_over_running = True

	while game_over_running:
		#While the game over screen is being presented to the user:
		#Get the current time
		curr_time = pygame.time.get_ticks()
		if curr_time - end_time >= 2000:
			#If s seconds have passed, exit the loop
			game_over_running = False

		#If the user wants to quit, quit the program
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

	#If the loop has ended, quit the program automatiaclly.
	quit()



def generate_enemies(numCols):
	#Fill the list enemies with enemies

	#Set the column equal to zero.
	col = 0
	for i in range(numCols):
		#For every column in numCols, add an enemy
		enemies.append(Enemy(0, 0, col))
		col += 1

	#Repeat for five rows with three types of enemies
	col = 0
	for i in range(numCols):
		enemies.append(Enemy(1, 1, col))
		col += 1

	col = 0
	for i in range(numCols):
		enemies.append(Enemy(1, 2, col))
		col += 1

	col = 0
	for i in range(numCols):
		enemies.append(Enemy(2, 3, col))
		col += 1

	col = 0
	for i in range(numCols):
		enemies.append(Enemy(2, 4, col))
		col += 1
	#enemies.append(Enemy(1, 3, 0))


def get_high_score():
	#Get the high score.
	try:
		#If score.txt exists, read and return the contents.
		file = open('score.txt', 'r')
		return file.read()
	except FileNotFoundError:
		#Otherwise, return zero.
		return '0'


def main_menu():
	#Call the menu at the beginning of the program
	#Fill the window will black
	window.fill((0, 0, 0))
	#Generate font for the title and the enemy points
	titleFont = pygame.font.SysFont('comicsans', 60, True)
	enemy_pt_font = pygame.font.SysFont('comicsans', 20, True)

	#Generate text for the title and the high score
	titleText = titleFont.render('SPACE INVADERS', 1, (255, 255, 255))
	high_score_text = font.render('High score: ' + get_high_score(), 1, (255, 255, 255))

	#Load each enemy sprite
	enemy0_img = pygame.image.load('sprites/enemy0_0.png')
	enemy1_img = pygame.image.load('sprites/enemy1_0.png')
	enemy2_img = pygame.image.load('sprites/enemy2_0.png')

	#Scale each enemy sprite down to a smaller scale
	enemy0_img = pygame.transform.scale(enemy0_img, (21, 15))
	enemy1_img = pygame.transform.scale(enemy1_img, (21, 15))
	enemy2_img = pygame.transform.scale(enemy2_img, (21, 15))

	#Generate text for the enemy points
	enemy0_pts = enemy_pt_font.render('30 points', 1, (255, 255, 255))
	enemy1_pts = enemy_pt_font.render('20 points', 1, (255, 255, 255))
	enemy2_pts = enemy_pt_font.render('10 points', 1, (255, 255, 255))

	#Blit the title and high score to the window
	window.blit(titleText, (width / 2 - 180, height / 2 - 190))
	window.blit(high_score_text, (width / 2 - 60 - 5 * len(str(player.score)), height / 2 - 150))

	#blit enemy icons
	window.blit(enemy0_img, (width / 2 - 30, height / 2 - 80))
	window.blit(enemy1_img, (width / 2 - 30, height / 2 - 55))
	window.blit(enemy2_img, (width / 2 - 30, height / 2 - 30))

	#blit enemy points
	window.blit(enemy0_pts, (width / 2 - 5, height / 2 - 80))
	window.blit(enemy1_pts, (width / 2 - 5, height / 2 - 55))
	window.blit(enemy2_pts, (width / 2 - 5, height / 2 - 30))

	#Prompt the user to press a key and blit to the screen
	user_prompt = font.render('Press any key to play', 1, (255, 255, 255))
	window.blit(user_prompt, (width / 2 - 100, height / 2 + 30))

	#Update the pygame display
	pygame.display.update()

	while True:
		#Get input from the user
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#If the user wants to quit, close the program
				quit()
			elif event.type == pygame.KEYDOWN:
				#If the user presses a key, run the game.
				run_game()


def post_high_score():
	#Open score.txt (or create it if it does not exist) and write the player's score.
	file = open('score.txt', 'w+')
	file.write(str(player.score))


def redraw_game():
	#Redraw background:
	window.fill((0, 0, 0))

	#Redraw projectiles:
	for projectile in player_proj:
		projectile.draw()

	for projectile in enemy_proj:
		projectile.draw()

	#Redraw player:
	player.draw()

	#Redraw enemies:
	for enemy in enemies:
		enemy.draw()

	#Redraw score:
	text = font.render('SCORE: ' + str(player.score), 1, (255, 255, 255))
	window.blit(text, (10, 10))


	#Redraw remaining lives:
	icon_width = 25
	icon_height = 15
	icon = pygame.image.load('sprites/player.png')
	icon = pygame.transform.scale(icon, (icon_width, icon_height))
	for i in range(player.lives):
		window.blit(icon, (width - (i + 1) * icon_width - 10 * (i + 1), 10))



def run():
	#Run the program

	#First, run the menu, then the game, and then quit.
	main_menu()
	run_game()
	quit()


def run_game():
	#Run the game itself.

	#First, generate enemies
	generate_enemies(numCols)

	#The initial time before starting the game
	time0 = pygame.time.get_ticks()

	while True:
		#Run the game undefinitely until the loop is broken
		clock.tick(30)

		#Get the current time
		time1 = pygame.time.get_ticks()

		if time1 - time0 >= 2000:
			#If 2 seconds have passed, unlock the player and enemies
			player.unlock()
			for enemy in enemies:
				enemy.unlock()

		if not player.finishedDying:
			#If the player is not finished dying, advance, redraw, check for impacts,
			#and check for deaths
			advance()
			redraw_game()
			checkImpact()
			checkDeath()
			pygame.display.update()
		else:
			#If the player is finished dying, call the game over function and return
			game_over()
			return

		if len(enemies) == 0:
			#If all enemies have been eliminated, pause momentarily
			time2 = pygame.time.get_ticks()
			pausing = True
			while pausing:

				clock.tick(30)
				player.unlocked = False

				#advance and redraw, then update the game
				advance()
				redraw_game()
				pygame.display.update()

				time3 = pygame.time.get_ticks()
				#If the appropriate time has passed, finish pausing
				if time3 - time2 > 2000:
					pausing = False

				#If the player wants to quit, quit the program
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						quit()

			#Go through all the projectiles in player_proj and enemy_proj and delete them
			for projectile in player_proj:
				player_proj.pop(player_proj.index(projectile))
			for projectile in enemy_proj:
				enemy_proj.pop(enemy_proj.index(projectile))

			#Generate new enemies
			generate_enemies(numCols)



		for event in pygame.event.get():
			#Once again, if the player wants to quit the game, quit the program.
			if event.type == pygame.QUIT:
				quit()










#Global variables:
width = 1024
height = 550 #448

window = define_window(width, height)

clock = pygame.time.Clock()

player = Player()

numCols = 11
enemies = []


player_proj = []
enemy_proj = []


font = pygame.font.SysFont('comicsans', 30, True)

#Main loop:
run()
