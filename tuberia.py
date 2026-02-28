import pygame, random

class Tuberia(pygame.sprite.Sprite):
    def __init__(self, x, espacio, imagen): 
        super().__init__() 
        self.imagen_tubo = imagen
        self.imagen_tubo_invertido = pygame.transform.flip(self.imagen_tubo, False, True)
        self.altura = random.randint(150, 300)
        self.espacio = espacio
        self.velocidad = 4
        self.tubo_arriba = self.imagen_tubo_invertido.get_rect(midbottom=(x, self.altura))
        self.tubo_abajo = self.imagen_tubo.get_rect(midtop=(x, self.altura + self.espacio))
        self.contado = False

    def update(self):
        self.tubo_abajo.x -= 2
        self.tubo_arriba.x -= 2

    def draw(self, pantalla):
        pantalla.blit(self.imagen_tubo_invertido, self.tubo_arriba)
        pantalla.blit(self.imagen_tubo, self.tubo_abajo)

    def mover(self):
        self.tubo_arriba.x -= self.velocidad
        self.tubo_abajo.x -= self.velocidad

    def fuera_de_pantalla(self):
        return self.tubo_arriba.right < 0
