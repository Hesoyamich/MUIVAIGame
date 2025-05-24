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

    def reset(self):
        # Случайные координаты объектов на карте.
        self.agent_pos = [np.random.randint(self.size), np.random.randint(self.size)]
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
            while pos in [self.agent_pos, self.passenger_pos, self.destination_pos] or pos in self.pits:
                pos = [np.random.randint(self.size), np.random.randint(self.size)]
            self.pits.append(pos)
        for i in range(5):
            pos = [np.random.randint(self.size), np.random.randint(self.size)]
            while pos in [self.agent_pos, self.passenger_pos, self.destination_pos] or pos in self.pits + self.obstacles:
                pos = [np.random.randint(self.size), np.random.randint(self.size)]
            self.obstacles.append(pos)

