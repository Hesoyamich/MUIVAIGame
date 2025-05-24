import pygame
import numpy as np

class TaxiDriver:

    def __init__(self, size=10):
        self.size = size
        self.player_pos = None
        self.passenger_pos = None
        self.destination_pos = None
        self.has_passenger = False
        self.done = False

    def reset(self):
        self.agent_pos = (np.random.randint(self.size), np.random.randint(self.size))
        self.passenger_pos = (np.random.randint(self.size), np.random.randint(self.size))
        while self.passenger_pos == self.agent_pos:
            self.passenger_pos = (np.random.randint(self.size), np.random.randint(self.size))
        self.destination_pos = (np.random.randint(self.size), np.random.randint(self.size))
        while self.destination_pos == self.agent_pos or self.destination_pos == self.passenger_pos:
            self.destination_pos = (np.random.randint(self.size), np.random.randint(self.size))
        self.has_passenger = False
        self.done = False

        self.traps = []
        self.obstacles = []
        for _ in range(3):  
            pos = (np.random.randint(self.size), np.random.randint(self.size))
            while pos in [self.agent_pos, self.passenger_pos, self.destination_pos] or pos in self.traps:
                pos = (np.random.randint(self.size), np.random.randint(self.size))
            self.traps.append(pos)
        for _ in range(5): 
            pos = (np.random.randint(self.size), np.random.randint(self.size))
            while pos in [self.agent_pos, self.passenger_pos, self.destination_pos] or pos in self.traps + self.obstacles:
                pos = (np.random.randint(self.size), np.random.randint(self.size))
            self.obstacles.append(pos)

        self.has_passenger = False
        self.done = False
        return self._get_state()
        return self._get_state()
