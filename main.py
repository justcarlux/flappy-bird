from game import FlyingDuckGame
from arcade_machine_sdk import GameMeta
import pygame

# 1. Inicializar Pygame
if not pygame.get_init():
    pygame.init()

# 2. ¡ESTA ES LA LÍNEA QUE FALTA! 
# Debes definir una resolución (ejemplo 400x600) antes de cargar imágenes.
# Si tu juego ya define esto internamente, asegúrate de que ocurra ANTES de self.fondo.convert()
screen = pygame.display.set_mode((400, 600)) 

# Configuración de Metadata
metadata = (GameMeta()
            .with_title("Flying Duck")
            .with_description("Esquiva las tuberías y demuestra tus reflejos con el pato más audaz.")
            .with_release_date("17/02/2026")
            .with_group_number(6)
            .add_tag("Arcade")
            .add_tag("Flyer")
            .add_tag("Jump")
            .add_author("Antonella Fermin")
            .add_author("Alexandra Cedeño"))

# 3. Ahora sí, al inicializar el juego, el "video mode" ya existe
game = FlyingDuckGame(metadata)

if __name__ == "__main__":
    game.run_independently()