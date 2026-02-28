import pygame, sys
from tuberia import Tuberia
import puntuaciones 
import menu  # Importamos tu nuevo módulo de menú

# --- Clase del Jugador ---
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen_original = pygame.image.load("imagenes/PATO DEFINITIVO.jpeg").convert()
        color_fondo = self.imagen_original.get_at((0,0))
        self.imagen_original.set_colorkey(color_fondo)
        
        self.image = pygame.transform.scale(self.imagen_original, (80, 80))
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

# --- Inicialización del Motor ---
pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flying Duck")

# --- Carga de Recursos ---
try:
    pygame.mixer.music.load("sounds/musica_fondo.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)
    sonido_colision = pygame.mixer.Sound("sounds/sonido_colision.mp3")
    sonido_puntaje = pygame.mixer.Sound("sounds/sonido_puntaje.mp3") 
except:
    sonido_colision = None
    sonido_puntaje = None

imagen_tubo = pygame.image.load("imagenes/tubo.jpeg").convert_alpha()
imagen_tubo = pygame.transform.scale(imagen_tubo, (80, 400))
fondo = pygame.image.load("imagenes/fondo3.jpg").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# --- Variables Globales ---
reloj = pygame.time.Clock()
FPS = 60 
ESPACIO_TUBERIAS = 220
EVENTO_NUEVA_TUBERIA = pygame.USEREVENT
pygame.time.set_timer(EVENTO_NUEVA_TUBERIA, 1500)

fuente = pygame.font.SysFont(None, 60)
fuente_pequena = pygame.font.SysFont(None, 35)

# --- Funciones de Lógica de Juego ---

def reiniciar_variables():
    """Limpia el juego para una nueva partida"""
    global grupo_tuberias, puntuacion, record
    if puntuacion > record:
        record = puntuacion
        puntuaciones.guardar_puntuacion_maxima(record)
    
    grupo_tuberias.clear()
    jugador.rect.center = (200, 300)
    jugador.velocidad = 0
    puntuacion = 0

def pantalla_perdiste():
    """Bucle de la pantalla de Game Over"""
    fuente_p = pygame.font.SysFont(None, 80)
    fuente_o = pygame.font.SysFont(None, 40)
    
    while True:
        # Dibujar una capa oscura sobre el juego pausado
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0,0))

        txt_p = fuente_p.render("PERDISTE", True, (255, 50, 50))
        txt_v = fuente_o.render("Espacio para volver a jugar", True, (255, 255, 255))
        txt_e = fuente_o.render("ESC para volver al menú", True, (200, 200, 200))

        pantalla.blit(txt_p, txt_p.get_rect(center=(ANCHO//2, ALTO//2 - 60)))
        pantalla.blit(txt_v, txt_v.get_rect(center=(ANCHO//2, ALTO//2 + 20)))
        pantalla.blit(txt_e, txt_e.get_rect(center=(ANCHO//2, ALTO//2 + 70)))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    reiniciar_variables()
                    return "JUGANDO"
                if evento.key == pygame.K_ESCAPE:
                    reiniciar_variables()
                    return "MENU"

# --- Bucle de Vida del Juego ---
record = puntuaciones.cargar_puntuacion_maxima()
puntuacion = 0
posicion_fondo = 0
estado_juego = "MENU"

jugador = Jugador()
todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(jugador)
grupo_tuberias = []

while True:
    if estado_juego == "MENU":
        menu.mostrar_menu(pantalla, ANCHO, ALTO)
        estado_juego = "JUGANDO"

    elif estado_juego == "JUGANDO":
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == EVENTO_NUEVA_TUBERIA:
                nueva_tuberia = Tuberia(800, ESPACIO_TUBERIAS, imagen_tubo)
                nueva_tuberia.contado = False 
                grupo_tuberias.append(nueva_tuberia)

        # 1. Fondo infinito
        posicion_fondo -= 2
        if posicion_fondo <= -ANCHO: posicion_fondo = 0 
        pantalla.blit(fondo, (posicion_fondo, 0))
        pantalla.blit(fondo, (posicion_fondo + ANCHO, 0))

        # 2. Tuberías y Colisiones
        for tuberia in grupo_tuberias:
            tuberia.mover()
            tuberia.draw(pantalla)
            
            # Colisión con tubos
            hitbox_pato = jugador.rect.inflate(-20, -20)
            if tuberia.tubo_arriba.colliderect(hitbox_pato) or tuberia.tubo_abajo.colliderect(hitbox_pato):
                if sonido_colision: sonido_colision.play()
                estado_juego = "GAME_OVER"

            # Puntaje
            if not tuberia.contado and tuberia.tubo_arriba.right < jugador.rect.left:
                puntuacion += 1
                tuberia.contado = True
                if sonido_puntaje: sonido_puntaje.play()

        grupo_tuberias = [t for t in grupo_tuberias if not t.fuera_de_pantalla()]

        # 3. Jugador
        todos_los_sprites.update()
        if jugador.rect.top <= 0 or jugador.rect.bottom >= ALTO:
            if sonido_colision: sonido_colision.play()
            estado_juego = "GAME_OVER"
        
        todos_los_sprites.draw(pantalla)

        # 4. Texto de UI
        txt_pts = fuente.render(f"Puntos: {puntuacion}", True, (255, 255, 255))
        txt_rec = fuente_pequena.render(f"Récord: {record}", True, (255, 215, 0))
        pantalla.blit(txt_pts, (20, 20))
        pantalla.blit(txt_rec, (20, 75))

        pygame.display.flip()

    elif estado_juego == "GAME_OVER":
        estado_juego = pantalla_perdiste()

    reloj.tick(FPS)