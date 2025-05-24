import pygame
import numpy as np

class TaxiDriver:

    def __init__(self, size=10):
        self.size = size
        self.player_pos = None
        self.passenger_pos = None
        self.destination_pos = None
        self.pits = []
        self.obstacles = []
        self.has_passenger = False
        self.done = False
        
        self.rewards_price = {
            "step_penalty": -0.1,
            "obstacle_collision": -2,
            "pit_collision": -50,
            "staying": -1,
            "getting_passenger": 10,
            "delivering_passenger": 100
        }

    def reset(self):
        # Случайные координаты объектов на карте.
        self.player_pos = [np.random.randint(self.size), np.random.randint(self.size)]
        self.passenger_pos = [np.random.randint(self.size), np.random.randint(self.size)]
        while self.passenger_pos == self.player_pos:
            self.passenger_pos = [np.random.randint(self.size), np.random.randint(self.size)]
        self.destination_pos = [np.random.randint(self.size), np.random.randint(self.size)]
        while self.destination_pos in (self.passenger_pos, self.player_pos):
            self.destination_pos = [np.random.randint(self.size), np.random.randint(self.size)]
        
        self.pits = []
        self.obstacles = []
        for i in range(3):
            pos = [np.random.randint(self.size), np.random.randint(self.size)]
            while pos in [self.player_pos, self.passenger_pos, self.destination_pos] or pos in self.pits:
                pos = [np.random.randint(self.size), np.random.randint(self.size)]
            self.pits.append(pos)
        for i in range(5):
            pos = [np.random.randint(self.size), np.random.randint(self.size)]
            while pos in [self.player_pos, self.passenger_pos, self.destination_pos] or pos in self.pits + self.obstacles:
                pos = [np.random.randint(self.size), np.random.randint(self.size)]
            self.obstacles.append(pos)

        self.has_passenger = False
        self.done = False
        return self.get_state()
    
    def get_state(self):
        # Нормализация значений к значениям между 0 и 1
        player_x, player_y = self.player_pos
        passenger_x, passenger_y = self.passenger_pos
        dest_x, dest_y = self.destination_pos
        state = [
            player_x / (self.size - 1),
            player_y / (self.size - 1),
            passenger_x / (self.size - 1),
            passenger_y / (self.size - 1),
            dest_x / (self.size - 1),
            dest_y / (self.size - 1),
            1.0 if self.has_passenger else 0.0
        ]

        # Добавление каждой ямы и препятствия к массиву
        for pit in self.pits:
            state.extend([pit[0] / (self.size - 1), pit[1] / (self.size - 1)])
        for obstacle in self.obstacles:
            state.extend([obstacle[0] / (self.size - 1), obstacle[1] / (self.size - 1)])
        
        return state

    def step(self, action):
        if self.done:
            return self.get_state(), 0, True
        
        x, y = self.player_pos
        # Сохранение новой позиции в массиве.
        if action == 0: # Вверх
            new_pos = [x, max(y - 1, 0)]
        elif action == 1: # Вниз
            new_pos = [x, min(y + 1, self.size - 1)]
        elif action == 2: # Влево
            new_pos = [max(x - 1, 0), y]
        elif action == 3:  # Вправо
            new_pos = [min(x + 1, self.size - 1), y]
        else:
            new_pos = self.player_pos

        # Проверка коллизии и подсчёт наград
        reward = self.rewards_price["step_penalty"]
        if new_pos in self.obstacles:
            reward += self.rewards_price["obstacle_collision"]
            new_pos = self.player_pos # Оставить игрока в том же месте
        elif new_pos in self.pits:
            reward += self.rewards_price["pit_collision"]
            self.done = True # Закончить игру
        elif new_pos == self.player_pos:
            reward += self.rewards_price["staying"] # Наказать за стояние на месте

        self.player_pos = new_pos

        # Проверка на игровые события
        if not self.has_passenger and self.player_pos == self.passenger_pos:
            self.has_passenger = True
            reward += self.rewards_price["getting_passenger"]
        if self.has_passenger and self.player_pos == self.destination_pos:
            self.done = True
            reward += self.rewards_price["delivering_passenger"]

        return self.get_state(), reward, self.done
    