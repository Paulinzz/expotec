import pygame
import random

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake The Game")

        self.largura, self.altura = 1560, 760
        self.tela = pygame.display.set_mode((self.largura, self.altura))

        self.relogio = pygame.time.Clock()

        # cores
        self.preta = (0, 0, 0)
        self.branca = (255, 255, 255)
        self.vermelha = (255, 0, 0)
        self.verde = (0, 255, 0)

        self.tamanho_quadrado = 20
        self.velocidade_jogo = 15

        self.rodar_jogo()

    def gerar_comida(self):
        comida_x = round(random.randrange(0, self.largura - self.tamanho_quadrado) / float(self.tamanho_quadrado)) * float(self.tamanho_quadrado) 
        comida_y = round(random.randrange(0, self.altura - self.tamanho_quadrado) / float(self.tamanho_quadrado)) * float(self.tamanho_quadrado) 
        return comida_x, comida_y

    def desenhar_comida(self, comida_x, comida_y):
        pygame.draw.rect(self.tela, self.verde, [comida_x, comida_y, self.tamanho_quadrado, self.tamanho_quadrado])

    def desenhar_cobra(self, pixels):
        for pixel in pixels:
            pygame.draw.rect(self.tela, self.branca, [pixel[0], pixel[1], self.tamanho_quadrado, self.tamanho_quadrado])

    def desenhar_pontuacao(self, pontuacao):
        fonte = pygame.font.SysFont("Helvetica", 35)
        texto = fonte.render(f"Pontos: {pontuacao}", True, self.vermelha)
        self.tela.blit(texto, [1, 1])

    def selecionar_velocidade(self, tecla):
        if tecla == pygame.K_DOWN:
            return 0, self.tamanho_quadrado
        elif tecla == pygame.K_UP:
            return 0, -self.tamanho_quadrado
        elif tecla == pygame.K_RIGHT:
            return self.tamanho_quadrado, 0
        elif tecla == pygame.K_LEFT:
            return -self.tamanho_quadrado, 0
        return None  # retorna None se a tecla não for uma seta

    def ignorar_tecla_nao_seta(self, tecla):
        if tecla not in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT]:
            return True
        return False #se a tecla digitada não é uma seta a cobrinha segue seu rumo até que uma seta seja clicada

    def rodar_jogo(self):
        fim_jogo = False
        x = self.largura / 2
        y = self.altura / 2
        velocidade_x = 0
        velocidade_y = 0
        tamanho_cobra = 1

        pixels = []
        comida_x, comida_y = self.gerar_comida()
        
        while not fim_jogo:
            self.tela.fill(self.preta)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    fim_jogo = True
                elif evento.type == pygame.KEYDOWN:
                    if self.ignorar_tecla_nao_seta(evento.key):
                        continue
                    nova_velocidade = self.selecionar_velocidade(evento.key)
                    if nova_velocidade:
                        velocidade_x, velocidade_y = nova_velocidade

            # atualizar a posição da cobra
            x += velocidade_x
            y += velocidade_y

            # checa se a cobra saiu dos limites da tela
            if x < 0 or x >= self.largura or y < 0 or y >= self.altura:
                fim_jogo = True

            # adiciona a nova posição da cabeça da cobra
            pixels.append([x, y])
            if len(pixels) > tamanho_cobra:
                del pixels[0]
            
            # verifica se a cobra bateu no próprio corpo
            for pixel in pixels[:-1]:
                if pixel == [x, y]:
                    fim_jogo = True

            # desenha elementos na tela
            self.desenhar_comida(comida_x, comida_y)
            self.desenhar_cobra(pixels)
            self.desenhar_pontuacao(tamanho_cobra - 1)

            # atualiza a tela
            pygame.display.update()

            # verifica se a cobra comeu a comida
            if x == comida_x and y == comida_y:
                tamanho_cobra += 1
                comida_x, comida_y = self.gerar_comida()

            self.relogio.tick(self.velocidade_jogo)

        pygame.quit()

if __name__ == "__main__":
    Jogo()
