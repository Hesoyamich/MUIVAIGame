import pygame
import numpy as np
import random


class JumpyBird:
    def __init__(self, settings={"pipe_space": 300, "pipe_gap": 150, "pipe_width": 30}, rewards={"survivability": 0.1, "jumping": 0.2, "collision": -10, "getting_score": 5}):
        self.bird_y = 1000 // 2
        self.bird_velocity = 0
        self.bird_size = 30
        self.gravity = 0.5
        self.jump_force = -8
        self.pipes = []
        self.score = 0
        self.pipe_space = settings["pipe_space"]
        self.pipe_gap = settings['pipe_gap']
        self.pipe_width = settings["pipe_width"]
        self.rewards = rewards
        self.pipe_speed = 3

    def add_pipe(self):
        pipe_top = random.randint(50, 1000 - self.pipe_gap - 50)
        self.pipes.append({
            'x': 1000,
            'top': pipe_top,
            'passed': False
        })

    def reset(self):
        self.bird_y = 1000 // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.add_pipe()
        return self.get_state()
    
    def get_state(self):
        # State: bird_y, bird_velocity, next_pipe info
        if len(self.pipes) > 0:
            next_pipe = self.pipes[0]
            pipe_x = next_pipe['x']
            pipe_top = next_pipe['top']
            pipe_bottom = pipe_top + self.pipe_gap
            horizontal_distance = (pipe_x - 1000/2) / 1000
        else:
            horizontal_distance = 1.0
            pipe_top = 0
            pipe_bottom = 1000

        return np.array([
            self.bird_y / 1000,
            self.bird_velocity / 10,
            horizontal_distance,
            pipe_top / 1000,
            pipe_bottom / 1000
        ])
    
    def step(self, action):
        reward = 0
        reward += self.rewards["survivability"]  # Награда за выживаемость
        done = False

        # Прыжок
        if action == 1:
            self.bird_velocity = self.jump_force
            reward = self.rewards["jumping"]  # Награда за прыжки

        # Гравитация
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        # Двигать трубы
        for pipe in self.pipes:
            pipe['x'] -= self.pipe_speed

        # Колизия экрана
        if self.bird_y < 0 or self.bird_y + self.bird_size > 1000:
            reward += self.rewards["collision"]
            done = True

        # Колизия труб
        bird_rect = pygame.Rect(1000//2 - self.bird_size//2, self.bird_y, self.bird_size, self.bird_size)
        for pipe in self.pipes:
            pipe_rect_top = pygame.Rect(pipe['x'], 0, self.pipe_width, pipe['top'])
            pipe_rect_bottom = pygame.Rect(pipe['x'], pipe['top'] + self.pipe_gap, 
                                         self.pipe_width, 1000)
            
            if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
                reward = self.rewards["collision"]
                done = True

            # Подсчёт очков
            if not pipe['passed'] and pipe['x'] + self.pipe_width < 1000//2:
                pipe['passed'] = True
                self.score += 1
                reward += self.rewards["getting_score"]

        # Удаление труб.
        self.pipes = [p for p in self.pipes if p['x'] > -self.pipe_width]
        if len(self.pipes) == 0 or self.pipes[-1]['x'] < 1000 - self.pipe_space:
            self.add_pipe()

        return self.get_state(), reward, done
    
    def render(self, display):
        
        # Рендер птицы
        pygame.draw.circle(display, (255, 255, 0), 
                          (1000//2, int(self.bird_y)), self.bird_size//2)
        
        # Рендер труб
        for pipe in self.pipes:
            pygame.draw.rect(display, (0, 128, 0),
                            (pipe['x'], 0, self.pipe_width, pipe['top']))
            pygame.draw.rect(display, (0, 128, 0),
                            (pipe['x'], pipe['top'] + self.pipe_gap, 
                             self.pipe_width, 1000))