import pygame
from scripts.TaxiDriver import TaxiDriver
from scripts.JumpyBird import JumpyBird
from scripts.AsteroidDodger import AsteroidDodger
from main_meny import MainMenu
from train_menu import TrainMenu
from training_process import TrainingProcessMenu
import json
import os
from launch_model import LaunchModel

class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.f1 = pygame.font.Font(None, 36)
        self.f2 = pygame.font.Font(None, 52)
        SCREEN_HEIGHT, SCREEN_WIDTH = 1000, 1000

        self.is_running = True
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.games = {"Taxi Driver": {"desc": "Нейронной сети требуется забрать попутчика \n и отвезти его в точку прибытия.", "game_class": TaxiDriver,
                                      "game_settings": {"Размер карты:":["size", 10], "Количество ям:": ["pits_amount", 0]},
                                      "rewards": {"Наказание за движение:":"step_penalty", "Падение в яму:":"pit_collision", "Стояние на месте:": "staying",
                                                  "Подбор попутчика": "getting_passenger", "Доставка попутчика:": "delivering_passenger", "Движение к цели": 'distance_multiplier',
                                                  "Посещение той же очки:": 'visited'}, "action_size": 4, "min_state_size": 5, "add_size": ["pits_amount", 2]
                                      },
                        "Jumpy Bird": {"desc": "Нейронной сети нужно научиться прыгать между труб.", "game_class": JumpyBird,
                                      "game_settings": {"Растояние между трубами:":["pipe_space", 300], "Шель между труб:": ["pipe_gap", 150], "Ширина трубы:": ["pipe_width", 30]},
                                      "rewards": {"Выживание:":"survivability", "Прыжок:":"jumping", "Колизия:": "collision",
                                                  "Получения очка:": "getting_score"}, "action_size": 2, "min_state_size": 5},
                        "Asteroid Dodger": {"desc": "Нейронной сети нужно научиться уворачиваться от астероидов.", "game_class": AsteroidDodger,
                                      "game_settings": {"Размер игрока:":["player_size", 30], "Размер астероида:": ["asteroid_size", 25], "Количество астероидов:": ["max_asteroids", 5]},
                                      "rewards": {"Выживание:":"survival", "Колизия:": "collision"}, "action_size": 2, "min_state_size": 2, "add_size": ["max_asteroids", 2]}}
        self.menu = MainMenu(self.f1)
        self.train_menu = None
        self.game_state = None
        self.training_proc = None
        self.current_game = None
        

    def run(self):
        while self.is_running:
            mouse_press = False
            key = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_press = True
                if event.type == pygame.KEYDOWN:
                    key = event
            
            mouse_pos = pygame.mouse.get_pos()

            if self.game_state == None:
                menu_event = self.menu.update(mouse_pos, mouse_press, None)
            else:
                menu_event = self.game_state.update(mouse_pos, mouse_press, key)
            if menu_event == "quit":
                self.is_running = False
            if menu_event == "start_nn":
                self.current_game = LaunchModel(self)
                self.game_state = self.current_game
            if menu_event == "train_nn":
                if self.train_menu == None:
                    self.train_menu = TrainMenu(self)
                    self.game_state = self.train_menu
            if menu_event == "train_next":
                self.train_menu.step += 1
                if self.train_menu.step == 4:
                    self.training_proc = TrainingProcessMenu(self.f1, self.games[self.train_menu.selected_game]["game_class"],self.train_menu.game_settings, 
                                                                self.train_menu.rewards, self.train_menu.layers, self.train_menu.gamma, self.train_menu.memory,
                                                                self.train_menu.epsilon_decay, self.train_menu.batch_size, self.train_menu.learning_rate, self.train_menu.episodes,
                                                                self.games[self.train_menu.selected_game]["min_state_size"] + 
                                                                self.train_menu.game_settings[self.games[self.train_menu.selected_game]["add_size"][0]] * 
                                                                self.games[self.train_menu.selected_game]["add_size"][1] if "add_size" in self.games[self.train_menu.selected_game].keys() else self.games[self.train_menu.selected_game]["min_state_size"],
                                                                self.games[self.train_menu.selected_game]['action_size'],
                                                                )
                    self.game_state = self.training_proc
            if menu_event == "train_back":
                self.game_state.step -= 1
                if self.game_state.step < 0:
                    self.train_menu = None
                    self.game_state = None
                
            if menu_event == "stop_training" or menu_event == "back_to_menu":
                self.game_state = None
                self.train_menu = None           

            if menu_event == "save_model":
                self.training_proc.agent.save_model(self.training_proc.model_name)
                conf_file = {"game": self.train_menu.selected_game, "settings": self.train_menu.game_settings}
                with open(f"models/{self.training_proc.model_name}/config.json", "w") as f:
                    json.dump(conf_file, f, indent=4)


            self.display.fill((40, 40, 40))

            if self.game_state == None:
                self.menu.render(self.display)

            else:
                self.game_state.render(self.display)


            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    g = Game()
    g.run()