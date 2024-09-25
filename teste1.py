def controles():
    wasd = pygame.image.load('imagens\\wasd.png')
    setinhas = pygame.image.load('imagens\\controles.png')
    wasd = pygame.transform.scale_by(wasd,4)
    setinhas = pygame.transform.scale_by(setinhas, 4)

    return setinhas, wasd