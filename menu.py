#menu.py

import pygame, sys

def mostrar_menu(pantalla, ANCHO, ALTO):
    try:
        fondo_menu = pygame.image.load("imagenes/fondo3.jpg").convert()
        fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
    except:
        fondo_menu = pygame.Surface((ANCHO, ALTO))
        fondo_menu.fill((0, 0, 0))

    try:
        imagen_titulo = pygame.image.load("imagenes/titulo.png").convert_alpha()
        imagen_titulo = pygame.transform.scale(imagen_titulo, (ANCHO, ALTO))
        rect_titulo = imagen_titulo.get_rect(topleft=(0, 0))
    except:
        imagen_titulo = None

    fuente_inst = pygame.font.SysFont("Arial", 45, bold=True)
    
    # Pre-renderizado de los textos del menú para que no se procesen en el bucle
    texto = "Presiona ESPACIO para jugar"
    surf_sombra = fuente_inst.render(texto, True, (20, 20, 20))
    surf_texto = fuente_inst.render(texto, True, (255, 255, 255))
    rect_texto = surf_texto.get_rect(center=(ANCHO // 2, ALTO * 0.85))
    
    reloj = pygame.time.Clock()

    while True:
        pantalla.blit(fondo_menu, (0, 0))

        if imagen_titulo:
            pantalla.blit(imagen_titulo, rect_titulo)

        # Dibujamos las superficies pre-renderizadas
        pantalla.blit(surf_sombra, (rect_texto.x + 3, rect_texto.y + 3))
        pantalla.blit(surf_texto, rect_texto)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return 
        
        reloj.tick(60)