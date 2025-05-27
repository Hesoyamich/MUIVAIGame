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
        self.selected_field = None
        #Данные для обучения
        self.selected_game = None
        self.field_value = None
        self.game_settings = {}
        self.rewards = {}
        self.initialize_games()

    def initialize_games(self):
        for i, game in enumerate(self.game.games.keys()):
            text_surf = self.game.f1.render(game, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topleft=(250, 250 + 100 * i)).inflate(50, 20)
            desc_rect = pygame.Rect(0, 0, text_rect.height, text_rect.height)
            desc_rect.center = (190, text_rect.centery)
            desc = self.game.games[game]["desc"]
            self.step_buttons[0].append([game, text_surf, text_rect, desc, desc_rect])

    def init_rewards(self):
        self.game_settings = {}
        self.rewards = {}
        # Инициализация настроек
        for i, setting in enumerate(self.game.games[self.selected_game]["game_settings"].keys()):
            setting_text = self.game.f1.render(setting, True, (255, 255, 255))
            text_rect = setting_text.get_rect(topleft=(250, 250 + 80 * i)).inflate(110, 20)
            setting_field = pygame.Rect(text_rect.right + 30, text_rect.top, 100, 40)
            setting_list = self.game.games[self.selected_game]["game_settings"][setting]
            self.step_buttons[1].append([setting_text, text_rect, setting_field, setting_list[0]])
            self.game_settings[setting_list[0]] = setting_list[1]
        # Инициализация наград
        for i, reward in enumerate(self.game.games[self.selected_game]["rewards"].keys()):
            reward_text = self.game.f1.render(reward, True, (255, 255, 255))
            text_rect = setting_text.get_rect(topleft=(250, 250 + len(self.game_settings) * 80 + 80 * i)).inflate(110, 20)
            reward_field = pygame.Rect(text_rect.right + 30, text_rect.top, 100, 40)
            reward_name = self.game.games[self.selected_game]["rewards"][reward]
            self.step_buttons[1].append([reward_text, text_rect, reward_field, reward_name])
            self.rewards[reward_name] = 0

    def update(self, mouse_pos, mouse_click, key):
        event = None
        if self.next_button_rect.collidepoint(mouse_pos) and mouse_click:
            if self.step == 0 and self.selected_game != None:
                event = "train_next"
                self.init_rewards()
            if self.step != 0:
                event = "train_next"
        if self.back_button_rect.collidepoint(mouse_pos) and mouse_click:
            event = "train_back"
        
        # Первый экран
        if self.step == 0:
            for game in self.step_buttons[0]:
                if game[2].collidepoint(mouse_pos) and mouse_click:
                    self.selected_game = game[0]
        
        # Второй экран
        if self.step == 1:
            for option in self.step_buttons[1]:
                if option[2].collidepoint(mouse_pos) and mouse_click:
                    self.selected_field = option[3]
                    print(self.selected_field)
            if self.selected_field:
                if self.field_value == None:
                    self.field_value = str(self.game_settings[self.selected_field]) if self.selected_field in self.game_settings else str(self.rewards[self.selected_field])
                if key != None:
                    if key.key == pygame.K_BACKSPACE:
                        self.field_value = self.field_value[:-1]
                    elif key.key == pygame.K_RETURN:
                        if len(self.field_value) == 0:
                            self.field_value = 0
                        if self.selected_field in self.game_settings:
                            try:
                                self.game_settings[self.selected_field] = float(self.field_value)
                            except:
                                self.game_settings[self.selected_field] = 0
                            
                        if self.selected_field in self.rewards:
                            try:
                                self.rewards[self.selected_field] = float(self.field_value)
                            except:
                                self.rewards[self.selected_field] = 0
                        self.field_value = None
                        self.selected_field = None
                        print(self.rewards)
                    else:
                        if key.unicode in self.numbers_filter:
                            self.field_value += key.unicode
                            if self.field_value.count(".") > 1:
                                self.field_value = self.field_value[:-1]
                            print(self.field_value)

        # Третий экран

        # Четвертый экран

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

        # Первый экран
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
                    
        # Второй экран
        if self.step == 1:
            for option in self.step_buttons[1]:
                pygame.draw.rect(display, (63, 63, 63), option[1], 0, 5)
                text_rect = option[0].get_rect(center=option[1].center)
                display.blit(option[0], text_rect) 
                pygame.draw.rect(display, (255,255,255), option[2], 0, 5)
                if option[3] == self.selected_field:
                    pygame.draw.rect(display, (123, 42, 72), option[2], 5, 5)
                number = self.game_settings[option[3]] if option[3] in self.game_settings else self.rewards[option[3]]
                option_text = self.game.f1.render(str(number), True, (23, 23, 23))
                option_rect = option_text.get_rect(center=option[2].center)
                display.blit(option_text, option_rect)

        display.blit(self.next_button, self.next_button_rect)
        display.blit(self.back_button, self.back_button_rect)


