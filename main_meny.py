import pygame

class MainMenu:
    def __init__(self, font):
        self.buttons = {"Запустить ИИ": "start_nn",
                        "Обучить ИИ": "train_nn",
                        "Выйти": "quit"}
        
        self.font = font
        self.button_rects = {}
        self.text = {}
        self.generate_texts()
        
        
    def update(self, mouse_pos, mouse_click, key):
        event = None
        for rect in self.button_rects.keys():
            if self.button_rects[rect].collidepoint(mouse_pos) and mouse_click:
                event = self.buttons[rect]
                print(event)
        
        return event

    def render(self, display):
        for button in self.buttons.keys():
            pygame.draw.rect(display, (255,0,0), self.button_rects[button])
            display.blit(self.text[button], self.button_rects[button])
            

    def generate_texts(self):
        for i, button in enumerate(self.buttons.keys()):
            self.text[button] = self.font.render(f"{button}", True, "white")
            self.button_rects[button] = self.text[button].get_rect()
            self.button_rects[button].center = (500, 100 * i + 400)
