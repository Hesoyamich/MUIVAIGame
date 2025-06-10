import pygame
import numpy as np
import random


class AsteroidDodger:

    def __init__(self, settings={"player_size": 30, "asteroid_size": 25, "max_asteroids": 5}, rewards={"survival": 0.1, "collision": -10}):
        self.player_size = settings["player_size"]
        self.asteroid_size = settings["asteroid_size"]
        self.max_asteroids = settings["max_asteroids"]

        self.player_x = 1000 // 2
        self.player_y = 1000 - 50
        self.asteroids = []
        self.score = 0
        self.rewards = rewards

    def reset(self):
        self.player_x = 1000 // 2
        self.asteroids = []
        self.score = 0
        self.add_asteroid()
        return self.get_state()
    
    def get_state(self):
        # State: player_x, player_velocity_x, asteroid positions (x,y)
        state = [self.player_x / 1000, 0]  # Нормализованое значение позиции игрока
        
        # Добавить астеройды в состояние
        for asteroid in self.asteroids:
            state.extend([asteroid['x']/1000, asteroid['y']/1000])
        
        # Заполнить несуществующие астеройды значением -1
        while len(state) < 2 + self.max_asteroids*2:
            state.extend([-1.0, -1.0])
        

        return np.array(state)
    
    def add_asteroid(self):
        if len(self.asteroids) < self.max_asteroids:
            self.asteroids.append({
                'x': random.randint(0, 1000 - self.asteroid_size),
                'y': -self.asteroid_size,
                'speed': random.uniform(3, 8)
            })

    def step(self, action):
        reward = 0
        reward += self.rewards["survival"]  # Награда за выживание
        done = False
        
        # Движение игрока (Действие 0: Влево, 1: Вправо)
        if action == 0:
            self.player_x = max(0, self.player_x - 5)
        elif action == 1:
            self.player_x = min(1000 - self.player_size, self.player_x + 5)

        # Обновить позиции астеройдов
        for asteroid in self.asteroids:
            asteroid['y'] += asteroid['speed']
            
            # Check collision
            if (self.player_x < asteroid['x'] + self.asteroid_size and
                self.player_x + self.player_size > asteroid['x'] and
                self.player_y < asteroid['y'] + self.asteroid_size and
                self.player_y + self.player_size > asteroid['y']):
                reward += self.rewards["collision"]
                done = True
                
        # Remove off-screen asteroids and add new ones
        self.asteroids = [a for a in self.asteroids if a['y'] < 1000]
        self.add_asteroid()
        
        self.score += 1
        return self.get_state(), reward, done

    def render(self):
        self.screen.fill((0, 0, 0))
        
        # Draw player
        pygame.draw.rect(self.screen, (0, 255, 0), 
                        (self.player_x, self.player_y, self.player_size, self.player_size))
        
        # Draw asteroids
        for asteroid in self.asteroids:
            pygame.draw.circle(self.screen, (255, 0, 0),
                             (asteroid['x'], asteroid['y']), self.asteroid_size)


