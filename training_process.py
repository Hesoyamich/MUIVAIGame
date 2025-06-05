import pygame
from dqnagent import DQNAgent
import numpy as np
from draw_plot import draw_plot

class TrainingProcessMenu:
    def __init__(self, font, game, settings, rewards, layers, gamma, memory, epsilon_decay, batch_size, learning_rate, episodes, state_size, action_size):
        self.font = font
        self.game = game(settings, rewards)
        self.agent = DQNAgent(state_size, action_size, memory, gamma, epsilon_decay=epsilon_decay, batch_size=batch_size, lr=learning_rate, layers=layers)
        self.episodes = episodes
        self.current_episode = 0
        self.done = False
        self.eps_data = []
        self.scores = []
        self.total_reward = 0
        self.total_time = 0
        self.state = self.game.reset()
        self.is_training = True
        self.plot = None
        # Кнопки после обучения
        self.back_to_menu_text = self.font.render("Венуться в меню", True, (255, 255, 255))
        self.back_to_menu_rect = self.back_to_menu_text.get_rect(left=20, centery=960)
        self.save_model_text = self.font.render("Сохранить модель", True, (255, 255, 255))
        self.save_model_rect = self.back_to_menu_text.get_rect(right=950, centery=960)
        # Кнопки сохранения модели
        self.saving_model = False



    def update(self, mouse_pos, mouse_press, key):
        event = None
        if self.done:
            self.done = False
            self.current_episode += 1
            self.state = self.game.reset()
            self.scores.append(self.total_reward)
            self.total_reward = 0
            self.total_time = 0
            self.eps_data.append(self.agent.epsilon)
            if self.current_episode == self.episodes:
                self.is_training = False
                x = [i+1 for i in range(self.episodes)]
                plot = draw_plot(x, self.scores, self.eps_data)
                self.plot = pygame.image.frombuffer(plot[0], plot[1], "RGBA")
        if self.is_training:
            action = self.agent.take_action(self.state)
            next_state, reward, self.done = self.game.step(action)
            self.agent.remember(self.state, action, reward, next_state, self.done)
            self.state = next_state
            self.total_reward += reward
            self.total_time += 1
        
            # Обучение
            self.agent.train()
            
            # Обновлять целевую модель переодически
            if self.total_time % self.agent.update_target_every == 0:
                self.agent.update_target_network()

        if key and self.is_training:
            if key.key == pygame.K_ESCAPE:
                event = "stop_training"

        if not self.is_training:
            if self.back_to_menu_rect.collidepoint(mouse_pos) and mouse_press:
                event = "back_to_menu"
            if self.save_model_rect.collidepoint(mouse_pos) and mouse_press:
                self.saving_model = True
                
        
        

        return event
    
    def render(self, display):
        if self.is_training:
            train_text = self.font.render(f"Эпизод: {self.current_episode}. Награды за эпизод: {self.total_reward}. \n Средняя награда: {np.mean(self.scores[-100:])} Эпсилон: {self.agent.epsilon}", True, (255, 255, 255))
            display.blit(train_text, (10, 500))
        else:
            display.blit(self.plot, (0,0))
            display.blit(self.back_to_menu_text, self.back_to_menu_rect)
            display.blit(self.save_model_text, self.save_model_rect)