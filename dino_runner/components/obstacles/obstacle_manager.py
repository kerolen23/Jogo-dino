import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            #Pegando um numero aleatorio de cada
            type_obstacle = random.randint(0, 1)
            if type_obstacle== 0:
                self.obstacles.append(Cactus()) 
            else: 
                type_obstacle == 1    
                self.obstacles.append(Bird())   
                
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                   pygame.time.delay(500)   
                   game.playing = False
                   game.death_count +=1
                   break
                #Verifica se for hammer 
                else:
                    if game.player.hammer:
                      self.obstacles.remove(obstacle)

    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)   
        
