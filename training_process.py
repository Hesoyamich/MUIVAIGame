import pygame
from dqnagent import DQNAgent
import numpy as np

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


    def update(self, mouse_pos, mouse_press, key):
        event = None
        if self.done:
            self.done = False
            self.current_episode += 1
            self.state = self.game.reset()
            self.total_reward = 0
            self.total_time = 0
            self.eps_data.append(self.agent.epsilon)
            self.scores.append(self.total_reward)
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

        if key:
            if key.key == pygame.K_ESCAPE:
                event = "stop_training"

        return event
    
    def render(self, display):
        train_text = self.font.render(f"Эпизод: {self.current_episode}. Награды за эпизод: {self.total_reward}. \n Средняя награда: {np.mean(self.scores[-100:])} Эпсилон: {self.agent.epsilon}", True, (255, 255, 255))
        display.blit(train_text, (10, 500))