import pygame

from abc import ABCMeta, abstractmethod
from random import choice


#Metodos calcular_regras servem para validar movimentos dos personagens pelo cenario e para definir o proximo movimento dos personagens
#Metodos pintar servem para pintar os objetos na tela
#Metodos processar_eventos servem para avaliar eventos como: se apertou para sair, pressionou e soltou uma tecla, qual a tecla pressionada, etc
pygame.init()

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
LARANJA = (255, 140, 0)
ROSA = (255, 15, 192)
CIANO = (0, 255, 255)

COMPRIMENTO_TELA = 1500
ALTURA_TELA = 830

CIMA = pygame.K_UP
BAIXO = pygame.K_DOWN
ESQUERDA = pygame.K_LEFT
DIREITA = pygame.K_RIGHT

DIRECAO_ACIMA = 1
DIRECAO_ABAIXO = 2
DIRECAO_DIREITA = 3
DIRECAO_ESQUERDA = 4
fonte = pygame.font.SysFont("arial", 48, True, False)

screen = pygame.display.set_mode((COMPRIMENTO_TELA, ALTURA_TELA), 0)

class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass
    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass
    @abstractmethod
    def esquina(self, direcoes):
        pass

class Placar:
    def __init__(self, Cenario):
        self.cenario = Cenario


    def exibir_placar(self, tela):
        placar = f"Score:   {cenario.pontos}"
        vidas = f"Vidas:    {cenario.vidas}"
        imagem_score = fonte.render(placar, True, AMARELO)
        imagem_vidas = fonte.render(vidas, True, AMARELO)
        tela.blit(imagem_score, (int(COMPRIMENTO_TELA / 2 * 1.2), 100))
        tela.blit(imagem_vidas, (int(COMPRIMENTO_TELA / 2 * 1.2), 150))

class Cenario(ElementoJogo):

    def __init__(self, tamanho, PACMAN):
        self.pacman = PACMAN
        self.moviveis = []
        self.pontos = 0
        # Estados possíveis: 0-Jogando; 1-Pausado; 2-Game Over; 3-Vitória
        self.estado = "Jogando"
        self.tamanho = tamanho
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
        self.vidas = 5
        
    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)
    def processar_eventos(self, eventos):
        for e in eventos:
            if pygame.QUIT == e.type:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.estado == "Jogando":
                        self.estado = "Pausado"
                    else:
                        self.estado = "Jogando"

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            cor = PRETO
            half = self.tamanho // 2
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, AMARELO, (x + half, y + half), self.tamanho // 10, 0)

    def pintar(self, tela):
        if self.estado == "Jogando":
            self.pintar_jogando(tela)
        elif self.estado == "Pausado":
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == "Game Over":
            self.pintar_jogando(tela)
            self.pintar_gameOver(tela)
        elif self.estado == "Vitoria":
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "GG IZI!!!")


    def pintar_texto_centro(self, tela, texto):
        texto_pausado = fonte.render(texto, True, AMARELO)
        pausado_x = (tela.get_width() - texto_pausado.get_width()) // 2
        pausado_y = (tela.get_height() - texto_pausado.get_height()) // 2
        tela.blit(texto_pausado, (pausado_x, pausado_y))

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S A D O")

    def pintar_gameOver(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R")

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha-1)][int(coluna)] != 2:
            direcoes.append(DIRECAO_ACIMA)
        if self.matriz[int(linha+1)][int(coluna)] != 2:
            direcoes.append(DIRECAO_ABAIXO)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIRECAO_DIREITA)
        if self.matriz[int(linha)][int(coluna-1)] != 2:
            direcoes.append(DIRECAO_ESQUERDA)
        return direcoes

    def calcular_regras(self):
        if self.estado == "Jogando":
            self.calcular_regras_jogando()
        elif self.estado == "Pausado":
            self.calcular_regras_pausado()
        elif self.estado == "Game Over":
            self.calcular_regras_gameOver()
        elif self.estado == "Vitoria":
            self.calcular_regras_vitoria()

    def calcular_regras_gameOver(self):
        pass

    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)

            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)

            direcoes = self.get_direcoes(lin, col)

            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and \
                movivel.coluna == self.pacman.coluna:
                self.vidas -= 1
                if self.vidas == 0:
                    self.estado = "Game Over"
                else:
                    self.pacman.linha = 1
                    self.pacman.coluna = 1

            if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and self.matriz[lin_intencao][col_intencao] != 2:
                movivel.aceitar_movimento()
                if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                    self.pontos += 1
                    self.matriz[lin][col] = 0
                    if self.pontos >= 306:
                        self.estado = "Vitoria"
            else:
                movivel.recusar_movimento(direcoes)

    def calcular_regras_pausado(self):
        for movivel in self.moviveis:
            lin = movivel.linha
            col = movivel.coluna
            direcoes = self.get_direcoes(lin, col)
            movivel.recusar_movimento(direcoes)
        pass

    def calcular_regras_vitoria(self):
        pass


class Pacman(ElementoJogo, Movivel):


    def __init__(self, tamanho):
        self.VELOCIDADE = 1
        self.coluna = 1
        self.linha = 1
        self.centro_x = 0
        self.centro_y = 0
        self.tamanho = tamanho
        self.raio = self.tamanho // 2
        self.VELOCIDADE_x = 0
        self.VELOCIDADE_y = 0
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura_boca = 0
        self.velocidade_abertura_boca = 3


    def pintar(self, tela):

        # Desenhar o corpo do Pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        # Desenho da boca do Pacman

        self.abertura_boca += self.velocidade_abertura_boca
        if self.abertura_boca > self.raio:
            self.velocidade_abertura_boca = -self.velocidade_abertura_boca
        elif self.abertura_boca <=0:
            self.velocidade_abertura_boca = -self.velocidade_abertura_boca

        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura_boca)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura_boca)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # Olho do Pacman
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def calcular_regras(self):

        self.coluna_intencao = self.coluna + self.VELOCIDADE_x
        self.linha_intencao = self.linha + self.VELOCIDADE_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == DIREITA:
                    self.VELOCIDADE_x = self.VELOCIDADE
                elif e.key == ESQUERDA:
                    self.VELOCIDADE_x = -self.VELOCIDADE
                elif e.key == CIMA:
                    self.VELOCIDADE_y = -self.VELOCIDADE
                elif e.key == BAIXO:
                    self.VELOCIDADE_y = self.VELOCIDADE
            elif e.type == pygame.KEYUP:
                if e.key == DIREITA:
                    self.VELOCIDADE_x = 0
                elif e.key == ESQUERDA:
                    self.VELOCIDADE_x = 0
                elif e.key == CIMA:
                    self.VELOCIDADE_y = 0
                elif e.key == BAIXO:
                    self.VELOCIDADE_y = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao


    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def processar_mouse(self, eventos):
        delay = 50

        for e in eventos:
            if e.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = e.pos
                self.coluna = (mouse_x + self.centro_x) // delay
                self.linha = (mouse_y + self.centro_y) // delay

    def esquina(self, direcoes):
        pass

class Fantasma(ElementoJogo):
    def __init__(self, cor, tamanho):
        self.velocidade = 1
        self.direcao = DIRECAO_ABAIXO
        self.coluna = 14
        self.linha = 13
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.cor = cor
        self.tamanho = tamanho

    def pintar(self, tela):

        ##Desenhar o corpo do fantasma
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contornos = [(px, py+self.tamanho),
                    (px + fatia, py + fatia),
                    (px + fatia * 2, py + fatia//2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px+ fatia*6, py + fatia//2),
                    (px + fatia * 7, py + fatia*2),
                    (px + self.tamanho, py+ self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contornos, 0)

        ##Desenhar olhos
        raio_olho_externo = fatia // 1.5
        raio_olho_interno = fatia // 2

        ##Pontos do olho esquerdo
        olho_esquerdo_x = int(px + fatia * 2.5)
        olho_esquerdo_y = int(py + fatia * 2.5)

        ##Pontos do olho direito

        olho_direito_x = int(px + fatia * 5.5)
        olho_direito_y = int(py + fatia * 2.5)

        #Desenho dos dois olhos
        pygame.draw.circle(tela, BRANCO, (olho_esquerdo_x, olho_esquerdo_y), raio_olho_externo, 0)
        pygame.draw.circle(tela, PRETO, (olho_esquerdo_x, olho_esquerdo_y), raio_olho_interno, 0)
        pygame.draw.circle(tela, BRANCO, (olho_direito_x, olho_direito_y), raio_olho_externo, 0)
        pygame.draw.circle(tela, PRETO, (olho_direito_x, olho_direito_y), raio_olho_interno, 0)

    def processar_eventos(self, eventos):
        pass

    def mudar_direcao(self, direcoes):
        self.direcao = choice(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def calcular_regras(self):

        if self.direcao == DIRECAO_ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == DIRECAO_ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == DIRECAO_ESQUERDA:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == DIRECAO_DIREITA:
            self.coluna_intencao += self.velocidade
    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

if __name__ == "__main__":
    size = ALTURA_TELA // 30
    pacman = Pacman(size)
    fantasma_vermelho = Fantasma(VERMELHO, size)
    fantasma_laranja = Fantasma(LARANJA,size)
    fantasma_rosa = Fantasma(ROSA, size)
    fantasma_ciano = Fantasma(CIANO, size)
    cenario = Cenario(size, pacman)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(fantasma_vermelho)
    cenario.adicionar_movivel(fantasma_ciano)
    cenario.adicionar_movivel(fantasma_rosa)
    cenario.adicionar_movivel(fantasma_laranja)

    placar = Placar(cenario)

    while True:
        #time.sleep(5)
        # Calcular Regras

        pacman.calcular_regras()
        fantasma_vermelho.calcular_regras()
        fantasma_ciano.calcular_regras()
        fantasma_rosa.calcular_regras()
        fantasma_laranja.calcular_regras()
        cenario.calcular_regras()
        # Pintar a tela

        screen.fill(PRETO)
        cenario.pintar(screen)
        pacman.pintar(screen)
        placar.exibir_placar(screen)
        fantasma_vermelho.pintar(screen)
        fantasma_laranja.pintar(screen)
        fantasma_ciano.pintar(screen)
        fantasma_rosa.pintar(screen)
        pygame.display.update()
        pygame.time.delay(60)

        # Detectar Eventos
        eventos = pygame.event.get()

        # pacman.processar_mouse(eventos)
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)

