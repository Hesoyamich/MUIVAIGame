import pygame
import tensorflow as tf
import os
import json

class LaunchModel:
    def __init__(self, main):
        self.main = main
        self.model = None
        self.game = None
        self.state = None
        self.loaded_models = []
        self.button_rects = []
        self.load_model()
        self.init_buttons()

    
    def load_model(self):
        model_folders = os.listdir("models")
        for folder in model_folders:
            files = os.listdir(f"models/{folder}")
            if "config.json" in files and "model.keras" in files:
                config = None
                with open(f"models/{folder}/config.json", "r") as f:
                    config = json.load(f)
                self.loaded_models.append([folder, config])

    def init_buttons(self):
        for i, model in enumerate(self.loaded_models):
            rect = pygame.Rect(0, 0, 500, 100)
            rect.centerx = 500
            rect.centery = 150 + 120 * i
            self.button_rects.append(rect)

    def update(self, mouse_pos, mouse_press, key):
        event = None
        if key:
            if key.key == pygame.K_ESCAPE:
                event = 'back_to_menu'
        
        if not self.game:
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos) and mouse_press:
                    self.game = self.main.games[self.loaded_models[i][1]["game"]]["game_class"](settings=self.loaded_models[i][1]["settings"])
                    self.model = tf.keras.models.load_model(f"models/{self.loaded_models[i][0]}/model.keras")
                    self.state = self.game.reset()

        else:
            state_tensor = tf.convert_to_tensor([self.state])
            q_values = self.model(state_tensor)
            action = tf.argmax(q_values[0]).numpy()

            self.state, reward, done = self.game.step(action)

            if done:
                self.state = self.game.reset()
                

        return event

    def render(self, display):
        if not self.game:
            for i, rect in enumerate(self.button_rects):
                pygame.draw.rect(display, (23, 23, 23), rect)
                model_name_text = self.main.f1.render(f"Название модели: {self.loaded_models[i][0]}", True, (255, 255, 255))
                model_name_rect = model_name_text.get_rect(top=rect.top, centerx=rect.centerx)
                display.blit(model_name_text, model_name_rect)
                game_name_text = self.main.f1.render(f"Игра: {self.loaded_models[i][1]['game']}", True, (255, 255, 255))
                game_name_rect = game_name_text.get_rect(centerx=rect.centerx, bottom=rect.bottom)
                display.blit(game_name_text, game_name_rect)
        else:
            self.game.render(display)


if __name__ == "__main__":
    l = LaunchModel(1)
    print(l.loaded_models)