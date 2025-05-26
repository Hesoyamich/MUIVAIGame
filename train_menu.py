import pygame
from dqnagent import DQNAgent

class TrainMenu:
    def __init__(self, game):
        self.game = game

        self.step = 0
        self.step_buttons = {0:[], 1:[], 2: [], 4: []}
        self.step_description = ["Выберите игру.", "Настройки игры и награды.", "Модель нейронной сети.", "Парамеры нейронной сети и обучения."]
        # Кнопка вернуться назад
        self.back_button = self.game.f1.render("Назад", True, (255, 255, 255))
        self.back_button_rect = self.back_button.get_rect()
        self.back_button_rect.bottomleft = (50, 1000 - 50)
        # Кнопка вернуться вперед
        self.next_button = self.game.f1.render("След. шаг", True, (255, 255, 255))
        self.next_button_rect = self.next_button.get_rect()
        self.next_button_rect.bottomright = (1000 - 50, 1000 - 50)

    def update(self, mouse_pos, mouse_click, key):
        event = None
        if self.next_button_rect.collidepoint(mouse_pos) and mouse_click:
            event = "train_next"
        if self.back_button_rect.collidepoint(mouse_pos) and mouse_click:
            event = "train_back"

        return event

    
    def render(self, display):
        gap = (1000 - 200) / 4
        for i in range(4):
            if i == self.step:
                text = self.game.f1.render(f"Шаг {i + 1}", True, (128, 128, 128))
                display.blit(text, (100 + i * gap, 50))
            else:
                text = self.game.f1.render(f"Шаг {i + 1}", True, (20, 20, 20))
                display.blit(text, (100 + i * gap, 50))
        text = self.game.f1.render(self.step_description[self.step], True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (500, 150)
        display.blit(text, text_rect)
        display.blit(self.next_button, self.next_button_rect)
        display.blit(self.back_button, self.back_button_rect)


