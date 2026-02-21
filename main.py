import pygame, sys

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.imagen_original = pygame.image.load("imagenes/PATO DEFINITIVO.jpeg").convert()
        
        
        color_fondo = self.imagen_original.get_at((0,0))
        self.imagen_original.set_colorkey(color_fondo)
        
        self.image = pygame.transform.scale(self.imagen_original, (100, 100))
        self.rect = self.image.get_rect() 
        self.rect.center = (200, 300)

        self.velocidad = 0 
        self.gravedad = 0.25
        self.salto = -6

    def update(self):
        self.velocidad += self.gravedad 
        self.rect.y += self.velocidad

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocidad = 3 

        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.velocidad = 0

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]: 
            self.velocidad = self.salto

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pato Volador")

reloj = pygame.time.Clock()
FPS = 60 


fondo = pygame.image.load("imagenes/fondo super definitivo.jpg").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
posicion_fondo = 0 

todos_los_sprites = pygame.sprite.Group()
jugador = Jugador()
todos_los_sprites.add(jugador)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    posicion_fondo -= 2
    if posicion_fondo <= -ANCHO:
        posicion_fondo = 0 

    
    pantalla.blit(fondo, (posicion_fondo, 0))
    pantalla.blit(fondo, (posicion_fondo + ANCHO, 0))

    todos_los_sprites.update()
    todos_los_sprites.draw(pantalla)
    
    pygame.display.flip()
    reloj.tick(FPS)