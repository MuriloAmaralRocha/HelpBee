import pygame
from pygame.locals import *
import sys
import random

pygame.init()

x = 86
y = 250

altura = 600
largura = 300
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Help Bee")

pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.set_volume(0.5)

BG = pygame.image.load('BG.png')
bgY = 0
bgY2 = BG.get_height() * -1

progess_bar = pygame.image.load('progess bar.png')
progess_bar = pygame.transform.scale(progess_bar, (20, 400))
Py = 595

jujuba = pygame.image.load('jujuba.png')
jujuba = pygame.transform.scale(jujuba, (75,128))

Goal = []
goal_anim = pygame.image.load('goal.png')
i = 0
while i < 4: 
  goal_parte = goal_anim.subsurface([0 + i*200, 0, 200, 200])
  goal_parte = pygame.transform.scale(goal_parte, (85,85))
  Goal.append(goal_parte)
  i += 1

Bee = []
bee_movimento = pygame.image.load('bee.png')
bee_movimento.set_colorkey((255, 255, 255))
i = 0
while i < 5: 
  bee_parte = bee_movimento.subsurface([0 + i*200, 0, 200, 200])
  bee_parte = pygame.transform.scale(bee_parte, (128,128))
  Bee.append(bee_parte)
  i += 1

Vida = [pygame.image.load('vida1.png'), pygame.image.load('vida2.png')]


clock = pygame.time.Clock()
hitbox = pygame.Rect(0,0,0,0)
def desenhaProjetil():
    global hitbox, objetos
    for objeto in objetos:
      tela.blit(jujuba, (int(objeto[0]), int(objeto[1])))
      hitbox = pygame.Rect(int(objeto[0])+20, int(objeto[1])+26, 39, 72)
      objeto[2] = hitbox
      ##pygame.draw.rect(tela, (255,0,0), hitbox, 2) ##ver hitbox dos projeteis
        

def desenhaTela():
    n = 0
    global i, j
    tela.blit(BG, (0, int(bgY)))
    tela.blit(BG, (0, int(bgY2)))
    tela.blit(Bee[int(i)], (int(x), int(y)))
    ##pygame.draw.rect(tela, (255,0,0), bee_hitbox, 2) ##ver hitbox da abelha
    desenhaProjetil()
    for z in trataVida():
      tela.blit(pygame.transform.scale(Vida[z], (80,80)), (155 + 40*n, -15))
      n += 1
    tela.blit(progess_bar, (5, 200))
    pygame.draw.line(tela, (0, 0, 0), (10, Py), (20, Py), 3)
    tela.blit(Goal[int(j)], (-26, 157))
    pygame.display.update()

def trataVida():
    global vidas
    if vidas == 3:
      l = [0, 0, 0]
    elif vidas == 2:
      l = [0, 0, 1]
    elif vidas == 1:
      l = [0, 1, 1]
    else:
      l = [1, 1, 1]
    return l

def telaFim():
    global vidas, passo, objetos, x, y, Py
    objetos = []
    speed = 30
    x = 86
    y = 250
    Py = 595
  
    run = True
    while run:
      pygame.time.delay(100)
      for event in pygame.event.get():
          if event.type == QUIT:
            pygame.quit()
            quit()
          if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
              run = False
              vidas = 3
      tela.blit(BG, (0,0))
      fonteGrande = pygame.font.SysFont('Arial', 40)
      fontePequena = pygame.font.SysFont('Arial', 18)
      lose = fonteGrande.render('Você perdeu', False, (0, 0, 0))
      win = fonteGrande.render('Você ganhou!', False, (0, 0, 0))
      play = fontePequena.render('Aperte espaço para jogar novamente', False, (0, 0, 0))
      if vidas < 1:
        tela.blit(lose, (55,200))
        tela.blit(play, (35,400))
      else:
        tela.blit(win, (55,200))
        tela.blit(play, (35,400))
      pygame.display.update()
        

i = 0.01
j = 0.01
pygame.time.set_timer(USEREVENT+2,random.randrange(3000, 5000))
pygame.time.set_timer(USEREVENT+1,250)
passo = 30
objetos = []
vidas = 3

pygame.mixer.music.play(-1)
run = True
while run:
    if vidas < 1:
        telaFim()
    trataVida()
  
    bee_hitbox = pygame.Rect(int(x)+50, int(y)+40, 30, 60)  
    bgY += 1.4
    bgY2 += 1.4
    if bgY > BG.get_height():
       bgY = BG.get_height() * -1
    if bgY2 > BG.get_height():
       bgY2 = BG.get_height() * -1
       
    Teclas = pygame.key.get_pressed()
    if Teclas[K_UP] and y > -30:
      y = y - 2.8
    if Teclas[K_DOWN] and y < 500:
      y = y + 2.8
    if Teclas[K_LEFT] and x > -40:
      x = x - 2.8
    if Teclas[K_RIGHT] and x < 210:
      x = x + 2.8


    for objeto in objetos:
      if objeto[1] > 600:
        objetos.pop(objetos.index(objeto))
      if bee_hitbox.colliderect(objeto[2]):
        objetos.pop(objetos.index(objeto))
        vidas -= 1
      objeto[1] += 2.
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT+1:
          passo += 2
          if Py > 277:
            Py -= 1
          else:
            telaFim()
        if event.type == USEREVENT+2:
          objetos.append([random.randrange(0,225), -128, hitbox])
            

    i = i + 0.2
    if i > 4.9:
        i = 0
        
    j = j + 0.15
    if j > 3.9:
        j = 0
    clock.tick(passo)
    desenhaTela()
