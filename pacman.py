import pygame
#import time

AMARELO = (255, 255, 9)
PRETO = (0,0,0)
COMPRIMENTO = 640
ALTURA = 480
pygame.init()
posiX_rect = 200
posiY_rect = 200

tela = pygame.display.set_mode((COMPRIMENTO, ALTURA), 0)
x = 20
y = 240
VELOCIDADE = 0.2
velocidade_x = VELOCIDADE
velocidade_y = VELOCIDADE
RAIO_BOLINHA = 50
#Retangulo = pygame.Rect(tela, AMARELO,(200, 200,100,100), 5)
while True:


    # calcula regras
    x += velocidade_x
    y += velocidade_y
    if x+RAIO_BOLINHA > COMPRIMENTO:
        velocidade_x = -VELOCIDADE
    if x-RAIO_BOLINHA<0:
        velocidade_x = VELOCIDADE
    if y+RAIO_BOLINHA > ALTURA:
        velocidade_y = -VELOCIDADE
    if y-RAIO_BOLINHA<0:
        velocidade_y = VELOCIDADE
    # pinta
    tela.fill(PRETO)
    pygame.draw.circle(tela, AMARELO, (int(x), int(y)), RAIO_BOLINHA, 5)
    pygame.draw.rect(tela, AMARELO,(200, 200,100,100), 5)
    pygame.display.update()
    # eventos
    for e in pygame.event.get():
        if pygame.QUIT == e.type:
            exit()
