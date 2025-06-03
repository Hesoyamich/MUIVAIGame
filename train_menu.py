import pygame
from dqnagent import DQNAgent

class TrainMenu:
    def __init__(self, game):
        self.game = game

        self.step = 0
        self.step_buttons = {0:[], 1:[], 2: [], 3: []}
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
        self.second_numbers_filter = "1234567890"
        self.filename_filter = '\/:*?<>|"'
        self.selected_field = None
        #Данные для обучения
        self.selected_game = None
        self.field_value = None
        self.game_settings = {}
        self.rewards = {}
        self.initialize_games()
        # 3 экран
        self.input_layer_text = None
        self.input_layer_rect = None
        self.layers = []
        self.layers_rects = []
        self.delete_layer_rect = pygame.Rect(0, 0, 50, 50)
        self.add_layer_rect = pygame.Rect(0, 0, 200, 50)
        # 4 экран
        self.gamma = 0.95
        self.memory = 20000
        self.epsilon_decay = 0.995
        self.batch_size = 64
        self.learning_rate = 0.001
        self.episodes = 100

    def initialize_games(self):
        for i, game in enumerate(self.game.games.keys()):
            text_surf = self.game.f1.render(game, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topleft=(250, 250 + 100 * i)).inflate(50, 20)
            desc_rect = pygame.Rect(0, 0, text_rect.height, text_rect.height)
            desc_rect.center = (190, text_rect.centery)
            desc = self.game.games[game]["desc"]
            self.step_buttons[0].append([game, text_surf, text_rect, desc, desc_rect])

    def init_train_options(self):
        options = ["Gamma", "Memory", "Epsilon Decay", "Batch Size", "Learning Rate", "Episodes"]
        self.gamma = 0.95
        self.memory = 20000
        self.epsilon_decay = 0.995
        self.batch_size = 64
        self.learning_rate = 0.001
        self.episodes = 100
        for i, option in enumerate(options):
            rect = pygame.Rect(510, 250 + 100 * i, 120, 50)
            self.step_buttons[3].append([option, rect])
        

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

    def init_layers(self):
        self.layers = []
        self.layers_rects = []
        add_inputs = self.game.games[self.selected_game]["add_size"]
        inputs = self.game.games[self.selected_game]["min_state_size"] + self.game_settings[add_inputs[0]] * add_inputs[1]
        self.input_layer_text = self.game.f1.render(f"Входной слой: {inputs} нейроннов", True, (255,255,255))

        self.input_layer_rect = self.input_layer_text.get_rect()
        self.input_layer_rect.center = (500, 250)

        self.layers.append(128)
        layer_rect = pygame.Rect(0, 0, 200, 50)
        layer_rect.center = (500, 350)
        self.layers_rects.append(layer_rect)
    
    def update_layers_buttons(self):
        # Обновление позиции кнопки удаления слоя
        self.delete_layer_rect.centery = self.layers_rects[-1].centery
        self.delete_layer_rect.left = self.layers_rects[-1].right + 10
        # Обновление позиции кнопки добавления слоя
        self.add_layer_rect.top = self.layers_rects[-1].bottom + 20
        self.add_layer_rect.centerx = self.layers_rects[-1].centerx

    def update(self, mouse_pos, mouse_click, key):
        event = None
        if self.next_button_rect.collidepoint(mouse_pos) and mouse_click:
            if self.step == 0 and self.selected_game != None:
                event = "train_next"
                self.init_rewards()
            if not self.selected_field and self.step == 1:
                event = "train_next"
                self.init_layers()
                self.update_layers_buttons()
            if not self.selected_field and self.step == 2:
                event = "train_next"
                self.init_train_options()
            if not self.selected_field and self.step == 3:
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
                                self.game_settings[self.selected_field] = int(self.field_value)
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
        if self.step == 2:
            for i, rect in enumerate(self.layers_rects):
                if rect.collidepoint(mouse_pos) and mouse_click:
                    self.selected_field = i
                    self.field_value = str(self.layers[i])
            if self.selected_field != None:
                if key != None:
                    if key.key == pygame.K_BACKSPACE:
                        self.field_value = self.field_value[:-1]
                    elif key.key == pygame.K_RETURN:
                        if len(self.field_value) == 0:
                            self.field_value = 1

                        self.layers[self.selected_field] = int(self.field_value)
                        self.field_value = None
                        self.selected_field = None
                    else:
                        if key.unicode in self.second_numbers_filter:
                            self.field_value += key.unicode
                            print(self.field_value)

            if len(self.layers) < 5:
                if self.add_layer_rect.collidepoint(mouse_pos) and mouse_click:
                    layer_rect = pygame.Rect(0, 0, 200, 50)
                    layer_rect.center = (500, 350 + 75 * len(self.layers))
                    self.layers_rects.append(layer_rect)
                    self.layers.append(64)
                    self.update_layers_buttons()
                    self.field_value = None
                    self.selected_field = None
            
            if len(self.layers) > 1:
                if self.delete_layer_rect.collidepoint(mouse_pos) and mouse_click:
                    self.layers_rects.pop()
                    self.layers.pop()
                    self.update_layers_buttons()
                    self.field_value = None
                    self.selected_field = None
                    
        # Четвертый экран
        if self.step == 3:
            for button in self.step_buttons[3]:
                if button[1].collidepoint(mouse_pos) and mouse_click:
                    self.selected_field = button[0]
                    if button[0] == "Gamma":
                        self.field_value = str(self.gamma)
                    elif button[0] == "Memory":
                        self.field_value = str(self.memory)
                    elif button[0] == "Epsilon Decay":
                        self.field_value = str(self.epsilon_decay)
                    elif button[0] == "Batch Size":
                        self.field_value = str(self.batch_size)
                    elif button[0] == "Learning Rate":
                        self.field_value = str(self.learning_rate)
                    elif button[0] == "Episodes":
                        self.field_value = str(self.episodes)

            if self.selected_field != None:
                if key != None:
            
                    if key.key == pygame.K_BACKSPACE:
                        self.field_value = self.field_value[:-1]
                    elif key.key == pygame.K_RETURN:
                        if len(self.field_value) == 0:
                            self.field_value = 0

                        if self.selected_field == "Gamma":
                            self.gamma = float(self.field_value)
                        elif self.selected_field == "Memory":
                            self.memory = int(self.field_value)
                        elif self.selected_field == "Epsilon Decay":
                            self.epsilon_decay = float(self.field_value)
                        elif self.selected_field == "Batch Size":
                            self.batch_size = int(self.field_value)
                        elif self.selected_field == "Learning Rate":
                            self.learning_rate = float(self.field_value)
                        elif self.selected_field == "Episodes":
                            self.episodes = int(self.learning_rate)

                        self.selected_field = None
                        self.field_value = None
                    
                    else:
                        if key.unicode in self.numbers_filter:
                            self.field_value += key.unicode

                    


        return event

    
    def render(self, display):
        if self.step != 4:
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
                number = 0
                pygame.draw.rect(display, (63, 63, 63), option[1], 0, 5)
                text_rect = option[0].get_rect(center=option[1].center)
                display.blit(option[0], text_rect) 
                pygame.draw.rect(display, (255,255,255), option[2], 0, 5)
                if option[3] == self.selected_field:
                    pygame.draw.rect(display, (123, 42, 72), option[2], 5, 5)
                    number = self.field_value
                else:
                    number = self.game_settings[option[3]] if option[3] in self.game_settings else self.rewards[option[3]]
                option_text = self.game.f1.render(str(number), True, (23, 23, 23))
                option_rect = option_text.get_rect(center=option[2].center)
                display.blit(option_text, option_rect)

        # Третий экран
        if self.step == 2:
            pygame.draw.rect(display, (63, 63, 63), self.input_layer_rect)
            display.blit(self.input_layer_text, self.input_layer_rect)
            for i, layer in enumerate(self.layers):
                layer_text = self.game.f1.render(f"Слой {i + 1}: {layer}", True, (255,255,255))
                if i == self.selected_field:
                    pygame.draw.rect(display, (123, 42, 72), self.layers_rects[i], 5, 5)
                else:
                    pygame.draw.rect(display, (63, 63, 63), self.layers_rects[i])
                display.blit(layer_text, layer_text.get_rect(center = self.layers_rects[i].center))
            
            if len(self.layers) < 5:
                pygame.draw.rect(display, (63,63,63), self.add_layer_rect)
                add_layer_text = self.game.f1.render("Добавить слой", True, (255, 255, 255))
                add_layer_text_rect = add_layer_text.get_rect(center=self.add_layer_rect.center)
                display.blit(add_layer_text, add_layer_text_rect)
            
            if len(self.layers) > 1:
                pygame.draw.rect(display, (123, 42, 72), self.delete_layer_rect)

            
            output_text = self.game.f1.render(f"Выходной слой: {self.game.games[self.selected_game]['action_size']}", True, (255,255,255))
            output_rect = output_text.get_rect(center=(500, 350 + len(self.layers) * 75 + 100))
            pygame.draw.rect(display, (63, 63, 63), output_rect)
            display.blit(output_text, output_rect)

        if self.step == 3:
            for button in self.step_buttons[3]:
                option_text = self.game.f1.render(button[0] + ":", True, (255, 255, 255))
                option_rect = option_text.get_rect(right=button[1].left, centery=button[1].centery)
                display.blit(option_text, option_rect)
                pygame.draw.rect(display, (255, 255, 255), button[1])
                if self.selected_field == button[0]:
                    pygame.draw.rect(display, (123, 42, 72), button[1], 5, 5)
                if self.selected_field != button[0]:
                    field_text = None
                    if button[0] == "Gamma":
                        field_text = self.gamma
                    elif button[0] == "Memory":
                        field_text = self.memory
                    elif button[0] == "Epsilon Decay":
                        field_text = self.epsilon_decay
                    elif button[0] == "Batch Size":
                        field_text = self.batch_size
                    elif button[0] == "Learning Rate":
                        field_text = self.learning_rate
                    elif button[0] == "Episodes":
                        field_text = self.episodes
                        
                    field_text_surf = self.game.f1.render(str(field_text), True, (63, 63, 63))
                    field_rect = field_text_surf.get_rect(center = button[1].center)
                    display.blit(field_text_surf, field_rect)
                else:
                    field_text_surf = self.game.f1.render(str(self.field_value), True, (63, 63, 63))
                    field_rect = field_text_surf.get_rect(center = button[1].center)
                    display.blit(field_text_surf, field_rect)


        display.blit(self.next_button, self.next_button_rect)
        display.blit(self.back_button, self.back_button_rect)


