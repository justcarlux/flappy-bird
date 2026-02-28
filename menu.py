import pygame, sys

def mostrar_menu(pantalla, ANCHO, ALTO):
    # 1. Cargar el fondo (opcional, por si la imagen tiene transparencias)
    try:
        fondo_menu = pygame.image.load("imagenes/fondo3.jpg").convert()
        fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
    except:
        fondo_menu = None

    # 2. Cargar el título y FORZAR que abarque TODA la pantalla
    try:
        imagen_titulo = pygame.image.load("imagenes/titulo.png").convert_alpha()
        # Aquí forzamos las dimensiones exactas de la ventana
        imagen_titulo = pygame.transform.scale(imagen_titulo, (ANCHO, ALTO))
        rect_titulo = imagen_titulo.get_rect(topleft=(0, 0))
    except:
        imagen_titulo = None

    # 3. Configuración de fuente para las instrucciones
    fuente_inst = pygame.font.SysFont("Arial", 45, bold=True)
    reloj = pygame.time.Clock()

    while True:
        # --- CAPA DE DIBUJO ---
        
        # Primero el fondo base
        if fondo_menu:
            pantalla.blit(fondo_menu, (0, 0))
        else:
            pantalla.fill((0, 0, 0))

        # Segundo el Título cubriendo toda la pantalla
        if imagen_titulo:
            pantalla.blit(imagen_titulo, rect_titulo)

        # Texto de instrucción (lo movemos un poco más abajo para que no tape el logo)
        texto = "Presiona ESPACIO para jugar"
        img_sombra = fuente_inst.render(texto, True, (20, 20, 20))
        img_texto = fuente_inst.render(texto, True, (255, 255, 255))
        
        # Posicionado en la parte inferior de la pantalla
        rect_texto = img_texto.get_rect(center=(ANCHO // 2, ALTO * 0.85))
        
        pantalla.blit(img_sombra, (rect_texto.x + 3, rect_texto.y + 3))
        pantalla.blit(img_texto, rect_texto)

        pygame.display.flip()

        # --- LÓGICA DE EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return 
        
        reloj.tick(60)