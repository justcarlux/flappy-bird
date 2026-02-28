import pygame, sys
from pathlib import Path
from tuberia import Tuberia
import puntuaciones 
import menu 
from arcade_machine_sdk import GameBase, BASE_WIDTH, BASE_HEIGHT

# --- CONFIGURACIÓN DE RUTAS ---
GAME_DIR = Path(__file__).resolve().parent
IMAGES_DIR = GAME_DIR / "imagenes"
SOUNDS_DIR = GAME_DIR / "sounds"

# --- CLASE DEL JUGADOR ---
class Jugador(pygame.sprite.Sprite):
    def __init__(self, images_dir):
        super().__init__()
        # Cargamos sin .convert() inicialmente para evitar errores de Video Mode
        self.imagen_original = pygame.image.load(str(images_dir / "PATO DEFINITIVO.jpeg"))
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

        # Límites de pantalla
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocidad = 3 

        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.velocidad = 0

        # Control de salto
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]: 
            self.velocidad = self.salto

# --- CLASE PRINCIPAL DEL JUEGO ---
class FlyingDuckGame(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.width, self.height = BASE_WIDTH, BASE_HEIGHT
        self.state = "MENU"
        
        # Carga de Recursos (Sin .convert() aquí para evitar el error de Video Mode)
        self.fondo_raw = pygame.image.load(str(IMAGES_DIR / "fondo3.jpg"))
        self.fondo = pygame.transform.scale(self.fondo_raw, (self.width, self.height))
        
        self.tubo_raw = pygame.image.load(str(IMAGES_DIR / "tubo.jpeg"))
        self.imagen_tubo = pygame.transform.scale(self.tubo_raw, (80, 400))
        
        # Sonidos
        try:
            self.sonido_colision = pygame.mixer.Sound(str(SOUNDS_DIR / "sonido_colision.mp3"))
            self.sonido_puntaje = pygame.mixer.Sound(str(SOUNDS_DIR / "sonido_puntaje.mp3"))
        except:
            self.sonido_colision = None
            self.sonido_puntaje = None

        self.fuente = pygame.font.SysFont(None, 60)
        self.fuente_pequena = pygame.font.SysFont(None, 35)
        
        self.record = puntuaciones.cargar_puntuacion_maxima()
        self.reset_game_vars()

    def reset_game_vars(self):
        """Reinicia las variables para una nueva partida"""
        self.jugador = Jugador(IMAGES_DIR)
        self.todos_los_sprites = pygame.sprite.Group()
        self.todos_los_sprites.add(self.jugador)
        self.grupo_tuberias = []
        self.puntuacion = 0
        self.posicion_fondo = 0
        self.ESPACIO_TUBERIAS = 220
        self.last_pipe_time = pygame.time.get_ticks()

    def start(self, surface):
        """Se ejecuta cuando el juego inicia realmente y la ventana ya existe"""
        super().start(surface)
        # Ahora que hay una ventana, optimizamos las imágenes
        self.fondo = self.fondo.convert()
        self.imagen_tubo = self.imagen_tubo.convert_alpha()
        
        try:
            pygame.mixer.music.load(str(SOUNDS_DIR / "musica_fondo.mp3"))
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        except: pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game_vars()
                        self.state = "PLAYING"
                    if event.key == pygame.K_ESCAPE:
                        self.reset_game_vars()
                        self.state = "MENU"

    def update(self, dt):
        if self.state == "MENU":
            # Llamamos al menú y cambiamos estado
            menu.mostrar_menu(self._GameBase__surface, self.width, self.height)
            self.state = "PLAYING"

        elif self.state == "PLAYING":
            # Generación de tuberías cada 1.5 segundos
            ahora = pygame.time.get_ticks()
            if ahora - self.last_pipe_time > 1500:
                nueva_tuberia = Tuberia(800, self.ESPACIO_TUBERIAS, self.imagen_tubo)
                self.grupo_tuberias.append(nueva_tuberia)
                self.last_pipe_time = ahora

            # Movimiento del fondo
            self.posicion_fondo -= 2
            if self.posicion_fondo <= -self.width: 
                self.posicion_fondo = 0 

            # Lógica de tuberías
            for tuberia in self.grupo_tuberias:
                tuberia.mover()
                
                # Colisiones con hitbox ajustada
                hitbox_pato = self.jugador.rect.inflate(-20, -20)
                if tuberia.tubo_arriba.colliderect(hitbox_pato) or tuberia.tubo_abajo.colliderect(hitbox_pato):
                    if self.sonido_colision: self.sonido_colision.play()
                    self.finalizar_partida()

                # Sumar puntos
                if not tuberia.contado and tuberia.tubo_arriba.right < self.jugador.rect.left:
                    self.puntuacion += 1
                    tuberia.contado = True
                    if self.sonido_puntaje: self.sonido_puntaje.play()

            # Limpiar tuberías fuera de pantalla
            self.grupo_tuberias = [t for t in self.grupo_tuberias if not t.fuera_de_pantalla()]

            # Actualizar Jugador
            self.todos_los_sprites.update()
            
            # Colisión con suelo o techo
            if self.jugador.rect.top <= 0 or self.jugador.rect.bottom >= self.height:
                if self.sonido_colision: self.sonido_colision.play()
                self.finalizar_partida()

    def render(self, surface=None):
        # Solución al error de argumento: si no pasan surface, usamos la del SDK
        if surface is None:
            surface = self._GameBase__surface

        if self.state == "PLAYING":
            # 1. Dibujar Fondo Infinito
            surface.blit(self.fondo, (self.posicion_fondo, 0))
            surface.blit(self.fondo, (self.posicion_fondo + self.width, 0))

            # 2. Dibujar Tuberías
            for tuberia in self.grupo_tuberias:
                tuberia.draw(surface)

            # 3. Dibujar Jugador
            self.todos_los_sprites.draw(surface)

            # 4. Interfaz de Usuario (UI)
            txt_pts = self.fuente.render(f"Puntos: {self.puntuacion}", True, (255, 255, 255))
            txt_rec = self.fuente_pequena.render(f"Récord: {self.record}", True, (255, 215, 0))
            surface.blit(txt_pts, (20, 20))
            surface.blit(txt_rec, (20, 75))

        elif self.state == "GAME_OVER":
            # Pantalla de fin de juego
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0,0))
            
            f_p = pygame.font.SysFont(None, 80).render("PERDISTE", True, (255, 50, 50))
            f_v = self.fuente_pequena.render("Espacio para volver a jugar", True, (255, 255, 255))
            f_e = self.fuente_pequena.render("ESC para volver al menú", True, (200, 200, 200))
            
            surface.blit(f_p, f_p.get_rect(center=(self.width//2, self.height//2 - 60)))
            surface.blit(f_v, f_v.get_rect(center=(self.width//2, self.height//2 + 20)))
            surface.blit(f_e, f_e.get_rect(center=(self.width//2, self.height//2 + 70)))

    def finalizar_partida(self):
        """Guarda el récord y cambia el estado"""
        if self.puntuacion > self.record:
            self.record = self.puntuacion
            puntuaciones.guardar_puntuacion_maxima(self.record)
        self.state = "GAME_OVER"

    def stop(self):
        super().stop()
        pygame.mixer.music.stop()