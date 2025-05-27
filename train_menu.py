import pygame
from dqnagent import DQNAgent

class TrainMenu:
    def __init__(self, game):
        self.game = game

        self.step = 0
        self.step_buttons = {0:[], 1:[], 2: [], 4: []}
        self.step_description = ["Выберите игру.", "Настройки игры и награды.", "Модель нейронной сети.", "Парамеры нейронной сети и обучения."]
        self.desc_mark = self.game.f2.render("!", True, (255,255,255))
        # Кнопка вернуться назад
        self.back_button = self.game.f1.render("Назад", True, (255, 255, 255))
        self.back_button_rect = self.back_button.get_rect()
        self.back_button_rect.bottomleft = (50, 1000 - 50)
        # Кнопка вернуться вперед
        self.next_button = self.game.f1.render("След. шаг", True, (255, 255, 255))
        self.next_button_rect = self.next_button.get_rect()
        self.next_button_rect.bottomright = (1000 - 50, 1000 - 50)
        # Фильтр ввода
        self.numbers_filter = "1234567890-."
        self.filename_filter = '\/:*?<>|"'
        #Данные для обучения
        self.selected_game = None
        self.initialize_games()

    def initialize_games(self):
        for i, game in enumerate(self.game.games.keys()):
            text_surf = self.game.f1.render(game, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topleft=(250, 250 + 100 * i)).inflate(50, 20)
            desc_rect = pygame.Rect(0, 0, text_rect.height, text_rect.height)
            desc_rect.center = (190, text_rect.centery)
            desc = self.game.games[game]["desc"]
            self.step_buttons[0].append([game, text_surf, text_rect, desc, desc_rect])

    def update(self, mouse_pos, mouse_click, key):
        event = None
        if self.next_button_rect.collidepoint(mouse_pos) and mouse_click:
            if self.step == 0 and self.selected_game != None:
                event = "train_next"
        if self.back_button_rect.collidepoint(mouse_pos) and mouse_click:
            event = "train_back"
        
        if self.step == 0:
            for game in self.step_buttons[0]:
                if game[2].collidepoint(mouse_pos) and mouse_click:
                    self.selected_game = game[0]

        return event

    
    def render(self, display):
        gap = (1000 - 200) / 4
        for i in range(4):
            if i == self.step:
                text = self.game.f1.render(f"Шаг {i + 1}", True, (123, 42, 72))
                display.blit(text, (100 + i * gap, 50))
            else:
                text = self.game.f1.render(f"Шаг {i + 1}", True, (240, 240, 240))
                display.blit(text, (100 + i * gap, 50))
        text = self.game.f1.render(self.step_description[self.step], True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (500, 150)
        display.blit(text, text_rect)

        if self.step == 0:
            for game in self.step_buttons[0]:
                pygame.draw.rect(display, (63, 63, 63), game[2], 0, 5)
                if self.selected_game == game[0]:
                    pygame.draw.rect(display, (123, 42, 72), game[2], 5, 5)
                else:
                    pygame.draw.rect(display, (113, 113, 113), game[2], 5, 5)
                text_rect = game[1].get_rect(center=game[2].center)
                display.blit(game[1], text_rect) 
                pygame.draw.rect(display, (63, 63, 63), game[4])
                center_text = self.desc_mark.get_rect(center=game[4].center)
                display.blit(self.desc_mark, center_text)
                pos = pygame.mouse.get_pos()
                if game[4].collidepoint(pos):
                    desc_text = self.game.f1.render(game[3], True, (255,255,255))
                    desc_rect = desc_text.get_rect(topleft=pos)
                    pygame.draw.rect(display, (113, 113, 113), desc_rect)
                    display.blit(desc_text, desc_rect)
                    

        display.blit(self.next_button, self.next_button_rect)
        display.blit(self.back_button, self.back_button_rect)


