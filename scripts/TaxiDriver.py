import pygame
import numpy as np

class TaxiDriver:

    def __init__(self, settings={"size": 10, "pits_amount": 0}):
        self.size = settings['size']
        self.player_pos = None
        self.passenger_pos = None
        self.destination_pos = None
        self.pits = []
        self.pits_amount = settings['pits_amount']
        self.has_passenger = False
        self.done = False
        
        self.visited = []


        self.rewards_price = {
            "step_penalty": -0.25,
            "pit_collision": -50,
            "staying": -1,
            "getting_passenger": 50,
            "delivering_passenger": 100,
            "distance_multiplier": 0.2,
            'visited': -5
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
        for i in range(self.pits_amount):
            pos = [np.random.randint(self.size), np.random.randint(self.size)]
            while pos in [self.player_pos, self.passenger_pos, self.destination_pos] or pos in self.pits:
                pos = [np.random.randint(self.size), np.random.randint(self.size)]
            self.pits.append(pos)

        self.has_passenger = False
        self.done = False
        self.visited.clear()
        return self.get_state()
    
    def get_state(self):
        # Нормализация значений к значениям между 0 и 1
        player_x, player_y = self.player_pos
        if not self.has_passenger:
            dest_x, dest_y = self.passenger_pos
        else:
            dest_x, dest_y = self.destination_pos
        
        state = [
            player_x / (self.size - 1),
            player_y / (self.size - 1),
            dest_x / (self.size - 1),
            dest_y / (self.size - 1),
            1.0 if self.has_passenger else 0.0
        ]

        # Добавление каждой ямы и препятствия к массиву
        for pit in self.pits:
            state.extend([pit[0] / (self.size - 1), pit[1] / (self.size - 1)])
        
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
        if new_pos in self.pits:
            reward += self.rewards_price["pit_collision"]
            self.done = True # Закончить игру
        elif new_pos == self.player_pos:
            self.done = True
            reward += self.rewards_price["pit_collision"] # Наказать за стояние на месте

        self.player_pos = new_pos

        if new_pos in self.visited:
            reward += self.rewards_price["visited"]
        else:
            self.visited.append(new_pos)



        # Проверка на игровые события
        if not self.has_passenger and self.player_pos == self.passenger_pos:
            self.has_passenger = True
            reward += self.rewards_price["getting_passenger"]
        if self.has_passenger and self.player_pos == self.destination_pos:
            self.done = True
            reward += self.rewards_price["delivering_passenger"]
        if not self.has_passenger:
            prev_distance = abs(self.player_pos[0] - self.passenger_pos[0]) + abs(self.player_pos[1] - self.passenger_pos[0])
            new_distance = abs(new_pos[0] - self.passenger_pos[0]) + abs(new_pos[1] - self.passenger_pos[0])
            reward += (prev_distance - new_distance) * self.rewards_price["distance_multiplier"]
        if self.has_passenger:
            prev_distance = abs(self.player_pos[0] - self.destination_pos[0]) + abs(self.player_pos[1] - self.destination_pos[1])
            new_distance = abs(new_pos[0] - self.destination_pos[0]) + abs(new_pos[1] - self.destination_pos[1])
            reward += (prev_distance - new_distance) * self.rewards_price["distance_multiplier"]

        if self.has_passenger or self.done:
            self.visited.clear()

        return self.get_state(), reward, self.done
    