import pygame

tela = (255,255,255)

def controles():
    wasd = pygame.image.load('imagens\\wasd.png')
    setinhas = pygame.image.load('imagens\\controles.png')
    wasd = pygame.transform.scale_by(wasd,4)
    setinhas = pygame.transform.scale_by(setinhas, 4)

    return setinhas, wasd


setinhas, wasd = controles()
tela.blit(wasd, (420, 300))  # Exibindo a imagem wasd
tela.blit(setinhas, (520, 300))  # Exibindo a imagem setinhas
