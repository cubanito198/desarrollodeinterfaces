import pygame
import random
import os
import subprocess

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Cargar imágenes y redimensionarlas
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Clases del juego
class Player:
    def __init__(self):
        self.image = player_img
        self.x = WIDTH // 2 - 25
        self.y = HEIGHT - 80
        self.speed = 5
        self.bullets = []
    
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - 50:
            self.x += self.speed
    
    def shoot(self):
        bullet = Bullet(self.x + 20, self.y)
        self.bullets.append(bullet)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)

class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(0, HEIGHT // 3)
        self.speed = 2
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, x, y):
        self.image = bullet_img
        self.x = x
        self.y = y
        self.speed = -5
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def main():
    running = True
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy() for _ in range(5)]  # Generar enemigos inicialmente
    
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move("left")
                if event.key == pygame.K_RIGHT:
                    player.move("right")
                if event.key == pygame.K_SPACE:
                    player.shoot()

        player.draw(screen)
        
        # Mover y dibujar balas
        for bullet in player.bullets[:]:  # Copia de la lista para evitar problemas al eliminar elementos
            bullet.move()
            if bullet.y < 0:
                player.bullets.remove(bullet)  # Eliminar balas fuera de la pantalla
            bullet.draw(screen)
        
        # Mover enemigos y detectar colisiones
        for enemy in enemies[:]:  # Copia de la lista
            enemy.move()
            enemy.draw(screen)

            # Comprobar colisión con el jugador
            if enemy.x < player.x + 50 and enemy.x + 40 > player.x and enemy.y < player.y + 50 and enemy.y + 40 > player.y:
                print("¡Game Over!")
                running = False  # Terminar el juego si un enemigo toca al jugador

            # Comprobar colisión con balas
            for bullet in player.bullets[:]:
                if enemy.x < bullet.x < enemy.x + 40 and enemy.y < bullet.y < enemy.y + 40:
                    enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    enemies.append(Enemy())  # Generar un nuevo enemigo
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    
    # Reiniciar el juego automáticamente después de la instalación
    script_path = os.path.abspath(__file__)
    subprocess.run(["python", script_path])

if __name__ == "__main__":
    main()
