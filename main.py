# This is the code for the game


import random   
import time
import pygame
pygame.init()

# CONSTANTS
MAP_NUMBER = 3
MESSAGE_NUMBER = 0
PLAYER_HP = 10000
VIRUS_DMG = 5
PARTICLE_DMG = 5
VIRUS_POINTS = 5

PLAYING = 0
PAUSED = 1
GAME_OVER = 2
TEST_MODE = 3
game_state = PLAYING

WIDTH = 800
HEIGHT = 600

pygame.display.set_mode()
logo = pygame.image.load("logo.jpg")
pygame.display.set_icon(logo)

messageList = ["THE BLOODSTREAM", "THE BRAIN", "THE LUNGS", "THE HEART"]
pygame.display.set_caption("  VIRUS HUNTER   HP: " + str(PLAYER_HP) + "  POINTS: 0  "  + messageList[MESSAGE_NUMBER])

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
clock.tick(60)
running = True

dirArr = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
ships = {}
redships = {}

for dir in dirArr:
  image = pygame.image.load("pic/blueship/blueship" + dir + ".png").convert_alpha()
  image = pygame.transform.scale(image, (100, 100))
  ships[dir] = image

for dir in dirArr:
  image = pygame.image.load("pic/redship/redship" + dir + ".png").convert_alpha()
  image = pygame.transform.scale(image, (100, 100))
  redships[dir] = image

gameover_image = pygame.image.load("backgrounds/gameOver.jpg").convert_alpha()
gameover_image = pygame.transform.scale(gameover_image, (WIDTH,HEIGHT))

ebola = pygame.image.load("pic/virus/ebola.png").convert_alpha()
ebola = pygame.transform.scale(ebola, (50,50))

influenzaImage = pygame.image.load("pic/virus/influenza.png").convert_alpha()
influenzaImage = pygame.transform.scale(influenzaImage, (75,75))

ebolaInfo = pygame.image.load("pic/slides/ebolaInfo.png").convert_alpha()
ebolaInfo = pygame.transform.scale(ebolaInfo, (WIDTH, HEIGHT))

blueParticle = pygame.image.load("pic/blueParticle.png").convert_alpha()
blueParticle = pygame.transform.scale(blueParticle, (100, 100))
redParticle = pygame.image.load("pic/redParticle.png").convert_alpha()
redParticle = pygame.transform.scale(redParticle, (100, 100))
particleGroup = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
  def __init__(self, playerHp, playerPoints):
    pygame.sprite.Sprite.__init__(self)

    self.playerHp = playerHp
    self.playerPoints = playerPoints
    
    self.attackMode = "BLUE"
    self.dir = "E"
    self.image = ships[self.dir] if (self.attackMode == "BLUE") else redships[self.dir]
    
    self.rect = self.image.get_rect()
    self.rect.center = 50, 50
    self.xSpeed = 0
    self.ySpeed = 0
  
  def move(self, dir):
    # time.sleep(0.01)
    acceleration = 3
    self.xSpeed *= 0.7
    self.ySpeed *= 0.7

    if dir == "N":
      self.ySpeed -= acceleration
    elif dir == "S":
      self.ySpeed += acceleration
    elif dir == "W":
      self.xSpeed -= acceleration
    elif dir == "E":
      self.xSpeed += acceleration
    elif dir == "NW":
      self.ySpeed -= acceleration
      self.xSpeed -= acceleration
    elif dir == "NE":
      self.ySpeed -= acceleration
      self.xSpeed += acceleration
    elif dir == "SW":
      self.ySpeed += acceleration
      self.xSpeed -= acceleration
    elif dir == "SE":
      self.ySpeed += acceleration
      self.xSpeed += acceleration
    
    self.image = ships[dir] if (self.attackMode == "BLUE") else redships[dir]
    self.dir = dir
    self.rect.x += self.xSpeed
    self.rect.y += self.ySpeed
    self.rect.clamp_ip(screen.get_rect()) # this line keeps the sprite inside the screen

  def shoot(self):
    if self.attackMode == "BLUE":
      particle = Particle(self.rect.x, self.rect.y, self.dir, self.attackMode)
      particleGroup.add(particle)
    elif self.attackMode == "RED":
      index = dirArr.index(self.dir)
      prev_index = (index - 1) % len(dirArr)
      next_index = (index + 1) % len(dirArr)
      
      particle1 = Particle(self.rect.x, self.rect.y, dirArr[index], self.attackMode)
      particle2 = Particle(self.rect.x, self.rect.y, dirArr[prev_index], self.attackMode)
      particle3 = Particle(self.rect.x, self.rect.y, dirArr[next_index], self.attackMode)

      particleGroup.add(particle1)
      particleGroup.add(particle2)
      particleGroup.add(particle3)

  def changeMode(self):
    self.attackMode = "RED" if (self.attackMode == "BLUE") else "BLUE"
    self.image = ships[self.dir] if (self.attackMode == "BLUE") else redships[self.dir]
    
class Particle(pygame.sprite.Sprite):
  def __init__(self, x, y, dir, attackMode):
    pygame.sprite.Sprite.__init__(self)
    self.parentX = x
    self.parentY = y
    self.dir = dir
    self.attackMode = attackMode

    self.image = blueParticle if (attackMode == "BLUE") else redParticle
    self.rect = self.image.get_rect()

    particleOffset = 60
    xOffset = 0
    yOffset = 0

    if self.dir == "N":
      yOffset = -particleOffset
    elif self.dir == "S":
      yOffset = particleOffset
    elif self.dir == "W":
      xOffset = -particleOffset
    elif self.dir == "E":
      xOffset = particleOffset
    elif self.dir == "NW":
      yOffset = -particleOffset / 2
      xOffset = -particleOffset / 2
    elif self.dir == "NE":
      yOffset = -particleOffset / 2
      xOffset = particleOffset / 2
    elif self.dir == "SW":
      yOffset = particleOffset / 2
      xOffset = -particleOffset / 2
    elif self.dir == "SE":
      yOffset = particleOffset / 2
      xOffset = particleOffset / 2
      
    self.rect.x = x + xOffset
    self.rect.y = y + yOffset

  def move(self):
    particleSpeed = 25

    if self.dir == "N":
      self.rect.y -= particleSpeed
    elif self.dir == "S":
      self.rect.y += particleSpeed
    elif self.dir == "W":
      self.rect.x -= particleSpeed
    elif self.dir == "E":
      self.rect.x += particleSpeed
    elif self.dir == "NW":
      self.rect.y -= particleSpeed
      self.rect.x -= particleSpeed
    elif self.dir == "NE":
      self.rect.y -= particleSpeed
      self.rect.x += particleSpeed
    elif self.dir == "SW":
      self.rect.y += particleSpeed
      self.rect.x -= particleSpeed
    elif self.dir == "SE":
      self.rect.y += particleSpeed
      self.rect.x += particleSpeed

    if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT or self.rect.y < 0:
      self.kill()

    distanceFromParent = ((self.rect.x - self.parentX) ** 2 + (self.rect.y - self.parentY) ** 2)

    if distanceFromParent > 3 * (particleSpeed ** 3):
      self.kill()


class pillGoodie(pygame.sprite.Sprite):
   def __init__(self, image,x,y):
     pygame.sprite.Sprite.__init__(self)
     self.image = pygame.image.load(image).convert_alpha()
     self.image = pygame.transform.scale(self.image, (50, 50))
     self.rect = self.image.get_rect()
     self.rect.x = x
     self.rect.y = y

pillGroup = pygame.sprite.Group()




class Virus(pygame.sprite.Sprite):
  def __init__(self, image, health):
    pygame.sprite.Sprite.__init__(self)
    self.image = image
    self.image = pygame.transform.scale_by(self.image, health / 10)
    self.health = health
    self.ogHealth = health
    self.flag = -40
    self.rect = self.image.get_rect()
    
    # spawn point
    # range = random.choice([[50,150],[450,550]])
    # range2 = random.choice([[50,150],[650,750]])
    # x = random.randint(range[0],range[1])
    # y = random.randint(range2[0],range2[1])
    
    # self.rect.center = 400,300

    self.speedY = random.choice([-2,2])
    self.speedX = random.choice([-2,2])
    
  # def move(self):
  #   speed = 0.2
  #   if self.flag > 0:  #if flag is postive
  #     self.rect.y -= speed      
  #     self.flag -= 1
  #     if self.flag == 0:
  #       self.flag = -40
  #   if self.flag < 0:  #if flag is negative
  #     self.rect.y += speed     
  #     self.flag += 1
  #     if self.flag == 0:
  #       self.flag = 40
  #   if self.flag > 0:  #if flag is postive
  #     self.rect.x -= speed      
  #     self.flag -= 1
  #     if self.flag == 0:
  #       self.flag = -40
  #   if self.flag < 0:  #if flag is negative
  #     self.rect.x += speed     
  #     self.flag += 1
  #     if self.flag == 0:
  #       self.flag = 40
    self.rect.clamp_ip(screen.get_rect())
    
  def move(self):
    if self.rect.top <= 50:
      self.speedY *= -1
      self.rect.top = 51
    
    if self.rect.bottom >= HEIGHT - 50:
      self.speedY *= -1
      self.rect.bottom = HEIGHT - 51
    
    if self.rect.left <= 50:
      self.speedX *= -1
      self.rect.left = 51
    
    if self.rect.right >= WIDTH - 50:
      self.speedX *= -1
      self.rect.right = WIDTH - 51

    self.rect.y += self.speedY 
    self.rect.x += self.speedX

class Ebola(Virus):
  def __init__(self, health, x, y): 
    super().__init__(ebola, health)
    self.rect.center = x, y
    
class Influenza(Virus):
  def __init__(self, health, x, y):
    super().__init__(influenzaImage, health)
    self.rect.center = x, y
 
group = pygame.sprite.Group()  #we need to add sprite to groups to show them on the screen
p1 = Player(2000, 0)
group.add(p1)

virusGroup = pygame.sprite.Group()

def draw_text(surf, text, size, x, y):
  font = pygame.font.Font( pygame.font.match_font('comic sans ms'), size)
  text_surface = font.render (text, True, (255,255,255))
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x, y)
  surf.blit(text_surface, text_rect)

def displayHelper(image):
  
  while True: 
      breakFlag = False
      newScreen = pygame.image.load(image).convert_alpha()
      newScreen = pygame.transform.scale(newScreen, (WIDTH, HEIGHT)) 
      pygame.display.set_caption("  VIRUS HUNTER " + " Press Enter to continue!")
      screen.blit(newScreen, (0,0))  
      pygame.display.flip()

      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
              breakFlag = True
              break

      if(breakFlag):
        break


# while True:
#     breakFlag = False
#     startScreen = pygame.image.load("virusHunter.png").convert_alpha()
#     startScreen = pygame.transform.scale(startScreen, (WIDTH, HEIGHT)) 
#     screen.blit(startScreen, (0,0))
#     pygame.display.flip()

#     for event in pygame.event.get():
#       if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#          breakFlag = True
#          break

#     if breakFlag:
#       break

displayHelper("virusHunter.png")

numFlu = 5
numEbola = 2
for _ in range(numFlu):
  randFlu = Influenza(20, random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
  virusGroup.add(randFlu)

for _ in range(numEbola):
  randEbola = Ebola(40, random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
  virusGroup.add(randEbola)

for _ in range(2): #pills
    randPill = pillGoodie("pill.png",random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
    pillGroup.add(randPill)
  
length = numFlu + numEbola

displayFlag = True

while running:
  if (MAP_NUMBER == 1 and displayFlag):
    displayHelper("pic/slides/ebolaInfo.png")
    displayHelper("pic/slides/influenzaInfo.png")
    displayFlag = False
    
  #print(length)
  
  if (length == 0):
      
    MAP_NUMBER += 1

    # if (MAP_NUMBER == 5):
    #    winScreen = "winScreen.png"
    #    winScreen_surface = pygame.image.load(winScreen).convert_alpha()
    #    winScreen_surface= pygame.transform.scale(winScreen_surface, (WIDTH, HEIGHT))
    #    pygame.display.flip()
    #    time.sleep(8)
    #    break
      
    p1.playerHp = 10000
    displayFlag = True
    MESSAGE_NUMBER += 1
    pygame.display.set_caption("  VIRUS HUNTER   HP: " + str(p1.playerHp) + "  POINTS: " + str(p1.playerPoints) +  "  "  + messageList[MESSAGE_NUMBER])

    if (MAP_NUMBER <= 4):
      loading_background = "loadingScreen" + str(MAP_NUMBER) + ".png"
      loading_background_surface = pygame.image.load(loading_background).convert_alpha()
      loading_background_surface= pygame.transform.scale(loading_background_surface, (WIDTH, HEIGHT)) 
    else:
      loading_background = "winScreen.png"
      loading_background_surface = pygame.image.load(loading_background).convert_alpha()
      loading_background_surface= pygame.transform.scale(loading_background_surface, (WIDTH, HEIGHT)) 
      screen.blit(loading_background_surface, (0, 0))
      pygame.display.flip()
      time.sleep(8)
      break
    
    screen.blit(loading_background_surface, (0, 0))
    pygame.display.flip()
    time.sleep(5)

    if (MAP_NUMBER == 2):
      numFlu = 2
      numEbola = 2
      for _ in range(numFlu):
        randFlu = Influenza(20, random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        virusGroup.add(randFlu)
  
      for _ in range(numEbola):
        randEbola = Ebola(40, random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        virusGroup.add(randEbola)

      for _ in range(4): #pills
        randPill = pillGoodie("pill.png",random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        pillGroup.add(randPill)

      length = numFlu + numEbola;
    elif (MAP_NUMBER == 3):
      numFlu = 5
      numEbola = 3
      for _ in range(numFlu):
        randFlu = Influenza(20, random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        virusGroup.add(randFlu)

      for _ in range(numEbola):
        randEbola = Ebola(40, random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        virusGroup.add(randEbola)

      for _ in range(6): #pills
        randPill = pillGoodie("pill.png",random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        pillGroup.add(randPill)

      length = numFlu + numEbola
    elif (MAP_NUMBER == 4):
      numFlu = 7
      numEbola = 6
      for _ in range(numFlu):
        randFlu = Influenza(20, random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        virusGroup.add(randFlu)

      for _ in range(numEbola):
        randEbola = Ebola(40, random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        virusGroup.add(randEbola)

      for _ in range(6): #pills
        randPill = pillGoodie("pill.png",random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        pillGroup.add(randPill)

      length = numFlu + numEbola
  
  if game_state == GAME_OVER:
    screen.blit(gameover_image, (0, 0))
    pygame.display.flip()
    time.sleep(7)
    break
  
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        game_state = PLAYING
      if event.key == pygame.K_e:
        p1.changeMode()
      
  keys = pygame.key.get_pressed()
  UP = keys[pygame.K_UP] or keys[pygame.K_w]
  DOWN = keys[pygame.K_DOWN] or keys[pygame.K_s]
  LEFT = keys[pygame.K_LEFT] or keys[pygame.K_a]
  RIGHT = keys[pygame.K_RIGHT] or keys[pygame.K_d]
  SPACE = keys[pygame.K_SPACE]

  # keysArr = [UP, DOWN, LEFT, RIGHT, SPACE]

  # print(keysArr)
  
  if UP and not (DOWN or LEFT or RIGHT):
    p1.move("N")
  elif DOWN and not (UP or LEFT or RIGHT):
    p1.move("S")
  elif LEFT and not (UP or DOWN or RIGHT):
    p1.move("W")
  elif RIGHT and not (UP or DOWN or LEFT):
    p1.move("E")
  elif UP and LEFT:
    p1.move("NW")
  elif UP and RIGHT:
    p1.move("NE")
  elif DOWN and LEFT:
    p1.move("SW")
  elif DOWN and RIGHT:
    p1.move("SE")
  elif SPACE:
    p1.shoot()

  if game_state in (PLAYING, TEST_MODE):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    new_background = "backgrounds/back_ground" + str(MAP_NUMBER) + ".jpg"
    new_background_surface = pygame.image.load(new_background)
    new_background_surface = pygame.transform.scale(new_background_surface, (WIDTH, HEIGHT))
  
    screen.blit(new_background_surface, (0,0))
    particleGroup.draw(screen)
    pillGroup.draw(screen)
    virusGroup.draw(screen)
    group.draw(screen)

    for p in pillGroup:
        if (p.rect.colliderect(p1.rect)):
          pillGroup.remove(p)
          if (p1.playerHp<10000):
            p1.playerHp+=2000
            
          pygame.display.set_caption("  VIRUS HUNTER   HP: " + str(p1.playerHp) + "  POINTS: " + str(p1.playerPoints) +  "  "  + messageList[MESSAGE_NUMBER])
      

    for v in virusGroup:
      v.move()
      if v.rect.colliderect(p1.rect):  # TOUCHES VIRUS
        #if (game_state != TEST_MODE):
          #game_state = PAUSED
        
        p1.playerHp -= VIRUS_DMG
        pygame.display.set_caption("  VIRUS HUNTER   HP: " + str(p1.playerHp) + "  POINTS: " + str(p1.playerPoints) +  "  "  + messageList[MESSAGE_NUMBER])

      if (p1.playerHp <= 0 and game_state != TEST_MODE):
          game_state = GAME_OVER
      
      for i in particleGroup:
        if v.rect.colliderect(i.rect):
          v.health -= (PARTICLE_DMG if (i.attackMode == "BLUE") else PARTICLE_DMG // 4)
          i.kill()
  
      if (v.health <= 0):
        p1.playerPoints += VIRUS_POINTS
        pygame.display.set_caption("  VIRUS HUNTER   HP: " + str(p1.playerHp) + "  POINTS: " + str(p1.playerPoints) +  "  "  + messageList[MESSAGE_NUMBER])
        if v.ogHealth // 2 > PARTICLE_DMG: # not one-shottable
          if isinstance(v, Ebola):
            virusGroup.add(Ebola(v.ogHealth // 2, v.rect.centerx, v.rect.centery))
            virusGroup.add(Ebola(v.ogHealth // 2, v.rect.centerx, v.rect.centery))
            virusGroup.add(Ebola(v.ogHealth // 2, v.rect.centerx, v.rect.centery))
            virusGroup.add(Ebola(v.ogHealth // 2, v.rect.centerx, v.rect.centery))

            length += 4
          if isinstance(v, Influenza):
            virusGroup.add(Influenza(v.ogHealth // 2, v.rect.centerx, v.rect.centery))
            virusGroup.add(Influenza(v.ogHealth // 2, v.rect.centerx, v.rect.centery))

            length += 2
        v.kill()
        length -= 1
          
    for i in particleGroup:
      i.move()
      
    pygame.display.flip()
    
    # clock.tick(60)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    # dt = clock.tick(60) / 1000

pygame.quit()
